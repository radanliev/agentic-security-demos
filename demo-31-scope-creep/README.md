# Demo 31: Integration Scope Creep

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain scope creep (an integration requests strictly more OAuth scopes than it uses)
- Flag 5/8 synthetic integrations as over-privileged with a strict-superset rule
- Compute the least-privilege set as the sorted union of used scopes
- Distinguish OAuth scopes from capability classes (Demo 21) and delegation properties (Demo 24)

## Conceptual Explanation

Agent integrations often copy broad scope lists. This toy checks eight
hand-built integrations: over-privileged when `set(requested)` strictly
supersets `set(used)`.

| Check | Result |
|-------|--------|
| Over-privileged | 5/8 (i1, i4, i5, i6, i8) |
| Tight (equal) | 3/8 (i2, i3, i7) |
| Least-privilege | 8 scopes (union of all used) |

Equal requests such as `i2` (`read`/`read`) are tight; `i8` requesting
`drive.admin` it never uses is the classic creep case.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real providers, tokens, or credentials
- No network access (standard library only)
- All integrations and scopes are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real integrations

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 31 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=31` |

## Research Connection

This demo illustrates the measurement question of a pending study of agent
integration privileges targeting ACM TOPS. That study has **collected no
confirmatory data**; every quantity there is `[RESULT PENDING]`. Nothing here
describes a publication, a venue result, or a measured effect size. Boundary:
this demo covers OAuth scopes only, not capability classes (Demo 21) nor
delegation properties (Demo 24).

Provenance: distilled from `demo-31-agent-integration-scope-creep-tops` (private research repo).

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Integration manifests (pending) | 8 hand-built integrations |
| Method | Scope-use gap measurement | Strict-superset check + union of used |
| Claims | Falsifiable over-privilege hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Manifest analyser | Two tiny scope helpers |
