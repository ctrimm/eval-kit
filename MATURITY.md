# The L1–L5 eval maturity scale

Five levels. Most teams stall at L2. The throughline at every level: freeze
gold early, keep it clean, measure with uncertainty, write the decision down.

## L1 — Vibes

**You are here if:** there is no gold set. Evaluation is someone reading a
handful of outputs and saying they look fine. Scores, if any, are a single
number from a run nobody can reproduce.

**Exit criteria (to reach L2):**

- A written gold set exists: concrete inputs with expected outputs.
- Every case was checked by a human who could defend the expected output.
- The set is committed to version control, and its hash is recorded.

**Failure mode:** every model or prompt change is a coin flip dressed up as
progress. Regressions ship silently because nothing would have caught them.

## L2 — Frozen gold

**You are here if:** a hand-verified gold set exists, it was sealed before
the system was built against it, and it is stratified — you can report scores
per case type, not just overall.

**Exit criteria (to reach L3):**

- The gold set has a stated size rationale (what difference do you need to
  detect, at what confidence?).
- Scores are reported with confidence intervals, per stratum.
- At least one pre-registered gate exists and has failed a run at least
  once. A gate that has never failed is a decoration.

**Failure mode — the L2 stall:** this is where most teams stop, and it is
worse than it looks. The gold set exists, so the team believes it "has
evals." But nothing runs the set automatically, so it rots: the task drifts,
the product changes, and the gold set quietly stops describing either. Worse,
because the set is small and visible, the system slowly gets tuned against
it — the gold becomes training data with extra steps. L2 done badly is L1
with paperwork. The exits are automation, intervals, and gates that bite.

## L3 — Synthetic scale with clean gold

**You are here if:** the case count is large enough to detect the
differences you care about, because cases are generated programmatically and
with AI assistance — and a human-verified holdout, drawn from the same
distribution, is kept sealed: never trained on, never tuned against, used
only to confirm that the synthetic majority is not lying.

**Exit criteria (to reach L4):**

- The holdout and the synthetic set agree within a stated margin; when they
  diverge, the divergence is investigated, not averaged away.
- Generation code is versioned with the data it produced.
- Contaminated cases (anything that leaked into training or tuning) are
  retired and the retirement is logged.

**Failure mode:** synthetic cases that all exercise the same easy pattern.
Volume without diversity is a bigger, more confident L2.

## L4 — Trajectory evals

**You are here if:** the unit of evaluation is a whole task, not a single
response. Task success, trajectory quality (did it take a sane path, use the
right tools, recover from errors), and cost are scored as separate numbers —
never blended into one score that hides a tradeoff.

**Exit criteria (to reach L5):**

- Gates are pre-registered per dimension, including a cost ceiling.
- Results are reported as replicates with uncertainty, not a single run.
- A decision log entry exists for every gate change and every ship/no-ship
  call the evals drove.

**Failure mode:** optimizing the blended score. A system that succeeds
slightly more often at three times the cost and twice the weirdness is not
better, and a single number will tell you it is.

## L5 — Living evals

**You are here if:** the evals run themselves. Gold sets are versioned and
refreshed on a schedule, evals run in CI on every relevant change, drift
against prior baselines is flagged automatically, and the decision log is
current enough that a new team member can reconstruct why the system behaves
the way it does.

**Maintenance obligations (there is no exit; L5 is a practice, not a
destination):**

- Refresh gold on a cadence matched to how fast the task itself changes.
- Re-verify the judge on a schedule if a model judge is in use; judges drift
  too.
- Retire stale strata and log the retirement.
- Review the decision log quarterly. Decisions whose evidence has been
  contradicted get a new entry, not a quiet edit.

**Failure mode:** treating L5 as an achievement instead of a chore. The
week the refresh is skipped is the week the eval starts becoming L2 again.
