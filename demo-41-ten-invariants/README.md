# Demo 41: Ten Invariants

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what a security invariant checklist is (properties every deployment should hold)
- Evaluate 10 synthetic invariant checks: 7 hold, 3 are violated
- Name the violated three: provenance-travels, memory-gated, reconstructable
- Apply the synthesis rule: no invariant without accepted evidence (all evidence here is synthetic)

## Conceptual Explanation

A checklist turns scattered guidance into testable properties. On 10
hand-built checks, 7 hold (authority-bound, typed-commitments, action-gated,
scan-bound, eval-pinned, human-approval, artifact-bom) and 3 fail:

| Violated invariant | Meaning |
|--------------------|---------|
| provenance-travels | Labels do not follow data across tool hops |
| memory-gated | Memory reads ignore the current task context |
| reconstructable | Incidents cannot be rebuilt from logs |

The lesson is the synthesis rule: an invariant earns its place only with
accepted evidence behind it — and every verdict here is backed solely by a
synthetic fixture, so none qualifies.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real deployments, audits, or credentials
- No network access (standard library only)
- All checks and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real systems

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 41 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=41` |

## Research Connection

This demo illustrates a synthesis argument about agent-security invariants
(targeting CACM). It contributes **checklist synthesis, not new evidence**:
every invariant stated here rests on synthetic checks only.

Provenance: distilled from `demo-41-agent-security-invariants-cacm` (private research repo).
The synthesis rule applies throughout: no invariant without accepted
evidence — and all evidence in this demo is synthetic, so the checklist
illustrates the form of the argument without making it.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Survey of accepted evidence (pending) | 10 hand-built checks |
| Method | Evidence-backed synthesis | Single fixed checklist |
| Claims | Candidate invariant set with stated rule | **No claims** — mechanism illustration only |
| Artefact | Synthesis with evidence table | One tiny evaluate function |
