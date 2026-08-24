# Demo 09: InterceptBound — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md) · Full course lab: [../docs/course/lab-09-interceptbound.md](../../docs/course/lab-09-interceptbound.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both agents | 3 min | `python3 student/interceptbound.py` |
| Probe guard & buffer | 5 min | inline scripts (Steps 4–5) |
| Generate results | 1 min | `python3 student/generate_intercept_results.py` |
| **Total** | **~15 min** | |

**Safety:** 100% offline. All 6 frames are JSON fixtures. **No sockets, no ARP, no packet capture.** The demo simulates only the decision layer.

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

**What this does:** Shows 6 traffic frames, scope policy (`allowed_sources` + `max_taint_for_action: low`), and buffer config (size 1000, TTL 60s, secure_delete).

**Before running, fill this prediction table:**

| Frame | In scope? | Contains injection/credential? | Baseline will… | Defended will… |
|-------|-----------|-------------------------------|----------------|----------------|
| `frame_001` (HTTP token) | ? | `token` in JSON body | ? | ? |
| `frame_003` (DNS TXT) | ? | `CANARY_DNS_INJECTION…` | ? | ? |
| `frame_004` (TLS handshake) | ? | — | ? | ? |
| `frame_005` (shutdown cmd) | ? | `{"command":"shutdown"}` | ? | ? |

**Critical hint:** `max_taint_for_action` is `low`, yet every frame carries `intercepted_network` with taint HIGH or MEDIUM. Predict: can *any* intercepted credential be stored?

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected:** `15 passed`. Notable: `test_baseline_no_taint_tracking` asserts the baseline **does** execute the shutdown from the stream — the vulnerability is preserved as a specimen.

```
============================== 15 passed in 0.XXs ==============================
```

---

## Step 3 — Run Both Agents

```bash
python3 student/interceptbound.py
```

**What this does:** Runs 6 frames through **Baseline** (no taint, string triggers) and **Taint-Aware** (scope → parse with taint labels → buffer with TTL → guard-gated actions), plus buffer and provenance demos.

**Expected highlights — compare with predictions:**

```
--- Unguarded Baseline ---
  frame_001 (HTTP with token): ALLOWED store_token
  frame_005 (shutdown injection): ALLOWED execute_shutdown    ← vulnerable

--- Taint-Aware Guarded ---
  frame_001: BLOCKED store_token   (taint_too_high: high > low)
  frame_005: BLOCKED execute_shutdown (taint_too_high: high > low)
  frame_002/003: BLOCKED process_injection (injection_detected)
  frame_004: parsed, observed, no sensitive action attempted
```

**Record three distinct block reasons:** `taint_too_high`, `injection_detected`, and (with a synthetic out-of-scope frame from Step 5) `source_not_allowed`. Distinct reasons let an operator tell *which defense* fired.

---

## Step 4 — Probe the Action Guard's Boundary

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from interceptbound import ActionGuard, TaintLevel, Provenance

g = ActionGuard(TaintLevel.LOW)
for action, taint, prov in [
    ("store_credential", TaintLevel.LOW,    Provenance.TRUSTED_LOCAL),
    ("store_credential", TaintLevel.MEDIUM, Provenance.INTERCEPTED_NETWORK),
    ("store_credential", TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
    ("log_metric",       TaintLevel.HIGH,   Provenance.INTERCEPTED_NETWORK),
]:
    ok, why = g.authorize(action, taint, "x", prov)
    print(f"{action:18} taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK'} ({why})")

print("\n-- same guard, max=MEDIUM --")
g2 = ActionGuard(TaintLevel.MEDIUM)
for taint in TaintLevel:
    ok, why = g2.authorize("report_finding", taint, "x", Provenance.INTERCEPTED_NETWORK)
    print(f"  report taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK'} ({why})")
EOF
```

**Expected:** At `max=LOW`, only trusted-local LOW is allowed; note the second guard rule — intercepted-network data requires LOW regardless of max, so even `max=MEDIUM` blocks intercepted HIGH.

---

## Step 5 — Inspect the Ephemeral Buffer

```bash
python3 - << 'EOF'
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
```

**Expected:**

```
immediately: DEMO_TOKEN_ABC123
after delete: None
after TTL:   None
```

**Why 60 seconds matters:** Even defended pipelines hold intercepted secrets transiently. TTL caps lifetime, `max_size` caps volume, secure-delete scrubs on eviction. The residual risk — secret in memory for up to 60 s — is why the guard *also* blocks storing it durably.

---

## Step 6 — Generate the Results File

```bash
python3 student/generate_intercept_results.py
cat results/intercept_results.json
```

**Expected:** 6 frames with `actions` vs `blocked` counts matching Step 3; total `parsed_fields` per frame; `taint_tracked: true` on all.

---

## Step 7 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2–6 |
| Tests passed | | `15 passed` |
| Baseline: frame_005 action | | `execute_shutdown` (allowed) |
| Defended: frame_001 disposition | | `blocked (taint_too_high)` |
| Guard at max=LOW: intercepted HIGH | | `BLOCK` |
| Result file | | `results/intercept_results.json` |

**Reproducibility check:** `rm -rf results/ &&` re-run Step 6. Verdicts must be identical; buffer timing will differ slightly (that's expected — note the difference).

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=09`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Replay detection: `seen_nonces` set; repeated nonce → `blocked: replay_detected` | nonce in JSON payloads |
| Standard | Taint refinement: downgrade `status` fields with rule id | Refinement must be enumerated, never default |
| Standard | Uniform result schema (always list-of-dicts) | Scope block currently returns a string — normalize |
| Extension | Omission detection: `SequenceWatcher` on per-source sequence numbers | Missing frame = attack (Module 5 pattern) |
| Extension | Credential-canary lifecycle: buffer fingerprint, not real value | `sha256(real)[:12]` + `CANARY_CRED` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `15 passed` fails after edits | Exercise changes | `git checkout -- student/ fixtures/ tests/` |
| `FileNotFoundError: fixtures/traffic.json` | Wrong directory | `cd demo-09-interceptbound` |
| All frames report `source_not_allowed` | System IP not in allowlist | Fixture allows `.10/.20/.30/.1`; restore with `git checkout -- fixtures/` |
| `taint_too_high` on every action | Expected with `max=LOW` | Raise `max_taint_for_action` to `medium` and re-run Step 4 |

---

## Safety Reminder

⚠️ **Teaching demonstration only — no ARP poisoning, MITM, or credential collection.** All frames are JSON fixtures. Fake credentials only (`DEMO_TOKEN_*`). Fully simulated traffic stream. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
