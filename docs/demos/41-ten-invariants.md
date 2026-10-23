# Demo 41: Ten Invariants

## Learning Objectives

- Explain what a security invariant checklist is (properties every deployment should hold)
- Evaluate 10 synthetic invariant checks: 7 hold, 3 are violated
- Name the violated three: provenance-travels, memory-gated, reconstructable
- Apply the synthesis rule: no invariant without accepted evidence (all evidence here is synthetic)

## Conceptual Explanation

A checklist turns scattered guidance into testable properties. On 10 hand-built checks, 7 hold (authority-bound, typed-commitments, action-gated, scan-bound, eval-pinned, human-approval, artifact-bom) and 3 fail:

| Violated invariant | Meaning |
|--------------------|---------|
| provenance-travels | Labels do not follow data across tool hops |
| memory-gated | Memory reads ignore the current task context |
| reconstructable | Incidents cannot be rebuilt from logs |

The lesson is the synthesis rule: an invariant earns its place only with accepted evidence behind it — and every verdict here is backed solely by a synthetic fixture, so none qualifies.

Boundary: this demo is checklist synthesis, not new evidence; each invariant connects to a dedicated demo (authority: Demo 04, gating: Demo 14, provenance: Demo 29). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real deployments, audits, or credentials
- No network access (standard library only)
- All checks and verdicts are hand-built toys

## Run It

```bash
cd demo-41-ten-invariants
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_inv.py           # writes results/invariants.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-41-ten-invariants/INSTRUCTIONS.md).
