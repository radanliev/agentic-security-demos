# Demo 58: Education Work AI Exposure

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Average published-style exposure labels within an occupation
- Roll those means up to a work family
- Report the share of tasks that would require an AI system to act rather than write
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Occupational exposure scores summarise how far a role's tasks overlap with what language models can write or do. This demo takes three synthetic higher-education roles, each with two tasks, and reports the mean exposure per role, the mean per work family, and the share of tasks tagged as agentic (the system would have to act, not just draft).

Exposure is not a forecast of job loss. The numbers are hand-built.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 58 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=58` |

## Research Connection

This demo illustrates the measurement layout for a task-level exposure study of higher- and distance-education work. No O*NET release has been joined yet; every empirical quantity in the research repository is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
