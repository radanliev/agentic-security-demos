# Demo 40: Corpus Union

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what a corpus union is (merge sources, dedupe, licence-gate)
- Normalise 12 synthetic records (lowercase + strip) and dedupe by SHA-256 to 9 unique texts
- Apply a licence gate (permissive + by-sa only) releasing 7/9 records
- Distinguish corpus INFRASTRUCTURE (this toy) from any measurement claim

## Conceptual Explanation

Sharing a security corpus means answering two questions: what is duplicated,
and what may be released? On 12 hand-built records from sources A/B/C:

| Stage | Count |
|-------|-------|
| Ingested records | 12 |
| Unique after SHA-256 dedupe | 9 (3 cross-source duplicates removed) |
| Releasable (permissive + by-sa) | 7/9 |
| Blocked | r07 (noncommercial), r08 (unlicensed) |

The lesson: dedupe decides what the corpus *is*; the licence gate decides
what it may *become*. Neither step says anything about the world outside the
fixture.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real datasets, licences, or credentials
- No network access (standard library only)
- All records, texts and verdicts are hand-built toys
- Nothing is deposited anywhere; results are not evidence about real corpora

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 40 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=40` |

## Research Connection

This demo illustrates the infrastructure design for a data-descriptor
deposit (targeting Scientific Data). That deposit is **pending — nothing has
been deposited**. Nothing here describes a publication, a venue result, or a
measured effect size.

Provenance: distilled from `demo-40-agentsec-corpus-scidata` (private research repo).
This demo is corpus INFRASTRUCTURE, not a measurement: it builds a releasable
record set rather than estimating any quantity about agent security.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Multi-source corpus deposit (pending) | 12 hand-built records |
| Method | Dedupe + licence review pipeline | Normalise, SHA-256, allowlist |
| Claims | Reusability documentation, no effects | **No claims** — mechanism illustration only |
| Artefact | Deposit candidate pipeline | Three tiny corpus functions |
