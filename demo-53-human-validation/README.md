# Demo 53: Human Validation of Agent Outputs

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain why an unchecked agent output is not a validated result
- Compute the share of planted errors that a declared sample would catch
- Estimate an error rate from the audited sample only
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Agent pipelines can write more outputs than any person can check. A protocol therefore samples which items to inspect, plants known errors so the checker is tested, and reports how many of those planted errors the sample would have caught. Coverage here is planted-in-sample divided by planted-total; the sample error rate is the share of sampled items that carry a planted error.

The eight items and the four-item sample are hand-built. No live agent is queried.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 53 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=53` |

## Research Connection

This demo illustrates a sampled, provenance-aware validation protocol for agent-produced research outputs. The measurement in the research repository is **pending**; every quantity there is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
