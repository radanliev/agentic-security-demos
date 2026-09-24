# Demo 13: Typed Commitments & Coverage Cues

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

<p align="center">
  <img src="https://img.shields.io/badge/Teaching%20demo-Synthetic%20only-blue?style=flat-square" alt="Teaching demo">
  <img src="https://img.shields.io/badge/Python-Stdlib%20only-blue?style=flat-square" alt="Standard library only">
  <img src="https://img.shields.io/badge/Network-Offline%20only-success?style=flat-square" alt="Offline only">
</p>

## Learning Objectives

- Explain what a derived coverage cue is (a static-analysis pointer, triage ranking, or owners file telling an assessor where to look)
- Show how a shared wrong input makes two assessors fail *together*, so their agreement stays high while both are wrong
- Implement a miniature agreement gate and read its pass/fail table sceptically
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Security pipelines often hand LLM assessors a **derived artefact** saying where to look. Nobody checks where that artefact came from. Two questions follow:

1. Does a well-formed but **wrong** cue degrade localisation?
2. Does that degradation **escape agreement-based redundancy** — the gate that passes work only when assessors agree?

This toy demonstrates the second question's mechanism on six synthetic instances. Two toy assessors (a cue-follower and a cue-ignoring heuristic) nominate one file each; the agreement gate passes instances where they agree:

| Cue level | Follower | Independent | Agreed |
|-----------|----------|-------------|--------|
| none (×2) | 2/2 | 2/2 | 2/2 |
| true (×2) | 2/2 | 0/2 | 0/2 |
| wrong (×2) | 0/2 | 1/2 | 1/2 |
| **total (×6)** | **4/6** | **3/6** | **3/6, of which 1 wrong** |

Instance `cue-wrong-02` is the lesson: both assessors nominate the same wrong file, so the gate **passes a wrong answer 1/3 of the time it passes anything**. Agreement measures shared input more than shared correctness.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real repositories, credentials, or API keys
- No network access (standard library only)
- All instances, cues and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real assessors

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 13 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=13` |

## Research Connection

This demo illustrates the design question of a preregistered study on typed pre-reveal commitments and coverage-cue provenance (targeting USENIX Security 2027 Cycle 2). That study has **collected no confirmatory data**; its preregistration is a draft. Nothing here describes a publication, a venue result, or a measured effect size.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Parent-study instruments, six model configurations (pending) | 6 hand-built instances |
| Assessors | LLM assessors under preregistered protocol | Two deterministic toy rules |
| Claims | Falsifiable hypotheses with equivalence margins | **No claims** — mechanism illustration only |
| Cues | Constructed per-instance cue levels | Hard-coded cue labels in fixtures |
