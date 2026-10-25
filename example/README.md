# The toy example

A complete eval that runs end to end, so you can see every piece of the kit
working before you replace it with your own task.

- `system.py` — the system under test: a keyword-rule classifier that sorts
  311-style messages into seven categories.
- `gold.jsonl` — 30 cases in the format specified in
  `templates/GOLD_SET.md`, each tagged with its category and a difficulty
  stratum (`routine` / `edge`).
- `gates.yaml` — the pre-registered thresholds for this example.
- `expected_output.txt` — the output of the run below, captured verbatim.

Run it:

```
python eval/run_eval.py --gold example/gold.jsonl --system example/system.py --gates example/gates.yaml
```

## What to notice

The system scores 28/30. The two misses (c006, c008) are both in the `edge`
stratum, and both are the same failure: a report phrased without any of the
words the rules key on. That is what the strata are for — the overall 0.933
would let you ship without ever seeing it.

The gates reflect that: `routine` is held to 0.90 because those cases are
the bulk of real traffic and the system should be nearly perfect on them,
while `edge` is gated at 0.70 — a floor, not a target. Raise the edge gate
to 0.95 in `gates.yaml` and re-run: the eval exits nonzero. In a real
project, the follow-up to these misses is a decision-log entry and either a
system change or a justified gate change — never a quiet edit to the gold.

## Replacing it with your task

1. Write your gold set in this format. Seal it.
2. Write a module with `predict(case_input)` that calls your system.
3. Write your gates before the first scored run.
4. Delete the toy files once yours pass — or keep them as a smoke test.
