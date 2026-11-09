# Demo 57: HE Governance Corpus Coding

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Validate codes against a closed codebook
- Compute percent agreement between two raters
- Compute Cohen's kappa and see why it is lower than raw agreement
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A corpus of institutional AI-governance documents is only as usable as its codebook. Two raters label each of six synthetic excerpts as absent, mentioned, specified or enforced. Percent agreement counts exact matches. Cohen's kappa subtracts the agreement expected if both raters used the same category frequencies by chance, so it sits below the raw rate whenever some categories are common.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 57 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=57` |

## Research Connection

This demo illustrates reliability checks for a UK higher-education AI-governance corpus. No documents have been sampled from the live frame yet; every empirical quantity in the research repository is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
