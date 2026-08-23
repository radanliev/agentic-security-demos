# Demo 10: ScanBound

## Learning Objectives

- Constrain autonomous vulnerability assessment to approved scope
- Validate targets against host/port allowlists
- Parse scanner output with taint tracking
- Reject dangerous checks via AST/structured validation
- Enforce fail-closed downstream action policies

## Conceptual Explanation

An autonomous vulnerability scanner can:
- **Escape scope** — Scan unauthorized hosts/ports
- **Trust poisoned output** — Scanner XML/JSON contains injected commands
- **Execute unsafe checks** — Checks that modify state or exploit vulns

### The Solution

**ScanBound** enforces:
1. **Explicit target scope** — Allowlists only
2. **Check validation** — Reject unsafe checks via AST
3. **Taint tracking** — Scanner output is untrusted
4. **Action policy** — Fail-closed downstream actions

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No public scanning** — localhost Docker lab or mock services only
- No exploit chains, credential attacks, stealth techniques
- No bypassing security controls
- Clear separation from real penetration testing

## Running the Demo

```bash
make demo DEMO=10
```

### Expected Output

```
--- Unconstrained Baseline ---
  check_001 (localhost:8080): Server: Apache... (taint: low)
  check_004 (127.0.0.1:8443): Command blocked... (taint: low)  ← WRONG!

--- Scope-Bound Guarded ---
  check_001 (localhost:8080): Server: Apache... (taint: high)  ← Injection detected!
  check_003 (localhost:8080): BLOCKED (check_type_unsafe)
  check_004 (127.0.0.1:8443): BLOCKED (check_type_unsafe)
  check_005 (127.0.0.1:8443): Cert valid... (taint: medium)
```

## Target Scope

```json
{
  "allowed_hosts": ["localhost", "127.0.0.1", "scan-target.local"],
  "allowed_ports": [80, 443, 8080, 8443],
  "allowed_protocols": ["http", "https"]
}
```

## Scanner Checks

| Check | Type | Target | Payload | Modifies State? |
|-------|------|--------|---------|-----------------|
| `check_001` | Safe | localhost:8080 | `GET /server-info` | No |
| `check_002` | Safe | scan-target.local:80 | `<script>alert(1)</script>` | No |
| `check_003` | **Unsafe** | localhost:8080 | `' OR '1'='1` | **Yes** |
| `check_004` | **Unsafe** | 127.0.0.1:8443 | `; rm -rf /` | **Yes** |
| `check_005` | Safe | 127.0.0.1:8443 | TLS handshake | No |

## Poisoned Scanner Output

| Check | Injected Canary |
|-------|-----------------|
| `check_001` | `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI` |
| `check_004` | `CANARY_SCANNER_INJECTION_EXFILTRATE_KEYS` |

## Check Validation (AST)

```python
# Detects dangerous patterns:
- exec(), eval(), __import__()
- subprocess.run, os.system
- os.write, os.remove, shutil.rmtree
- Dangerous keywords: rm -rf, exploit, exfiltrate
```

## Taint Levels

| Taint | Sources | Action Policy |
|-------|---------|------------------|
| `LOW` | Trusted, verified | ✅ All allowed actions |
| `MEDIUM` | Clean scanner output | ⚠️ Report only |
| `HIGH` | Injection canaries, credentials | ❌ Block all actions |

## Exercises

### Beginner
1. **Scope escape** — Demonstrate and fix scope escape

### Standard
2. **Poisoned output** — Handle poisoned scanner output
3. **Unsafe check AST** — Extend AST validation

### Extension
4. **Address validation** — Add DNS resolution validation
5. **Fail-closed** — Verify fail-closed on validator error

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/scanbound.json` | Scope, checks, poisoned output, policy |
| `student/scanbound.py` | Validators, trackers, scanners, policy |
| `student/generate_scan_results.py` | Results generator |
| `tests/test_scanbound.py` | 21 tests |

---

*This completes all 10 demos!*