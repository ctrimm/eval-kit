# Preregistration — <eval name>

Filled in BEFORE the first scored run. If it is not written here, it was not
pre-registered, and the run is exploratory — say so when you report it.

- **Date:**
- **Author:**
- **System under test:** (name, and version or commit hash)

## Hypothesis

One or two sentences, stated so they can be wrong. "The new extractor will
beat the baseline on the `edge` stratum by at least 5 points without
regressing `routine`" is a hypothesis. "The new extractor is better" is not.

## Gold set

- **File:**
- **Version / commit hash of the sealed set:**
- **Size:** (total, and per stratum)
- **How cases were verified:** (who checked the expected outputs, and how)
- **Holdout statement:** which subset is human-verified holdout, and
  confirmation it has not been trained or tuned against.

## Gates

A gate is a number the run must clear, written down before the run. Every
gate needs a rationale: why this number, and what happens if it fails.

| Metric | Threshold | Rationale |
|---|---|---|
| overall accuracy | | |
| stratum: <name> | | |
| cost per task | | |

## Sample size and uncertainty

- **n per stratum:**
- **Interval method:** Wilson score interval (the harness default).
- **Smallest difference worth detecting:** and the n that implies.

## Judge configuration

- **Judge type:** exact match / model judge (delete one)
- **If model judge:** model name and version, prompt (link or hash),
  temperature and other settings.
- **Judge spot-check:** who re-scores a sample of judged cases by hand, how
  many, and how often.

## Stop rules

What result would make you stop, revert, or not ship? Write it now, while
stopping is still cheap.

## Deviations

(Filled in after the run.) Anything that differed from this document, and
why. An honest deviations section is worth more than a clean run.
