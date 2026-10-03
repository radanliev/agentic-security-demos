# Demo 26: Sandbox Probes

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain sandbox isolation as an escape-rate ladder over 8 probes and 3 configs
- Show that no sandbox means 8/8 escapes, a subprocess boundary still leaks 3/8, and strict isolation holds at 0/8
- Name the 3 subprocess leakers (net-egress, dns, env-read) and why process boundaries miss them
- Distinguish this teaching toy from the pending IEEE S&P 2027 study it illustrates (ACSAC 2027 as Plan B) (no data collected there yet)

## Conceptual Explanation

Execution isolation is tested with probes: each probe tries one escape
(filesystem, network, persistent state, and so on). The escape rate per
config is the isolation score.

This toy uses 8 hand-built probes over 3 configs:

| Config | Escaped | Rate | Lesson |
|--------|---------|------|--------|
| `none` | 8/8 | 1.00 | no boundary, everything escapes |
| `subprocess` | 3/8 | 0.38 | net-egress, dns, env-read still leak |
| `strict` | 0/8 | 0.00 | full isolation holds |

The subprocess row is the lesson: process boundaries stop local
escapes (filesystem, persistence) but not network and environment reads.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real sandboxes, escapes, payloads, or privileged operations
- No network access (standard library only); probes are table entries, never executed
- All probes and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real sandboxes

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 26 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=26` |

## Research Connection

This demo illustrates the design question of a pending study on agent
sandbox isolation (targeting IEEE S&P 2027 Cycle 2 as Plan A, ACSAC 2027 as Plan B). That study has **collected no
confirmatory data**; every quantity there is `[RESULT PENDING]`. Nothing here describes
a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-26-agent-sandbox-isolation-acsac` (private research repo).
Boundary: this demo is execution isolation (can code reach outside its
box); it is not network reconnaissance — that is Demo 06.
Different questions, fixtures, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Sandbox escape experiments (pending) | 8 hand-built probes × 3 configs |
| Method | Isolation harness with real boundaries | Escape-rate lookup over a JSON matrix |
| Claims | Falsifiable isolation hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Probe harness | `sandbox.py` scorer over JSON toys |
