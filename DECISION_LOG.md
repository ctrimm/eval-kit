# Decision Log

Every data-backed decision in this repo gets an entry: decision, evidence,
date. Entries are append-only. When new evidence overturns a decision, add a
new entry that names the old one — do not edit history. (Starter template
with the full instructions: `templates/DECISION_LOG.md`.)

---

## 2026-10-24 — Package eval practice as a template repo

**Decision:** Distill the evaluation workflow used across several projects
into a public template repo (eval-kit v1) instead of leaving it as private
habit: a runnable harness, a toy example that passes its own gates, and
copy-in templates for preregistration, gold sets, and decision logs.

**Evidence:** The same four failures kept recurring across projects, and
each one maps to a piece of this kit:

1. *Gold sets built after the system.* Once you have seen the system's
   outputs, you write cases it can pass. Hence: the gold set spec requires
   sealing before the build (`templates/GOLD_SET.md`).
2. *Thresholds chosen after the run.* A gate picked once the scores are
   known always passes. Hence: `templates/PREREGISTRATION.md` is filled in
   before the first scored run, and the harness exits nonzero on a failed
   gate so CI can enforce it.
3. *Point estimates with no uncertainty.* A 0.90 on 30 cases and a 0.90 on
   3,000 cases are different claims. Hence: the harness reports Wilson score
   intervals per stratum, not just accuracy.
4. *Decisions that lived in chat.* Six months later nobody can say why a
   threshold is 0.85. Hence: this log, and the rule that every number-driven
   call gets an entry.

**Design choices made with this entry:**

- *Wilson score intervals, not the normal approximation.* Strata are often
  small (n under 50), where the normal interval can extend past 0 or 1 and
  collapses to zero width at a perfect score. Wilson behaves at both edges.
- *Standard-library-only harness.* Every dependency is adoption friction for
  a template whose whole pitch is "start today." The gates file is a small,
  documented subset of YAML parsed in `eval/gates.py` for the same reason.
- *Exact match is the default judge; a model judge is an interface, not a
  feature.* An unrecorded model judge is a vibe with an API bill. The stub
  in `eval/run_eval.py` refuses to run; subclassing it forces the
  configuration into the preregistration.
- *The example must be able to fail.* `tests/check_example.py` verifies both
  directions: the toy eval passes its gates, and an impossible gate makes it
  exit nonzero. A kit whose demo cannot fail teaches the wrong lesson.

**Revisit if:** the harness needs a feature the standard library makes
painful (parallel trajectory scoring is the likely candidate), or the
maturity scale's level boundaries stop matching how teams actually stall.
