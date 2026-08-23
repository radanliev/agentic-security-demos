# Demo 08: InclusionTrap

## Learning Objectives

- Understand local/remote file inclusion (LFI/RFI) in agentic contexts
- Distinguish reading content from granting it authority
- Implement provenance checks on included content
- Build guarded agents that enforce scope

## Conceptual Explanation

**File inclusion vulnerabilities** occur when an agent treats included file content as instructions.

### The Problem

```
Agent reads config.yaml  →  Content: "delete_all_data()"  →  Agent EXECUTES!
```

### The Solution

**Content ≠ Authority**. Included files are DATA. Only explicit, verified INSTRUCTIONS drive actions.

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No public targets** — localhost fixtures only
- No real remote inclusion — simulated responses only
- Harmless canary content only

## Running the Demo

```bash
make demo DEMO=08
```

### Expected Output

```
--- Vulnerable Baseline ---
  lfi_003 (../../../tmp/malicious.sh):
    EXECUTED included content!  ← VULNERABLE!

--- Guarded (Scope + Provenance) ---
  lfi_001 (../../../../etc/passwd):
    BLOCKED: scope_violation

  lfi_003 (../../../tmp/malicious.sh):
    BLOCKED: injection_detected

  rfi_001 (http://localhost:8080/external_config):
    BLOCKED: injection_detected

  safe_001 (config/settings.yaml):
    ALLOWED: safe_content_read_only
```

## Inclusion Scenarios

| Scenario | Type | Path/URL | Expected |
|----------|------|----------|----------|
| `lfi_001` | Path traversal | `../../../../etc/passwd` | Blocked: traversal |
| `lfi_002` | Upload directory | `uploads/user_avatar.png` | Allowed: binary |
| `lfi_003` | Injection in temp | `../../../tmp/malicious.sh` | Blocked: injection |
| `rfi_001` | Simulated RFI | `http://localhost:8080/...` | Blocked: injection |
| `safe_001` | Legitimate config | `config/settings.yaml` | Allowed: data only |

## Scope Policy

```json
{
  "allowed_read_paths": ["/app/config/*", "/app/data/*", "/app/templates/*"],
  "denied_read_paths": ["/etc/*", "/tmp/*", "/root/*"],
  "allowed_actions": ["read_file", "render_template"],
  "denied_actions": ["exec", "write_file", "network_request"]
}
```

## Key Principle

> **READING content ≠ GRANTING authority**

Included files are DATA. Only explicit, verified INSTRUCTIONS drive actions.

## Exercises

### Beginner
1. **Path traversal variants** — Test `..`, `....//`, URL encoding

### Standard
2. **MIME type check** — Add MIME type validation
3. **Nested inclusion** — Handle includes within includes

### Extension
4. **Provenance loss** — Detect provenance loss in pipeline

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/inclusion.json` | Files, scenarios, scope policy |
| `student/inclusiontrap.py` | Vulnerable/guarded agents, scope, detector |
| `student/generate_inclusion_results.py` | Results generator |
| `tests/test_inclusiontrap.py` | 14 tests |

---

*Next: [Demo 09: InterceptBound](../demos/09-interceptbound.md)*