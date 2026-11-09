# Demo 56: Learning Performance Meta-analysis

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Compute an inverse-variance weighted mean
- See that a more precise study pulls the mean more than a noisier one
- Read Cochran Q as a heterogeneity check, not as a quality badge
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A meta-analysis does not average published headlines. Each synthetic study contributes an effect `yi` and a variance `vi`; the fixed-effect mean weights each row by `1/vi`, so a precise row moves the mean more than a noisy one. Cochran Q asks whether the rows scatter more than that weighting would expect.

The four rows are hand-built. They are not taken from any paper, and the mean is not a literature estimate.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 56 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=56` |

## Research Connection

This demo illustrates the estimator that a systematic review of generative-AI effects on learning performance would use. No studies have been coded yet; every empirical quantity in the research repository is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
