# Demo 47: Pre-reveal Seal

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Hash a localisation commitment before any ground truth is read
- Chain each seal to the previous seal
- Refuse a commitment whose bytes no longer match the seal

## Conceptual Explanation

A blind evaluation writes the guessed defect id first, seals those bytes, and
only then opens the answer key. On three hand-built cases:

| Case | What happens | Verdict |
|------|----------------|---------|
| hit | sealed guess matches the key | hit |
| miss | sealed guess names a different component | miss |
| edited | bytes change after the seal, even if the new text would match the key | commitment_hash_mismatch |

The lesson: a later edit is not a new answer. Scoring never consults the key
until the sealed digest still matches.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real vulnerabilities, systems, or credentials
- No network access (standard library only)
- All cases and verdicts are hand-built toys

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | none (no randomness) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=47` |

## Research Connection

This demo illustrates seal-before-reveal for a localisation commitment.
That study is **pending**. Nothing here describes a publication or a measured effect size.

Provenance: distilled from `demo-47-blind-verification-eval-sais` (private research repo).
The exercise is the seal, the chain link, and the rule that the answer key stays closed
until the digest matches.
