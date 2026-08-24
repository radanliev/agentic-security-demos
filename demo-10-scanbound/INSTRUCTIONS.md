# Demo 10: ScanBound — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md) · Full course lab: [../docs/course/lab-10-scanbound.md](../../docs/course/lab-10-scanbound.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both scanners | 3 min | `python3 student/scanbound.py` |
| Probe validators | 5 min | inline scripts (Steps 4–5) |
| Generate results | 1 min | `python3 student/generate_scan_results.py` |
| **Total** | **~20 min** | Capstone module — take your time |

**Safety:** 100% offline. Targets are `localhost`, `127.0.0.1`, `scan-target.local`. Checks are *simulated* — poisoned outputs are JSON from the fixture. **Nothing leaves your machine.**

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-10-scanbound
```

---

## Step 1 — Read the Fixture and Predict

```bash
cat fixtures/scanbound.json
```

**Before running, fill this prediction table:**

| Check | In scope? | Passes validation? | Output taint | Guarded disposition |
|-------|-----------|--------------------|--------------|---------------------|
| `check_001` (info, safe) | ? | ? | ? | ? |
| `check_002` (xss, safe) | ? | ? | ? | ? |
| `check_003` (SQLi, **unsafe**, modifies state) | ? | ? | ? | ? |
| `check_004` (RCE, **unsafe**, `rm -rf`) | ? | ? | ? | ? |
| `check_005` (TLS, safe) | ? | ? | ? | ? |

**Hints:**
- `check_003/004` are `type: "unsafe"` **and** `modifies_state: true` — two independent validation failures
- Check_001 and 004 outputs carry injection canaries → HIGH taint
- `report` requires taint LOW, but all outputs are MEDIUM/HIGH → predict `actions_taken: []` (empty)

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected:** `21 passed` — the largest suite in the course.

**Key tests:**

| Test | Pins |
|------|------|
| `test_check_validator_ast_detection` | `exec('malicious')` caught only by AST, not keywords |
| `test_unconstrained_trusts_all_output` | Baseline labels *everything* LOW (including poisoned) |
| `test_guarded_blocks_unsafe_checks` | 003/004 blocked with `check_type_unsafe` |
| `test_guarded_tracks_taint` | Blocked checks still have taint tracked (observation vs action) |
| `test_address_ambiguity_prevented` | Only explicitly listed names resolve |

```
============================== 21 passed in 0.XXs ==============================
```

---

## Step 3 — Probe the Validators in Isolation

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import CheckValidator, ScannerCheck, Target

cv = CheckValidator()
def mk(payload, ctype="safe", state=False):
    return ScannerCheck("x", "x", ctype, Target("localhost", 8080, "http"),
                        payload, "ok", state)

for payload, ctype, state in [
    ("GET /health",                 "safe",  False),
    ("' OR '1'='1",                 "unsafe", True),
    ("GET /x",                      "safe",  True),
    ("rm -rf /",                    "safe",  False),
    ("exec('malicious')",           "safe",  False),
    ("import subprocess",           "safe",  False),
    ("__import__('os').system('x')","safe",  False),
]:
    ok, why = cv.validate(mk(payload, ctype, state))
    print(f"{'ALLOW' if ok else 'BLOCK':6} {why:32} {payload[:30]}")
EOF
```

**Expected:** Only row 1 allows; each block has a distinct reason: `check_type_unsafe`, `modifies_state`, `dangerous_payload_keyword`, `dangerous_ast_pattern`.

**Lesson:** keyword screens catch strings; **AST catches structure**. `__import__('os')` has no banned keyword — only parsing reveals the call.

---

## Step 4 — Run Both Scanners End-to-End

```bash
python3 student/scanbound.py
```

**What this does:** Runs 5 checks through **Unconstrained Baseline** (trusts all output, taint LOW everywhere) and **Scope-Bound Guarded** (scope → AST check → taint → policy).

**Expected:**

```
--- Unconstrained Baseline ---
  check_001: Server: Apache... (taint: low)
  check_004: Command blocked... (taint: low)          ← wrong trust

--- Scope-Bound Guarded ---
  check_001: Server: Apache... (taint: high)          ← injection detected
  check_003: BLOCKED (check_type_unsafe)
  check_004: BLOCKED (check_type_unsafe)
  check_005: Cert valid... (taint: medium)
```

**Record three observations:**

1. **Blocked checks still got taint-tracked** — validation blocks execution/forwarding, but tracking still observes.
2. **Same finding, different trust** — check_001's text is identical in both scanners; trust differs (LOW vs HIGH) because provenance differs.
3. **`actions_taken` is empty** — all taints are MEDIUM/HIGH; report needs LOW. The pipeline ends safely *by default*.

---

## Step 5 — Probe Scope Validation Edge Cases

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import ScopeValidator, Target

sv = ScopeValidator(
    allowed_hosts=["localhost", "127.0.0.1", "scan-target.local"],
    allowed_ports=[80, 443, 8080, 8443],
    allowed_protocols=["http", "https"],
)
for host, port, proto in [
    ("localhost",         8080, "http"),
    ("evil.com",          80,   "http"),
    ("localhost",         22,   "ssh"),
    ("LocalHost",         8080, "http"),
]:
    ok, why = sv.validate(Target(host, port, proto))
    print(f"{host:20}:{port:<5} {proto:6} -> {'ALLOW' if ok else 'BLOCK':6} ({why})")
EOF
```

**Expected:** `LocalHost` is blocked (exact-match allowlist is fail-closed but case-brittle — note this for the canonicalization exercise).

---

## Step 6 — Generate the Results File

```bash
python3 student/generate_scan_results.py
cat results/scan_results.json
```

**Expected:** 5 findings (all taint-tracked), 2 blocked checks (003/004), `actions_taken: []`.

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
| Tests passed | | `21 passed` |
| Blocked checks | | 2 (003, 004) |
| High-taint findings | | 2 (001, 004) |
| `actions_taken` | | `[]` (empty — correct) |
| Result file | | `results/scan_results.json` |

**Reproducibility check:** `rm -rf results/ &&` re-run Step 6. JSON must be identical.

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=10`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Add check_006 targeting `intranet.corp.local:80` | Predict `host_not_allowed`; verify output never tainted |
| Standard | Human-in-the-loop: MEDIUM+1 approval reports, HIGH+2 approvals | Audit log with approver ids |
| Standard | Canonical scope: `LocalHost` should match `localhost` | Lowercase + alias table; suffix attacks blocked |
| Extension | AST aliases: `import subprocess as sp; sp.run(...)` | Track `as` bindings; resolve chains |
| Extension | Waiver rung for action policy (never for exploit/exfiltrate) | Meta-policy > individual waiver |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `21 passed` fails after edits | Exercise changes | `git checkout -- student/ fixtures/ tests/` |
| `FileNotFoundError: fixtures/scanbound.json` | Wrong directory | `cd demo-10-scanbound` |
| `check_004` still appears in `results` | Expected — blocked checks are still taint-tracked | See note in Step 4 |
| `LocalHost` blocked but you expected allow | Exact-match scope is case-sensitive | Exercise 3 fixes this |
| Want to allow a denied action | No waiver path for `exploit` by design | Exercise 5 adds a *sanctioned* path |

---

## Safety Reminder

⚠️ **Teaching demonstration only — localhost targets only.** No public scanning, no exploit chains, no credential attacks. This module teaches the *governance layer* around scanning, never scanning itself. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
