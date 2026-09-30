# Demo 28: Memory Poisoning

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain memory-integrity poisoning: planted instructions inside stored entries that steer later behaviour
- Run the MemScope auditor over 8 synthetic entries and confirm it flags exactly the 3 poisoned ones with 0 false positives
- State the auditor's limits: literal case-insensitive patterns only, no semantic detection
- Distinguish this teaching toy from the pending DEF CON talk it illustrates (no data collected there yet)

## Conceptual Explanation

Stored memory is an integrity surface: an entry reading "ignore previous
instructions …" can steer the agent long after it was written. Auditing
means scanning stored entries for known instruction patterns.

This toy uses 8 hand-built entries:

| Entries | Verdict | Lesson |
|---------|---------|--------|
| `e2`, `e4`, `e6` | POISONED (3/8) | each carries one literal pattern |
| `e1`, `e3`, `e5`, `e7`, `e8` | benign (5/8) | everyday notes, never flagged |

The auditor is a literal case-insensitive substring match over three
patterns — a stand-in for a real audit tool, not one.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real memory stores, prompts, exfiltration, or credentials
- No network access (standard library only)
- All entries and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real memory systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 28 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=28` |

## Research Connection

This demo illustrates the MemScope audit tooling prepared for a pending
DEF CON 35 talk on agent memory poisoning. That work has **collected no
confirmatory data**; every quantity there is `[RESULT PENDING]`. Nothing here describes
a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-28-agent-memory-poisoning-defcon` (private research repo).
Boundary: this demo is memory INTEGRITY (attack entries plus an audit
tool); the sibling Demo 22 is memory PRIVACY (leakage: retention,
resurfacing, erasure). Different failure modes, fixtures, and checks.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Poisoned memory-store cases (pending) | 8 hand-built entries |
| Method | MemScope audit tooling plus live talk demo | Literal substring match over 3 patterns |
| Claims | Tool capability claims to be shown live | **No claims** — mechanism illustration only |
| Artefact | MemScope auditor | `memascope.py` matcher over JSON toys |
