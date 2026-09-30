# Demo 39: Incident Taxonomy

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what a practitioner incident taxonomy is (patterns mapped to controls)
- Tally 10 synthetic incidents into 4 attack patterns with prompt-injection on top at 4/10
- Show a static 10-item control catalogue with 7/10 entries supported
- Distinguish this practitioner guidance toy from any research claim

## Conceptual Explanation

Practitioners turn incident reports into counts: which pattern recurs, and
which controls already cover it? On 10 hand-built incident sketches:

| Pattern | Count |
|---------|-------|
| prompt-injection | 4/10 (top) |
| tool-misuse | 3/10 |
| data-exfiltration | 2/10 |
| privilege-escalation | 1/10 |

The static control catalogue (input sanitisation, allowlists, provenance
labelling, human approval, egress filtering, memory gating, audit logging)
supports 7/10 entries; cross-agent attestation, hardware-backed identity and
formal verification are marked unsupported. The lesson is deliberately thin:
counts guide where to look first, nothing more.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real incidents, victims, or credentials
- No network access (standard library only)
- All incidents, patterns and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real incidents

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 39 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=39` |

## Research Connection

This demo is written as a magazine-style practitioner guidance piece
(targeting IEEE S&P Magazine). It makes **no research claims** — it reports
counts over synthetic sketches only, with no hypotheses and no confirmatory
data.

Provenance: distilled from `demo-39-ai-incidents-practitioner-taxonomy-spmag` (private research repo).
It shares no topic with Demo 38 (assurance coding): this demo is practitioner
guidance from incident counts; Demo 38 codes public assurance claims.
Different sources, methods, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Practitioner incident corpus (counts only) | 10 hand-built sketches |
| Method | Pattern coding with control mapping | Single fixed tally |
| Claims | None — guidance, not research | **No claims** — mechanism illustration only |
| Artefact | Taxonomy table for practitioners | Two tiny tally functions |
