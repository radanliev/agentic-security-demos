# Demo 08: InclusionTrap — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md) · Full course lab: [../docs/course/lab-08-inclusiontrap.md](../../docs/course/lab-08-inclusiontrap.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both inclusion agents | 3 min | `python3 student/inclusiontrap.py` |
| Probe resolver & scope | 3 min | inline scripts (Steps 4–5) |
| Generate results | 1 min | `python3 student/generate_inclusion_results.py` |
| **Total** | **~15 min** | |

**Safety:** 100% offline. Localhost fixtures only. "Remote" fetch is simulated from JSON — **no network call ever**. Harmless canary content only. `make verify-safety` blocks any real network import.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-08-inclusiontrap
```

**Verify:**

```bash
ls
# Expected: Makefile  README.md  INSTRUCTIONS.md  fixtures  results  student  tests
```

---

## Step 1 — Read the Fixture and Predict

```bash
cat fixtures/inclusion.json
```

**What this does:** Shows the virtual filesystem (`/app/config/settings.yaml`, `/tmp/malicious.sh`, `/etc/passwd`, etc.), 5 scenarios, and the agent scope (`allowed: /app/config/* …`, `denied: /etc/*, /tmp/*, /root/*`).

**Before running, fill this prediction table:**

| Scenario | Resolves to | Scope? | Injection? | Guarded will… | Vulnerable will… |
|----------|-------------|--------|------------|---------------|------------------|
| `lfi_001` (`../../../../etc/passwd`) | ? | ? | ? | ? | ? |
| `lfi_002` (`uploads/user_avatar.png`) | ? | ? | ? | ? | ? |
| `lfi_003` (`../../../tmp/malicious.sh`) | ? | ? | ? | ? | ? |
| `rfi_001` (`http://localhost:8080/external_config`) | — | ? | ? | ? | ? |
| `safe_001` (`config/settings.yaml`) | ? | ? | ? | ? | ? |

**Key to notice:** The resolver for guarded and vulnerable agents differs; the scope's `allowed` set never contains `/etc/*` or `/tmp/*`; lfi_003 and rfi_001 both contain canary + dangerous strings.

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected:** `14 passed`. Watch for:

- `test_vulnerable_agent_executes_injection` — pins that the vulnerable agent *does* execute the canary
- `test_reading_not_executing` — asserts guarded never has `action == "executed"` for any scenario

```
============================== 14 passed in 0.XXs ==============================
```

---

## Step 3 — Run Both Inclusion Agents

```bash
python3 student/inclusiontrap.py
```

**What this does:** Runs 5 scenarios through **Vulnerable Baseline** (normalizes traversal so it can find the file, detects injection, then **executes anyway**) and **Guarded** (injection screening before scope, path traversal rejected, read-only allow, never executes).

**Expected highlights:**

```
--- Vulnerable Baseline ---
  lfi_003: ✗ VULNERABLE
    Action: executed (injection_detected_but_executed)
    ⚠️  EXECUTED INCLUDED CONTENT!
  lfi_001: allowed (scope never checked)

--- Guarded (Scope + Provenance) ---
  lfi_001: blocked (scope_violation: /blocked/traversal not in allowed paths)
  lfi_002: allowed (safe_content_read_only)
  lfi_003: blocked (injection_detected)
  rfi_001: blocked (injection_detected)
  safe_001: allowed (safe_content_read_only)
```

**Record the thesis sentence:** **READING content ≠ GRANTING authority.** The vulnerable agent knew about lfi_003's injection and executed it anyway. Detection without enforcement is logging, not security.

---

## Step 4 — Probe Scope and Detector in Isolation

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from inclusiontrap import ScopePolicy, InjectionDetector

scope = ScopePolicy(
    allowed=["/app/config/*", "/app/data/*", "/app/templates/*", "/app/uploads/*"],
    denied=["/etc/*", "/tmp/*", "/root/*"],
)
for p in ["/app/config/settings.yaml", "/app/uploads/x.png",
          "/etc/passwd", "/tmp/malicious.sh", "/blocked/traversal"]:
    print(f"{p:28} can_read={scope.can_read(p)}")

det = InjectionDetector()
for c in ["ignore previous instructions", "rm -rf /", "eval(x)",
          "debug: false\nlog_level: info"]:
    print(f"detect({c[:30]!r:35}) -> {det.detect(c)}")
EOF
```

**Expected:** First two scope probes `True`, next three `False`; detector flags the three malicious strings, not the clean YAML.

---

## Step 5 — Trace the Guarded Resolver

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from inclusiontrap import GuardedInclusionAgent, ScopePolicy

agent = GuardedInclusionAgent({}, ScopePolicy(["/app/*"], []))
for p in ["config/settings.yaml", "../../../../etc/passwd",
          "/app/../../etc/shadow", "uploads/../config/settings.yaml"]:
    print(f"{p:32} -> {agent._resolve_path(p)}")
EOF
```

**Expected:**

```
config/settings.yaml              -> /app/config/settings.yaml
../../../../etc/passwd            -> /blocked/traversal
/app/../../etc/shadow             -> /blocked/traversal
uploads/../config/settings.yaml   -> /blocked/traversal
```

**Lesson:** The guarded resolver rejects *any* traversal syntax (`../` or `/../`) rather than normalizing it. `uploads/../config/…` would resolve to an allowed path — but the guard still blocks. Strict > clever when canonicalization has edge cases.

---

## Step 6 — Run the Thesis Test Explicitly

```bash
python3 -m pytest tests/test_inclusiontrap.py::TestInclusionTrap::test_reading_not_executing -v
```

**What this does:** Processes **every** scenario through the guarded agent and asserts no result has `action == "executed"`.

**Why it matters:** This single assertion *is* the module thesis made executable.

---

## Step 7 — Generate the Results File

```bash
python3 student/generate_inclusion_results.py
cat results/inclusion_results.json
```

**Expected:** 5 rows with `action`/`reason`/`provenance` matching Step 3; `file_system` for local scenarios, `simulated_remote` for rfi_001.

---

## Step 8 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2, 3, 7 |
| Tests passed | | `14 passed` |
| lfi_003 vulnerable action | | `executed` (Step 3) |
| lfi_003 guarded action | | `blocked (injection_detected)` (Step 3) |
| lfi_001 guarded reason | | `scope_violation` (Step 3) |
| Result file | | `results/inclusion_results.json` |

**Reproducibility check:** `rm -rf results/ &&` re-run Step 7 — JSON must be identical.

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=08`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Traversal gauntlet: `....//`, `%2f`, backslash variants | Guard sees decoded strings — who decodes? |
| Standard | MIME screening: block `application/x-msdownload` even in-scope | `allowed` = where; type = what |
| Standard | Nested inclusion: allowed template includes `../tmp/malicious.sh` | Depth limit 3, provenance inheritance |
| Extension | Provenance-loss detector: `ProvenanceLostError` on missing label | URL source must be `simulated_remote` |
| Extension | Allow-list template renderer blocking SSTI `{{__class__}}` | Render only allows `{{data}}` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `14 passed` fails after edits | Exercise changes broke logic | `git checkout -- student/ fixtures/ tests/` |
| `FileNotFoundError: fixtures/inclusion.json` | Wrong directory | `cd demo-08-inclusiontrap` |
| `lfi_003` guarded reports `scope_violation` not `injection_detected` | Content was empty (old file read path) | `git checkout -- student/inclusiontrap.py` (updated version checks scenario content) |
| RFI seems to use real network | It doesn't — simulated response from fixture | Verify with `grep -R "requests\|urllib\|socket" student/` |

---

## Safety Reminder

⚠️ **Teaching demonstration only — localhost fixtures only.** No public targets, no real remote inclusion. Harmless canary content. Clear reset: delete `results/` and re-run. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
