# Demo 22: Agent Memory Leakage

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain the three memory-privacy failure modes: persisting high-sensitivity content, resurfacing entries across sessions/users, and failing to honour deletion
- Run a tiny leakage screen over 8 synthetic memory entries and read its counts
- Distinguish memory PRIVACY (leakage: what is kept, reshown, or not erased) from memory INTEGRITY (poisoning: what is planted), the topic of the sibling Demo 28
- Distinguish this teaching toy from the pending PoPETs study it illustrates (no data collected there yet)

## Conceptual Explanation

Agents with persistent memory can leak in three quiet ways: they store
content they should not keep, they resurface one session's content in
another session or user, and they keep content the user asked to delete.

This toy uses 8 hand-built entries:

| Check | Result | Lesson |
|-------|--------|--------|
| Persists high-sensitivity (`m1`, `m2`) | 2 | high-sensitivity content should never persist |
| Resurfaces across sessions (`m3`, `m4`) | 2 | entries reappear under another session/user |
| Erasure failures (`m7` of 3 deleted) | 1/3 | deletion is requested but the entry stays |

Entries `m5`/`m6` are the contrast: deleted and actually gone.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real memory stores, users, sessions, or personal data
- No network access (standard library only)
- All entries and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real memory systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 22 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=22` |

## Research Connection

This demo illustrates the design question of a pending study on agent
memory leakage (targeting PoPETs 2027). That study has **collected no
confirmatory data**; every quantity there is `[RESULT PENDING]`. Nothing here describes
a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-22-agent-memory-leakage-pets` (private research repo).
Boundary: this demo is memory PRIVACY (leakage: retention, resurfacing,
erasure); the sibling Demo 28 is memory INTEGRITY (poisoning: planted
instructions and audit). Different failure modes, fixtures, and checks.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Agent memory-store observations (pending) | 8 hand-built entries |
| Method | Privacy measurement across sessions/users | Three tiny predicates |
| Claims | Falsifiable leakage hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Leakage screen over real stores | `memory.py` predicates over JSON toys |
