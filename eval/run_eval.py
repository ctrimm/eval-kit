#!/usr/bin/env python3
"""Run an evaluation against a frozen gold set.

Standard library only. Gold set format: templates/GOLD_SET.md.
Gate format: eval/gates.py.

Usage:
    python eval/run_eval.py --gold example/gold.jsonl \
        --system example/system.py --gates example/gates.yaml

The system under test is a Python file defining:

    def predict(case_input):  -> the system's answer, as a string

Scores are exact match (after normalization) plus a judge score, reported
overall and per stratum (per gold-set tag) with Wilson score confidence
intervals. If a gates file is given, the process exits nonzero when any
gate fails — that is what makes the gate real in CI.
"""

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gates import check_gates, load_gates  # noqa: E402


def wilson_interval(successes, n, z=1.96):
    """Wilson score interval for a binomial proportion.

    Preferred over the normal approximation at the small n typical of
    strata: it stays inside [0, 1] and does not collapse at p = 0 or 1.
    """
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


def normalize(text):
    return " ".join(str(text).strip().casefold().split())


class Judge:
    """Judge interface: score() returns a float in [0, 1].

    To use a model judge, subclass this, implement score(), and record the
    model, prompt, and settings in your preregistration BEFORE trusting
    its numbers. An unrecorded judge configuration is not a measurement.
    """

    name = "base"

    def score(self, case_input, expected, predicted):
        raise NotImplementedError


class ExactMatchJudge(Judge):
    name = "exact-match"

    def score(self, case_input, expected, predicted):
        return 1.0 if normalize(expected) == normalize(predicted) else 0.0


class ModelJudgeStub(Judge):
    """Interface stub for an LLM-as-judge. Refuses to run, on purpose."""

    name = "model-stub"

    def score(self, case_input, expected, predicted):
        raise NotImplementedError(
            "ModelJudgeStub does not score anything. Subclass Judge, call "
            "your model in score(), and pre-register its configuration."
        )


JUDGES = {"exact": ExactMatchJudge, "model-stub": ModelJudgeStub}


def load_system(path):
    spec = importlib.util.spec_from_file_location("system_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "predict"):
        raise SystemExit(f"System module {path} must define predict(case_input)")
    return module


def load_gold(path):
    cases = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            case = json.loads(line)
            for field in ("id", "input", "expected", "tags"):
                if field not in case:
                    raise SystemExit(f"{path}:{lineno}: missing field {field!r}")
            cases.append(case)
    if not cases:
        raise SystemExit(f"{path}: no cases found")
    return cases


def summarize(rows):
    """rows: list of dicts with 'correct' (bool) and 'judge' (float)."""
    n = len(rows)
    correct = sum(1 for r in rows if r["correct"])
    accuracy = correct / n
    lo, hi = wilson_interval(correct, n)
    return {
        "n": n,
        "correct": correct,
        "accuracy": accuracy,
        "ci95": [lo, hi],
        "mean_judge_score": sum(r["judge"] for r in rows) / n,
    }


def fmt(stats):
    lo, hi = stats["ci95"]
    return (f"accuracy {stats['accuracy']:.3f} ({stats['correct']}/{stats['n']})"
            f"  95% CI [{lo:.3f}, {hi:.3f}]")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gold", required=True, help="gold set JSONL file")
    parser.add_argument("--system", required=True,
                        help="python file defining predict(case_input)")
    parser.add_argument("--gates", help="gates.yaml file (subset format, see gates.py)")
    parser.add_argument("--judge", default="exact", choices=sorted(JUDGES),
                        help="judge to score with (default: exact)")
    parser.add_argument("--json-out", help="also write the full report as JSON here")
    args = parser.parse_args(argv)

    cases = load_gold(args.gold)
    system = load_system(args.system)
    judge = JUDGES[args.judge]()

    rows = []
    for case in cases:
        predicted = system.predict(case["input"])
        rows.append({
            "id": case["id"],
            "input": case["input"],
            "expected": case["expected"],
            "predicted": predicted,
            "tags": case["tags"],
            "correct": normalize(predicted) == normalize(case["expected"]),
            "judge": judge.score(case["input"], case["expected"], predicted),
        })

    overall = summarize(rows)
    strata = {}
    for tag in sorted({t for r in rows for t in r["tags"]}):
        strata[tag] = summarize([r for r in rows if tag in r["tags"]])

    print(f"Gold set: {args.gold} ({len(cases)} cases)")
    print(f"System:   {args.system}")
    print(f"Judge:    {judge.name}")
    print()
    print(f"Overall: {fmt(overall)}")
    print(f"Mean judge score: {overall['mean_judge_score']:.3f}")
    print()
    print("By stratum:")
    width = max(len(t) for t in strata)
    for tag, stats in strata.items():
        print(f"  {tag:<{width}}  n={stats['n']:<3} {fmt(stats)}")

    misses = [r for r in rows if not r["correct"]]
    if misses:
        print()
        print(f"Mismatches ({len(misses)}):")
        for r in misses:
            print(f"  {r['id']}: expected {r['expected']!r}, got {r['predicted']!r}")

    report = {"overall": overall, "strata": strata, "rows": rows}
    exit_code = 0
    if args.gates:
        gates = load_gates(args.gates)
        results = check_gates(gates, overall["accuracy"],
                              overall["mean_judge_score"],
                              {t: s["accuracy"] for t, s in strata.items()})
        print()
        print(f"Gates ({args.gates}):")
        for label, thr, actual, passed in results:
            actual_s = f"{actual:.3f}" if actual is not None else "not measured"
            print(f"  {label} >= {thr:.2f}: {actual_s}  {'PASS' if passed else 'FAIL'}")
        all_passed = all(p for *_rest, p in results)
        print(f"GATE: {'PASS' if all_passed else 'FAIL'}")
        report["gates"] = [
            {"label": label, "threshold": thr, "actual": actual, "passed": passed}
            for label, thr, actual, passed in results
        ]
        exit_code = 0 if all_passed else 1

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
