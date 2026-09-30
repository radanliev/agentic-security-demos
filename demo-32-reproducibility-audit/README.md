# Demo 32: Reproducibility Audit

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what a reproducibility audit checks (code, data, and whether the claim reproduces)
- Audit ten synthetic papers: 6/10 share code+data, 4/10 reproduce
- Verify the invariant that reproducing implies sharing code+data
- Distinguish auditing the field from making new attack claims

## Conceptual Explanation

Surveys of agent security report many defences with few shared artefacts.
This toy audits ten hand-built papers across four channels (content, tool,
memory, multiagent).

| Check | Result |
|-------|--------|
| Code+data | 6/10 |
| Reproduces | 4/10 |
| Invariant | every reproducing paper shares code+data |

Per-channel reproduction: content 2/3, tool 1/3, memory 1/2, multiagent 0/2.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real papers, benchmarks, models, or credentials
- No network access (standard library only)
- All papers and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about the field

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 32 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=32` |

## Research Connection

This demo illustrates the audit question of a pending survey of agent
security targeting ACM CSUR. That survey has **collected no confirmatory
data**; every quantity there is `[RESULT PENDING]`. Nothing here describes a
publication, a venue result, or a measured effect size. Boundary: this demo
is an audit of the field, with no new attack claims.

Provenance: distilled from `demo-32-agent-security-sok-reproducibility-csur` (private research repo).

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Published papers and artefacts (pending) | 10 hand-built papers |
| Method | Survey coding + reproduction checks | Count code+data and reproduces by channel |
| Claims | Falsifiable audit hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Coding guide + audit dataset | One tiny audit module |
