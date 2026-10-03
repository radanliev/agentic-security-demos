# Demo 29: Provenance Graphs

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what an agent action provenance graph is (nodes are actions, edges are cause links, roots need authority)
- Reconstruct attribution over six synthetic actions and flag the orphan with no cause
- Show a sha256 chain over ordered records verifies cleanly but breaks when a copy is tampered
- Distinguish post-incident reconstruction from release assurance (Demo 05)

## Conceptual Explanation

After an incident, investigators rebuild who caused what: each action should
point at its cause, back to a trusted root. One orphan with a null cause that
is not the root cannot be attributed — here `a5`, so attribution is 5/6.

A separate integrity layer chains the ordered records with sha256. The clean
chain verifies; a copy with one edited authority field fails verification.

| Check | Result |
|-------|--------|
| Attributable | 5/6 (unattributable: a5) |
| Chain over clean records | verified |
| Chain over tampered copy | tamper detected |

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real incidents, logs, models, or credentials
- No network access (standard library only)
- All actions, authorities and hashes are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real forensics

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 29 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=29` |

## Research Connection

This demo illustrates the reconstruction question of a pending AgentForensics
study targeting IEEE S&P 2027 Cycle 2 (Plan A; IEEE TIFS as Plan B). That study has **collected no confirmatory data**;
every quantity there is `[RESULT PENDING]`. Nothing here describes a
publication, a venue result, or a measured effect size. Boundary: this demo is
post-incident reconstruction, not release assurance (Demo 05).

Provenance: distilled from `demo-29-agent-forensics-provenance-tifs` (private research repo).

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Agent execution traces (pending) | 6 hand-built actions |
| Method | Provenance graph recovery + integrity checks | Cause-link partition + sha256 chain over ordered records |
| Claims | Falsifiable attribution hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Forensic reconstruction toolkit | Two tiny provenance helpers |
