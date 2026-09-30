# Demo 19: Lineage Risk

> **New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain inherited supply-chain risk (a clean child of a flagged parent is still risky)
- Classify 8 synthetic models by own flags vs inherited risk
- Show 6/8 risky: 1 origin, 2 introduced, 3 inherited
- Distinguish this teaching toy from the preregistered ICSE study it illustrates (no data collected there yet)

## Conceptual Explanation

Models derive from parents: fine-tunes, merges, re-uploads. A pickled parent,
a remote-code parent, or a licence problem flows downhill even when the child
looks clean.

This toy uses 8 hand-built models:

| Model | Parent | Own flags | Verdict |
|-------|--------|-----------|---------|
| A | none | clean | safe |
| B | none | pickle | origin (risky) |
| a1 | A | clean | safe |
| a2 | A | remote code | introduced (risky) |
| b1 | B | clean | inherited (risky) |
| b2 | B | clean | inherited (risky) |
| c1 | a2 | clean | inherited (risky) |
| c2 | a1 | licence problem | introduced (risky) |

Risky total: 6/8 (B, a2, b1, b2, c1, c2); inherited 3 (b1, b2, c1);
introduced 2 (a2, c2); origin 1 (B).

## Safety Notice

WARNING: **This is a teaching demonstration using synthetic fixtures only.**
- No real model hub data, weights, models, or credentials
- No network access (standard library only)
- All models, flags and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real hubs

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 19 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `python3 student/run_lineage.py` |

## Research Connection

This demo illustrates the design question of a preregistered study on model
lineage inherited risk (targeting ICSE 2028, Hub lineage corpus). That study has
**collected no confirmatory data**; every quantity there is `[RESULT PENDING]`.
Nothing here describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-19-model-lineage-inherited-risk-icse` (private research repo).
Boundary: this demo is weight-supply-chain inheritance; it is not model-card
disclosure analysis (Demo 36). Different question, data, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Hub lineage corpus (pending) | 8 hand-built models |
| Method | Lineage-wide risk propagation measurement | Depth-ordered flag inheritance |
| Claims | Falsifiable inheritance hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Lineage risk scanner | One tiny classifier module |
