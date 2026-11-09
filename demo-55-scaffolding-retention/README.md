# Demo 55: Scaffolding Retention Power

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Separate an immediate performance difference from a residual (retention) difference
- Compute two-sample power from n, sd and a planned difference, with no live data
- See that the same sample size can be well powered for a large immediate effect and weak for a smaller residual
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A two-arm study that compares generative-AI scaffolding against a control can show a large immediate difference and a much smaller difference once the scaffold is removed. Power is not a single number: it depends on which difference the study claims to detect. This demo uses the usual normal approximation for two equal arms and a fixed standard deviation, on a hand-built plan (n = 40 per arm, sd = 1, differences 0.4 and 0.15). No participant data are present.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 55 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=55` |

## Research Connection

This demo illustrates the sample-size question for a generative-AI scaffolding retention trial. The trial itself has not been run; every empirical quantity in the research repository is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
