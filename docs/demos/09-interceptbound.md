# Demo 09: InterceptBound

## Learning Objectives

- Model intercepted/relayed traffic with synthetic frames
- Implement provenance and taint labels on parsed data
- Distinguish observations from instructions in traffic
- Build ephemeral buffers with safe deletion
- Design downstream action guards

## Conceptual Explanation

An agent processing intercepted traffic sees forged responses. **Taint tracking** labels data by source: `trusted_local`, `user_supplied`, `intercepted_network`. Downstream actions require untainted provenance.

### The Problem

```
Intercepted HTTP Response  →  Agent  →  "token=abc"  →  Store in DB
                          →  Agent  →  "shutdown"   →  EXECUTE!
```

### The Solution

**Taint tracking + Action guards**: Every parsed field carries taint level. High-taint data from intercepted network blocked from sensitive actions.

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No ARP poisoning, MITM, or credential collection**
- No public interception or third-party traffic
- Fake credentials and local canaries only

## Running the Demo

```bash
make demo DEMO=09
```

### Expected Output

```
--- Unguarded Baseline ---
  frame_001 (HTTP with token): ALLOWED store_token
  frame_005 (shutdown injection): ALLOWED execute_shutdown  ← VULNERABLE!

--- Taint-Aware Guarded ---
  frame_001 (token): BLOCKED store_token (taint_too_high)
  frame_004 (TLS safe): ALLOWED observation
  frame_005 (shutdown): BLOCKED execute_shutdown (taint_too_high)
  frame_002 (DNS injection): BLOCKED process_injection
```

## Traffic Frames

| Frame | Protocol | Source | Taint | Injection |
|-------|----------|--------|-------|-----------|
| `frame_001` | HTTP | 192.168.1.10 | HIGH | Token in body |
| `frame_002` | HTTP | 192.168.1.10 | HIGH | XSS in HTML |
| `frame_003` | DNS | 192.168.1.1 | HIGH | TXT injection |
| `frame_004` | TLS | 192.168.1.20 | MEDIUM | None |
| `frame_005` | Custom | 192.168.1.30 | HIGH | Shutdown cmd |
| `frame_006` | HTTP | 192.168.1.10 | MEDIUM | 401 Unauthorized |

## Taint Levels

| Level | Sources | Can Trigger Sensitive Actions? |
|-------|---------|--------------------------------|
| `LOW` | Trusted local, user supplied | ✅ Yes |
| `MEDIUM` | Intercepted network (clean) | ⚠️ Low-risk only |
| `HIGH` | Intercepted network (injected) | ❌ No |

## Action Guard

```python
guard = ActionGuard(max_taint_for_action=TaintLevel.LOW)
guard.authorize("store_credential", TaintLevel.HIGH, ...)  # → False
guard.authorize("report_finding", TaintLevel.LOW, ...)     # → True
```

## Ephemeral Buffer

- Max size: 1000 entries
- TTL: 60 seconds
- Secure delete: Overwrite on deletion

## Exercises

### Beginner
1. **Replay detection** — Detect replayed frames

### Standard
2. **Omission detection** — Detect omitted frames in sequence
3. **Credential canary** — Track credential-like canaries

### Extension
4. **Taint propagation** — Propagate taint through transformations

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/traffic.json` | 6 synthetic traffic frames |
| `student/interceptbound.py` | Tracker, buffer, guard, agents |
| `student/generate_intercept_results.py` | Results generator |
| `tests/test_interceptbound.py` | 15 tests |

---

*Next: [Demo 10: ScanBound](../demos/10-scanbound.md)*