# Demo 02: Supply Chain AIBOM Drift

## Learning Objectives

- Understand AI Bill of Materials (AIBOM) and component inventory concepts
- Detect when agent permissions drift from declared capabilities
- Implement fail-closed policy gates
- Design waiver mechanisms with expiration and justification

## Conceptual Explanation

An **AIBOM (AI Bill of Materials)** declares what components, models, tools, and permissions an agentic system uses. **Drift** occurs when the running system exceeds or deviates from this declaration.

### The Workflow

1. **Declared Inventory** — What the system claims to use
2. **Runtime Observation** — What the system actually uses
3. **Policy Gate** — Automated check that blocks drift
4. **Waiver Process** — Controlled, time-limited exceptions

## Safety Notice

⚠️ **Teaching demonstration only.**
- Synthetic package names (e.g., `secure-parser-123`)
- No real dependencies, registries, or credentials
- Local validation only — no cluster required

## Running the Demo

```bash
make demo DEMO=02
```

### Expected Output

```
=== Drift Scenario: compliant-001 ===
System matches declared AIBOM
Compliant: True

=== Drift Scenario: drifted-002 ===
Agent gained scanner execution capability
Compliant: False
DENY: exec:tools:parser,validator,scanner (not_allowed_default_deny)

=== Drift Scenario: invalid-waiver-003 ===
Waiver for shell access without approval
Compliant: False
DENY: exec:shell:* (explicitly_denied)

=== Drift Scenario: valid-waiver-004 ===
Properly scoped, approved, time-limited waiver
Compliant: True
ALLOW: exec:tools:scanner (waiver_granted)
```

## Drift Scenarios

| Scenario | Description | Expected |
|----------|-------------|----------|
| `compliant-001` | System matches AIBOM | PASS |
| `drifted-002` | Extra `exec:tools:scanner` | BLOCK |
| `invalid-waiver-003` | Unapproved shell access | REJECT WAIVER |
| `valid-waiver-004` | Approved, scoped, time-limited | ACCEPT WAIVER |

## Policy Structure

```json
{
  "allowed_capabilities": [
    "read:files:/workspace/*",
    "write:files:/workspace/output/*",
    "exec:tools:parser,validator",
    "net:http:api.internal/*"
  ],
  "denied_capabilities": [
    "exec:tools:scanner",
    "net:http:*",
    "write:files:/etc/*",
    "exec:shell:*"
  ],
  "waiver_rules": {
    "max_duration_hours": 24,
    "requires_approval": true,
    "allowed_scopes": ["exec:tools:scanner", "net:http:specific.host"]
  }
}
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **AIBOM** | AI Bill of Materials — declared component inventory |
| **Drift** | Runtime capabilities exceed declaration |
| **Fail-Closed** | Default deny; explicit allow only |
| **Waiver** | Time-limited, approved exception |
| **Least Privilege** | Minimum capabilities for function |

## Exercises

### Beginner
1. **Add drift scenario** — Add network capability drift to `fixtures/aibom.json`

### Standard
2. **Waiver expiration** — Test edge cases (expired, expiring soon)
3. **Pattern matching** — Extend wildcard capability matching

### Extension
4. **JSON results** — Generate reproducible drift detection reports
5. **GitHub Actions** — Implement `validate_aibom.py` for CI/CD

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/aibom.json` | AIBOM, policy, drift scenarios |
| `student/policy_gate.py` | Fail-closed policy evaluation |
| `student/validate_aibom.py` | GitHub Actions compatible validator |
| `tests/test_aibom_drift.py` | 12 tests covering all concepts |

## Running Tests

```bash
cd demo-02-supply-chain-aibom
make test
# Or from root:
make test DEMO=02
```

## CI Integration

```yaml
# .github/workflows/aibom-check.yml
- name: Validate AIBOM
  run: |
    cd demo-02-supply-chain-aibom
    python student/validate_aibom.py
# Exit codes: 0=compliant, 1=drift, 2=error
```

---

*Next: [Demo 03: Evaluation Invariants](../demos/03-eval-invariants.md)*