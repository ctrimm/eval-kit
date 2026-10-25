# Gold set format

One JSON object per line (JSONL). Four fields:

```json
{"id": "c001", "input": "Huge pothole on Elm Street near the bus stop.", "expected": "pothole", "tags": ["pothole", "routine"]}
```

- **id** — stable, unique string. Never reused, even if the case is retired.
- **input** — exactly what the system under test receives. No cleanup, no
  hints, no formatting the real input would not have.
- **expected** — the gold answer, in the exact form the scorer compares
  against.
- **tags** — list of stratum labels: task type, difficulty, source, whatever
  breakdown you need to see separately. Every case carries at least one
  stratum tag. The harness reports a score and confidence interval per tag.

## Rules

1. **Seal before build.** The set is finished and committed before the
   system is built or tuned against it. Record the commit hash in the
   preregistration. After sealing, changes go through a decision-log entry.
2. **Stratify on purpose.** Overall accuracy hides the failure you care
   about. Decide your strata before you write cases: the easy bulk, the
   edge cases, the categories where an error is expensive.
3. **Keep a clean holdout.** A human-verified subset — a working rule is
   ~50 cases per class — that is never trained on, never tuned against, and
   never used for prompt or threshold selection. It exists to catch the day
   the rest of the set stops being honest. At L3, where most cases are
   synthetic or AI-generated, the holdout is human-verified and the rest is
   not a substitute for it.
4. **Verify like it matters.** Every expected output is checked by a human
   who could defend it. A gold set with wrong gold measures the system
   against noise.
5. **Retire contamination, do not delete it.** If a case leaks into training
   data or gets tuned against directly, mark it retired (move it to a
   `retired.jsonl` with the reason), and log the retirement. Silent edits
   destroy the set's history.
6. **Version the set.** Gold v1, v2, v3 — scores are only comparable within
   a version. A score change across a gold version change is two changes;
   report both.

## Sizing

Decide n from the difference you need to detect, not from how many cases
are easy to write. With a paired comparison and a typical spread of
outcomes, ~50 cases per stratum gives a 95% interval roughly ±14 points;
~250 cases brings it near ±6. If a 5-point regression would change a ship
decision, a 40-case gold set cannot see it — write more cases or accept
the blindness in the preregistration, in writing.
