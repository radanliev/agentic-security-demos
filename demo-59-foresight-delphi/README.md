# Demo 59: Provenance-labelled Foresight

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Summarise a small panel with the median and inter-quartile range
- Flag consensus when the IQR is at most 1.5 on a 1-7 scale
- Keep every summary attached to the briefing hash the (synthetic) panellists saw
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A Delphi round that opens with a dated briefing should store every rating with the hash of that briefing. This demo summarises two synthetic propositions: P1 is tightly grouped around 6 and meets the IQR <= 1.5 consensus rule; P2 is split by a single 7 among otherwise low ratings, so it does not. No panellists were recruited.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real students, patients, institutions, credentials, or API keys
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 59 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=59` |

## Research Connection

This demo illustrates the summary layer of a provenance-labelled Delphi. No panel has been recruited and no ethics application has been filed; every empirical quantity in the research repository is `[RESULT PENDING]`.

Nothing here describes a publication, a venue result, or a measured effect size.
