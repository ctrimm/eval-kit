#!/usr/bin/env python3
"""Checks for the eval-kit example. Standard library only.

Run directly:

    python tests/check_example.py

or under pytest (the test_* functions are collected). The point of the
third check: a harness whose gates cannot fail is not a harness.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_eval(gates_path):
    return subprocess.run(
        [sys.executable, "eval/run_eval.py",
         "--gold", "example/gold.jsonl",
         "--system", "example/system.py",
         "--gates", str(gates_path)],
        cwd=ROOT, capture_output=True, text=True)


def test_gold_set_shape():
    lines = [l for l in (ROOT / "example/gold.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    cases = [json.loads(l) for l in lines]
    assert len(cases) >= 30, f"expected >= 30 gold cases, got {len(cases)}"
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "gold case ids must be unique"
    for case in cases:
        assert case["input"] and case["expected"], case["id"]
        assert case["tags"], f"{case['id']}: every case needs a stratum tag"


def test_example_eval_passes_gates():
    result = run_eval(ROOT / "example/gates.yaml")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "GATE: PASS" in result.stdout
    assert "95% CI" in result.stdout


def test_gate_failure_exits_nonzero():
    with tempfile.NamedTemporaryFile(
            "w", suffix=".yaml", delete=False) as fh:
        fh.write("min_accuracy: 1.01\n")
        impossible = fh.name
    result = run_eval(impossible)
    assert result.returncode != 0, "an impossible gate must fail the run"
    assert "GATE: FAIL" in result.stdout


if __name__ == "__main__":
    test_gold_set_shape()
    test_example_eval_passes_gates()
    test_gate_failure_exits_nonzero()
    print("ALL CHECKS PASSED")
