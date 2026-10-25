"""Pre-registered gate loading and checking.

The gates file uses a small, flat subset of YAML, parsed here so the kit
needs no third-party packages:

    min_accuracy: 0.85
    min_mean_judge_score: 0.85
    strata:
      routine: 0.90
      edge: 0.70

A run passes only if every gate passes. Thresholds belong in the
preregistration, written before the run — not tuned after seeing scores.
A gate that has never failed is a decoration.
"""


def load_gates(path):
    """Parse the flat gates.yaml subset into a dict."""
    gates = {"strata": {}}
    in_strata = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            indented = line[0] in (" ", "\t")
            key, _, value = line.strip().partition(":")
            key, value = key.strip(), value.strip()
            if not indented:
                in_strata = key == "strata"
                if not in_strata:
                    gates[key] = float(value)
            elif in_strata:
                gates["strata"][key] = float(value)
            else:
                raise ValueError(f"Unexpected nested key in gates file: {raw!r}")
    return gates


def check_gates(gates, overall_accuracy, mean_judge_score, strata_accuracy):
    """Return a list of (label, threshold, actual, passed) tuples.

    `actual` is None when a gated stratum is absent from the results —
    which fails the gate. A gate on a stratum you did not measure is a
    failed gate, not a skipped one.
    """
    results = []
    if "min_accuracy" in gates:
        thr = gates["min_accuracy"]
        results.append(("min_accuracy", thr, overall_accuracy,
                        overall_accuracy >= thr))
    if "min_mean_judge_score" in gates:
        thr = gates["min_mean_judge_score"]
        results.append(("min_mean_judge_score", thr, mean_judge_score,
                        mean_judge_score >= thr))
    for stratum, thr in sorted(gates.get("strata", {}).items()):
        actual = strata_accuracy.get(stratum)
        results.append((f"stratum {stratum}", thr, actual,
                        actual is not None and actual >= thr))
    return results
