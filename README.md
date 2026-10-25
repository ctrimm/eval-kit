# eval-kit-template

A starter kit for evaluating AI systems with the discipline the work actually
needs: a gold set frozen before you build, gates written down before you run,
results reported with confidence intervals, and a decision log that records
what the numbers made you do.

Use it as a GitHub template: click "Use this template", replace the toy
example in `example/` with your task, and start at whatever maturity level
you can honestly claim.

## Why this exists

It is for anyone shipping an AI system whose quality claims have to survive
scrutiny — a team about to change a model or a prompt, a researcher reporting
a number other people will cite, a practitioner whose current eval is reading
a few outputs and nodding. The kit exists because four failures keep
recurring wherever AI systems get evaluated, and each one maps to a piece of
it:

1. **Gold sets built after the system.** Once you have seen the outputs, you
   write cases the system can pass. So the gold set is sealed before the
   build.
2. **Thresholds chosen after the run.** A gate picked once the scores are
   known always passes. So gates are preregistered, and the harness exits
   nonzero when one fails.
3. **Point estimates with no uncertainty.** 0.90 on 30 cases and 0.90 on
   3,000 cases are different claims. So every score ships with a confidence
   interval, per stratum.
4. **Decisions that lived in chat.** Six months later nobody can say why a
   threshold moved. So every number-driven decision goes in the decision
   log, with its evidence and date.

The full reasoning, in this repo's own log: [DECISION_LOG.md](DECISION_LOG.md).

## The maturity scale

| Level | Name | What it means |
|---|---|---|
| L1 | Vibes | No gold set. Someone reads a few outputs and says they look good. |
| L2 | Frozen gold | A hand-verified gold set, sealed before the build, stratified by case type. |
| L3 | Synthetic scale with clean gold | Programmatic cases plus AI-generated diversity, with a human-verified holdout that is never trained on. |
| L4 | Trajectory evals | Whole task trajectories scored — task success, trajectory quality, and cost as separate numbers — against pre-registered gates. |
| L5 | Living evals | Gold sets versioned and refreshed, evals running in CI, drift flagged, every change decision-logged. |

Full entry and exit criteria per level: [MATURITY.md](MATURITY.md).

The throughline at every level: freeze gold early, keep it clean, measure
with uncertainty, write the decision down.

## Quickstart

Run the toy example end to end (Python 3.10+, standard library only):

```
python eval/run_eval.py --gold example/gold.jsonl --system example/system.py --gates example/gates.yaml
python tests/check_example.py
```

You should see per-stratum scores with 95% confidence intervals and
`GATE: PASS`, exit code 0. Then change a threshold in `example/gates.yaml`
to something the system cannot meet and run again: the eval exits nonzero.
That is the point of a gate.

## Repo layout

```
eval/           the harness: run_eval.py (scoring + confidence intervals), gates.py
example/        a complete toy eval that runs: system, gold set, gates, expected output
templates/      PREREGISTRATION.md, DECISION_LOG.md, GOLD_SET.md — copy these into your project
tests/          checks that the example eval passes its gates and that gates can fail
DECISION_LOG.md this repo's own decision log, kept the way the kit prescribes
MATURITY.md     the L1–L5 scale with entry/exit criteria
```

## How to adopt

1. Use this repo as a template, or copy `eval/` and `templates/` into an
   existing project.
2. Write your gold set first, following `templates/GOLD_SET.md`. Seal it:
   after that commit, the gold set changes only through a decision-log entry.
3. Fill in `templates/PREREGISTRATION.md` — hypothesis, gates, sample size,
   judge configuration — before the first scored run.
4. Wire the eval into CI so every change runs against the frozen gold. See
   `.github/workflows/ci.yml` here for the pattern.
5. Log every decision the numbers drive in DECISION_LOG.md: decision,
   evidence, date.

## What this kit is not

- Not a benchmark. The example data is a toy 311-style classifier so the
  plumbing runs. Your gold set is your task.
- Not a judge. The default judge is exact match. `eval/run_eval.py` defines
  a judge interface so you can plug in a model judge — and the
  preregistration template makes you write down its configuration before
  you trust its scores.

## License

MIT. See [LICENSE](LICENSE).
