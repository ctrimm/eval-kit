# Decision Log

## Instructions

- Every data-backed decision gets an entry: **decision, evidence, date**.
- Append-only. When new evidence overturns a decision, add a new entry that
  names the old one. Never edit an old entry into agreement with the
  present — the history is the value.
- "We decided" without numbers is not an entry. If the decision was not
  driven by evidence, say that plainly; an unevidenced call recorded here
  is a smell, and recording it is how you notice the pattern.
- Revisit entries when new evidence contradicts them. A decision log nobody
  re-reads is a write-only memory.

Copy the entry skeleton below for each decision.

---

## YYYY-MM-DD — <short decision title>

**Decision:** What was decided, in one or two sentences. Include the number
that now governs behavior (threshold, version, configuration) if there is
one.

**Evidence:** The data behind the call. Name the eval run, the gold set
version, the scores with intervals, or the measurement. Link the artifact
if one exists.

**Revisit if:** The condition that should reopen this decision. ("If the
edge stratum grows past 500 cases," "if the judge model is retired.")

<!-- Example, filled in:

## 2026-01-15 — Ship extractor v2 behind the 0.85 gate

**Decision:** Promote extractor v2 to production. Overall accuracy gate
stays at 0.85; the `edge` stratum gate rises from 0.60 to 0.70 next cycle.

**Evidence:** Run 2026-01-14 against gold v3 (n=412): overall 0.91
[0.88, 0.94], edge 0.74 [0.66, 0.81], vs v1 overall 0.86 [0.82, 0.89].
Cost per task unchanged within noise. Preregistration: evals/2026-01-14.md.

**Revisit if:** edge accuracy drops below 0.70 on the monthly refresh, or
the holdout starts disagreeing with the synthetic set by more than 5 points.

-->
