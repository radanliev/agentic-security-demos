# Demo 52: LLM Simulation Validation

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain why a calibrated simulator can still fail a held-out year or a renamed module
- Score two toy predictors on held-out pass and withdrawal rates
- Use a rename probe to catch a memorizer that recites published labels
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A simulator of a learner cohort is not validated just because it matches last year's published rates. Held-out years ask whether the same regularities appear again. A contamination probe asks whether the simulator is reciting published labels: the same module is presented under a new name. An honest predictor transfers the original module's rates; a memorizer that keys on the printed name does not.

This demo runs both checks on two hand-built predictors and four synthetic module rows. No language model is called.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 52 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=52` |

## Research Connection

This demo illustrates verification-and-validation questions for LLM multi-agent simulations of distance-learning cohorts. The measurement in the research repository is **pending**; every quantity there is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
