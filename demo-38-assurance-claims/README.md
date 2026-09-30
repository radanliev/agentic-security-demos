# Demo 38: Assurance Claims

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what coding a public claim against assurance obligations means
- Code 8 synthetic system cards against 5 obligations (threats, evals, agentic, third_party, mitigations)
- Show full coverage holds for only 3/8 cards and third-party coverage is weakest at 3/8
- Distinguish this teaching toy from the pending Journal of Cybersecurity longitudinal study it illustrates

## Conceptual Explanation

System cards make public claims; assurance asks whether each claim is backed
by a stated obligation. Coding 8 hand-built cards against 5 obligations:

| Obligation | Covered |
|------------|---------|
| threats | 7/8 |
| evals | 5/8 |
| agentic | 4/8 |
| third_party | 3/8 (weakest) |
| mitigations | 7/8 |

Only 3/8 cards cover every obligation. The lesson: third-party evaluation is
the thinnest public claim, so an assurance reader should ask for it first.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real system cards, vendors, or credentials
- No network access (standard library only)
- All cards, codings and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real cards

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 38 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=38` |

## Research Connection

This demo illustrates the design question of a longitudinal study of system
card assurance claims (targeting the Journal of Cybersecurity). That study is
**pending**; every quantity there is `[RESULT PENDING]`. Nothing here
describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-38-system-card-assurance-claims-joc` (private research repo).
It shares no topic with Demo 39 (incident taxonomy): this demo codes public
CLAIMS against obligations; Demo 39 codes incident reports into patterns.
Different sources, methods, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Longitudinal corpus of real system cards (pending) | 8 hand-built cards |
| Method | Coded content analysis over time | Single fixed coding table |
| Claims | Falsifiable coverage-trend hypotheses | **No claims** — mechanism illustration only |
| Artefact | Coding protocol with reliability checks | One tiny coverage function |
