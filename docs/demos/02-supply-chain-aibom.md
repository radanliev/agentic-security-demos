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

The policy gate section (the per-capability `ALLOW` lines for `read:files:/workspace/*`, `write:files:/workspace/output/*` and `net:http:api.internal/*` are omitted here; they appear in every scenario that includes those capabilities):

```
Declared capabilities (AIBOM): ['exec:tools:parser', 'exec:tools:validator', 'net:http:api.internal/*', 'read:files:/workspace/*', 'write:files:/workspace/output/*']
Evaluation time: 2025-01-14T12:00:00Z (fixed by the fixture for reproducibility)

=== compliant-001: System matches declared AIBOM ===
Drift detected: False
  ALLOW: exec:tools:parser (explicitly_allowed)
  ALLOW: exec:tools:validator (explicitly_allowed)
Compliant: True
✓ Matches expected: PASS

=== drifted-002: Agent gained scanner execution capability ===
Drift detected: True (undeclared: exec:tools:scanner)
  ALLOW: exec:tools:parser (explicitly_allowed)
  ALLOW: exec:tools:validator (explicitly_allowed)
  DENY: exec:tools:scanner (explicitly_denied)
Compliant: False
✓ Matches expected: BLOCKED

=== invalid-waiver-003: Waiver for shell access without approval ===
Drift detected: True (undeclared: exec:shell:*)
Waiver exec:shell:*: REJECTED: not approved; scope exec:shell:* is not waivable
  DENY: exec:shell:* (explicitly_denied)
Compliant: False
✓ Matches expected: WAIVER REJECTED

=== valid-waiver-004: Properly scoped, approved, time-limited waiver ===
Drift detected: True (undeclared: exec:tools:scanner)
Waiver exec:tools:scanner: ACCEPTED
  ALLOW: exec:tools:scanner (waiver_granted)
Compliant: True
✓ Matches expected: WAIVER ACCEPTED
```

Then the CI validator, with real exit codes:

```
Running GitHub Actions validation script (self-test: every scenario behaves as labelled)...
self-test: 4/4 scenarios behave as their expected label
Exit code: 0

Validating a compliant runtime (expect exit 0) and a drifted runtime (expect exit 1)...
compliant-001: COMPLIANT (evaluated at 2025-01-14T12:00:00+00:00)
Exit code: 0
DENY: exec:tools:scanner (explicitly_denied)
drift: undeclared capabilities ['exec:tools:scanner']
drifted-002: NON-COMPLIANT (evaluated at 2025-01-14T12:00:00+00:00)
Exit code: 1
```

The run ends by printing the results JSON, also written to `results/drift_results.json` (`"result": "pass"` is computed from the four `matches_expected` flags, not asserted).

## Drift Scenarios

| Scenario | Description | Drift | Expected |
|----------|-------------|-------|----------|
| `compliant-001` | System matches AIBOM | no | PASS |
| `drifted-002` | Extra `exec:tools:scanner` (explicitly denied) | yes | BLOCK |
| `invalid-waiver-003` | Unapproved shell access, for a scope that is not waivable | yes | REJECT WAIVER |
| `valid-waiver-004` | Approved by a named approver, scoped, 24-hour waiver | yes | ACCEPT WAIVER |

Drift (runtime capabilities the AIBOM does not declare) is reported separately from the policy verdict: `valid-waiver-004` shows `Drift detected: True` *and* `Compliant: True`. The waiver sanctions the drift; it does not erase it. Composite tool lists (`exec:tools:parser,validator`) are expanded and matched per tool, so a runtime with fewer tools than declared is not drift.

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

Decision order per capability: explicit allow → valid waiver → explicit deny → default deny (fail-closed). A specific allow such as `net:http:api.internal/*` beats the broad `net:http:*` deny because allow is checked first, not because it is more specific. A valid waiver lifts an explicit deny — but only for a scope in `allowed_scopes`, approved by a named approver, in force at the evaluation time, and no longer than `max_duration_hours`. The fixture pins `evaluation_time` (`2025-01-14T12:00:00Z`) so the 24-hour waiver in `valid-waiver-004` is judged the same way on every run.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **AIBOM** | AI Bill of Materials — declared component inventory |
| **Drift** | Runtime capabilities exceed declaration |
| **Fail-Closed** | Default deny; explicit allow only |
| **Waiver** | Time-limited, approved (by a named approver), scoped exception — makes drift compliant without erasing it |
| **Least Privilege** | Minimum capabilities for function |

## Exercises

### Beginner
1. **Add drift scenario** — Add network capability drift to `fixtures/aibom.json`

### Standard
2. **Waiver expiration** — Test edge cases (expired, expiring soon)
3. **Pattern matching** — Extend per-tool expansion (`expand_capability`) to host lists such as `net:http:a.internal,b.internal`

### Extension
4. **JSON results** — Generate reproducible drift detection reports
5. **GitHub Actions** — Wire `validate_aibom.py --runtime observed.json` into a CI workflow that fails on exit 1 (the repository does not ship one)

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/aibom.json` | AIBOM, policy, pinned `evaluation_time`, drift scenarios |
| `student/policy_gate.py` | Fail-closed policy evaluation; drift reported separately from compliance |
| `student/validate_aibom.py` | GitHub Actions compatible validator (`--scenario ID`, `--runtime observed.json`, `--self-test`, `--now`) |
| `student/generate_results.py` | Writes `results/drift_results.json` with computed outcomes |
| `tests/test_aibom_drift.py` | 17 tests covering all concepts |

## Running Tests

```bash
cd demo-02-supply-chain-aibom
make test
# Or from root:
make test DEMO=02
```

## CI Integration

The repository ships no AIBOM workflow: `.github/workflows/ci.yml` only runs this demo's tests (`make test`) and, in its reproducibility job, `make demo`. The validator is built to be dropped into one — it judges a single observed runtime capability set and exits by compliance:

```bash
cd demo-02-supply-chain-aibom
python3 student/validate_aibom.py --scenario compliant-001; echo "exit code: $?"   # 0
python3 student/validate_aibom.py --scenario drifted-002; echo "exit code: $?"     # 1
python3 student/validate_aibom.py --runtime observed.json                          # {"runtime_capabilities": [...], "waiver": {...}}
python3 student/validate_aibom.py --self-test                                      # every fixture scenario behaves as its expected label
# Exit codes: 0 = compliant, 1 = non-compliant, 2 = error
# The clock defaults to the fixture's evaluation_time; --now now uses the real clock
# (against which the 2025 waiver in valid-waiver-004 has lapsed: exit 1).
```

---

*Next: [Demo 03: Evaluation Invariants](../demos/03-eval-invariants.md)*