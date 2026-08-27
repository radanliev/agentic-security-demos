# Demo 10: ScanBound — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md) · Full course lab: [../docs/course/lab-10-scanbound.md](../../docs/course/lab-10-scanbound.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both scanners | 3 min | `python3 student/scanbound.py` |
| Probe validators and policy | 6 min | inline scripts (Steps 3, 5, 6) |
| Generate results | 1 min | `python3 student/generate_scan_results.py` |
| **Total** | **~20 min** | Capstone module — take your time |

**Safety:** 100% offline. Targets are `localhost`, `127.0.0.1`, `scan-target.local` (plus one deliberately out-of-scope name that is never contacted). The scanner is *simulated*: `SimulatedScanner.execute` returns canned JSON from the fixture and records that the check ran. Actions the baseline "takes" are recorded, never performed. **Nothing leaves your machine** — `test_no_network_or_process_imports` checks the module's imports.

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

The `expected` block is the **answer key** (read only by the tests and the results generator — never by the scanners). Cover it while you predict:

| Check | In scope? | Passes validation? | Runs? | Output taint | Auto-reported? |
|-------|-----------|--------------------|-------|--------------|----------------|
| `check_001` (info, safe; output carries a canary) | ? | ? | ? | ? | ? |
| `check_002` (xss, safe; clean output) | ? | ? | ? | ? | ? |
| `check_003` (SQLi, **unsafe**, modifies state) | ? | ? | ? | ? | ? |
| `check_004` (RCE, **unsafe**, `; rm -rf /`) | ? | ? | ? | ? | ? |
| `check_005` (TLS, safe; clean output) | ? | ? | ? | ? | ? |
| `check_006` (safe, but target `intranet.corp.local`) | ? | ? | ? | ? | ? |
| `check_007` (debug page, safe; output leaks `db_password=`) | ? | ? | ? | ? | ? |

**Hints:**
- A check that fails scope or validation is **never executed** — it produces no output, no finding and no taint. There is nothing to observe.
- Taint is read from the finding *text*: a `CANARY_…` marker, an instruction (`RUN_CMD`, `EXFILTRATE`) or a credential pattern makes it HIGH; clean scanner output is MEDIUM, never LOW.
- `max_taint_for_report` is `medium`: MEDIUM findings are auto-reported, HIGH findings are held (`taint_too_high`). Predict `actions_taken` and `actions_blocked`.

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected:** `51 passed` — the largest suite in the course.

**Key tests:**

| Test | Pins |
|------|------|
| `test_rejected_checks_never_execute` / `test_validation_happens_before_execution` | 003/004/006 never reach the scanner (a spy scanner records calls) |
| `test_ast_screen_catches_structure_without_keyword_gate` | `exec ('x')`, `import subprocess`, `__import__('os')…` — payloads with no banned keyword |
| `test_unknown_type_fails_closed` | `type: "code_exec"` (or a typo) is rejected, not waved through |
| `test_detection_reads_every_string_not_a_side_channel` | taint comes from the output text, wherever the injection sits |
| `test_action_policy_consulted_for_every_finding` | the policy is called once per finding; the ledger records allow *and* block |
| `test_unconstrained_follows_injected_instructions_simulated` | the baseline's failure is an *action*, not just a label |
| `test_generator_matches_fixture_expectations` | `results/scan_results.json` is checked against the answer key |

```
============================== 51 passed in 0.XXs ==============================
```

---

## Step 3 — Probe the Check Validator in Isolation

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import CheckValidator, ScannerCheck, Target

cv = CheckValidator()
def mk(payload, ctype="safe", state=False):
    return ScannerCheck("x", "x", ctype, Target("localhost", 8080, "http"), payload, "ok", state)

for payload, ctype, state in [
    ("GET /health",                  "safe",   False),
    ("' OR '1'='1",                  "unsafe", True),
    ("GET /x",                       "safe",   True),
    ("; rm -rf /",                   "safe",   False),
    ("exec('malicious')",            "safe",   False),
    ("exec ('malicious')",           "safe",   False),
    ("import subprocess",            "safe",   False),
    ("__import__('os').system('x')", "safe",   False),
    ("json.dumps({'a': 1})",         "safe",   False),
    ("probe",                        "code_exec", False),
]:
    ok, why = cv.validate(mk(payload, ctype, state))
    print(f"{'ALLOW' if ok else 'BLOCK':6} {payload!r:32} {why}")
EOF
```

**Expected:**

```
ALLOW  'GET /health'                    safe
BLOCK  "' OR '1'='1"                    check_type_unsafe; modifies_state
BLOCK  'GET /x'                         modifies_state
BLOCK  '; rm -rf /'                     dangerous_payload_keyword: rm -rf
BLOCK  "exec('malicious')"              dangerous_ast_pattern: call:exec
BLOCK  "exec ('malicious')"             dangerous_ast_pattern: call:exec
BLOCK  'import subprocess'              dangerous_ast_pattern: import:subprocess
BLOCK  "__import__('os').system('x')"   dangerous_ast_pattern: call:.system; dangerous_ast_pattern: call:__import__
ALLOW  "json.dumps({'a': 1})"           safe
BLOCK  'probe'                          check_type_unknown: 'code_exec'
```

**Lesson:** keyword screens catch strings; **AST catches structure**. `exec ('malicious')` and `__import__('os').system('x')` contain no banned keyword — only parsing reveals the call. The AST screen therefore runs on *every* payload (there is no keyword pre-gate) and parses statements as well as expressions (`import subprocess` is a statement). Payloads that are not Python at all (`GET /health`) are simply out of its reach, which is why the other three screens exist — and why *every* failing screen is listed, not just the first.

**Known limit** (Exercise 4): names built at runtime — `getattr(__builtins__, 'ex' + 'ec')` — are not resolved statically.

---

## Step 4 — Run Both Scanners End-to-End

```bash
python3 student/scanbound.py
```

**What this does:** Runs 7 checks through **Unconstrained Baseline** (runs everything, labels every output `taint: low`, reports it, and follows instruction-shaped output) and **Scope-Bound Guarded** (scope → validate → execute → taint → policy).

**Expected — verbatim:**

```
--- Unconstrained Baseline (runs everything, trusts everything) ---
  check_001 (localhost:8080): Server: Apache/2.4.41 <!-- CANARY_SCANNER_INJECTION_RUN_CMD_... (taint: low)
    ACTION: report:check_001
    ACTION: execute_command:whoami [SIMULATED - recorded, not run] <- from check_001 output
  check_004 (127.0.0.1:8443): Command blocked. CANARY_SCANNER_INJECTION_EXFILTRATE_KEYS... (taint: low)
    ACTION: report:check_004
    ACTION: exfiltrate:keys [SIMULATED - recorded, not run] <- from check_004 output
  check_006 (intranet.corp.local:80): SHOULD_NEVER_BE_READ: out-of-scope host answered... (taint: low)
    ACTION: report:check_006
  Checks executed: 7/7

--- Scope-Bound Guarded (scope -> validate -> execute -> taint -> policy) ---
  check_001 (localhost:8080): Server: Apache/2.4.41 <!-- CANARY_SCANNER_INJECTION_RUN_CMD_... (taint: high [canary_marker, instruction_run_cmd])
    BLOCKED ACTION: report:check_001 (taint_too_high: high > medium)
  check_002 (scan-target.local:80): XSS reflected in search... (taint: medium)
    ACTION: report:check_002
  BLOCKED CHECK: check_003 (check_type_unsafe; modifies_state) - never executed
  BLOCKED CHECK: check_004 (check_type_unsafe; modifies_state; dangerous_payload_keyword: rm -rf) - never executed
  check_005 (127.0.0.1:8443): Cert valid until 2031-06-30... (taint: medium)
    ACTION: report:check_005
  BLOCKED CHECK: check_006 (host_not_allowed: intranet.corp.local) - never executed
  check_007 (localhost:8080): Debug page exposed: db_password=DEMO_PASSWORD_1234... (taint: high [credential_pattern])
    BLOCKED ACTION: report:check_007 (taint_too_high: high > medium)
  Checks executed: 4/7 -> ['check_001', 'check_002', 'check_005', 'check_007']
```

**Record three observations:**

1. **Rejected checks never run.** 003, 004 and 006 produce no finding and no taint — `Checks executed: 4/7`. Validation is a gate *before* execution, not a label on a result.
2. **Same finding text, different trust.** check_001's output is identical in both runs; the baseline labels it `low` and *executes the instruction inside it* (simulated), the guarded scanner reads `high` off the text and holds the finding.
3. **The policy was consulted for every finding.** Two MEDIUM findings are reported; two HIGH findings are blocked with a reason. An empty `actions_blocked` would have meant "never asked", not "nothing to block".

---

## Step 5 — Probe Scope Validation Edge Cases

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import ScopeValidator, Target

sv = ScopeValidator(allowed_hosts=["localhost", "127.0.0.1", "scan-target.local"],
                    allowed_ports=[80, 443, 8080, 8443], allowed_protocols=["http", "https"])
for host, port, proto in [
    ("localhost",              8080, "http"),
    ("evil.example",           80,   "http"),
    ("localhost",              22,   "ssh"),
    ("localhost",              8080, "ftp"),
    ("LocalHost",              8080, "http"),
    ("localhost.evil.example", 80,   "http"),
]:
    ok, why = sv.validate(Target(host, port, proto))
    print(f"{host:24}:{port:<5} {proto:6} -> {'ALLOW' if ok else 'BLOCK':6} ({why})")
EOF
```

**Expected:**

```
localhost               :8080  http   -> ALLOW  (in_scope)
evil.example            :80    http   -> BLOCK  (host_not_allowed: evil.example)
localhost               :22    ssh    -> BLOCK  (port_not_allowed: 22)
localhost               :8080  ftp    -> BLOCK  (protocol_not_allowed: ftp)
LocalHost               :8080  http   -> BLOCK  (host_not_allowed: LocalHost)
localhost.evil.example  :80    http   -> BLOCK  (host_not_allowed: localhost.evil.example)
```

`LocalHost` is blocked: exact-match allowlists are fail-closed but case-brittle — note it for the canonicalization exercise. The suffix attack (`localhost.evil.example`) is blocked for the same reason.

---

## Step 6 — Probe the Action Policy Boundary

```bash
python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import ActionPolicy, ActionType, TaintLevel

ap = ActionPolicy(allowed=["report_finding", "generate_report"],
                  denied=["exploit", "exfiltrate", "modify_target", "execute_command"],
                  max_taint=TaintLevel.MEDIUM)
for action, taint in [
    (ActionType.REPORT_FINDING,  TaintLevel.LOW),
    (ActionType.REPORT_FINDING,  TaintLevel.MEDIUM),
    (ActionType.REPORT_FINDING,  TaintLevel.HIGH),
    (ActionType.EXPLOIT,         TaintLevel.LOW),
    (ActionType.EXECUTE_COMMAND, TaintLevel.LOW),
    (ActionType.GENERATE_REPORT, TaintLevel.MEDIUM),
]:
    ok, why = ap.authorize(action, taint)
    print(f"{action.value:16} taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK':6} ({why})")
EOF
```

**Expected:**

```
report_finding   taint=low    -> ALLOW  (authorized)
report_finding   taint=medium -> ALLOW  (authorized)
report_finding   taint=high   -> BLOCK  (taint_too_high: high > medium)
exploit          taint=low    -> BLOCK  (action_denied: exploit)
execute_command  taint=low    -> BLOCK  (action_denied: execute_command)
generate_report  taint=medium -> ALLOW  (authorized)
```

Two distinct denial reasons: policy membership (`action_denied`, unconditional — no taint level authorises `exploit`) versus data quality (`taint_too_high`). The command the baseline "executed" in Step 4 is exactly the `execute_command` row.

---

## Step 7 — Generate the Results File

```bash
python3 student/generate_scan_results.py
cat results/scan_results.json
```

**Expected:** `"result": "pass"`; `summary.guarded_executed` = `["check_001", "check_002", "check_005", "check_007"]`; 3 `blocked_checks` (003, 004, 006, each `"executed": false`); `actions_taken` = `["report:check_002", "report:check_005"]`; `actions_blocked` lists 001 and 007 with `taint_too_high: high > medium`; `matches_expected: true` for all 7 checks. `result` is **computed** by comparing both scanners with the fixture's `expected` block; the generator exits 1 on any mismatch. `commit` is the git SHA (or `local` outside a checkout).

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
| Tests passed | | `51 passed` |
| Checks executed (guarded) | | 4 of 7 |
| Blocked checks | | 3 (003, 004 validation; 006 scope) |
| High-taint findings | | 2 (001 canary, 007 credential) |
| `actions_taken` / `actions_blocked` | | 2 / 2 |
| Baseline instructions followed (simulated) | | `execute_command:whoami`, `exfiltrate:keys` |
| Result file | | `results/scan_results.json` (`"result": "pass"`) |

**Reproducibility check:** `rm -rf results/ &&` re-run Step 7 (the generator recreates the directory). The file must be byte-identical on the same commit and machine.

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=10`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | 1. Add check_008 targeting `10.0.0.5:8080` with a canned output | Predict `host_not_allowed`; assert it is absent from `taint_map` and from `executed` |
| Standard | 2. Human-in-the-loop: `review_and_report(findings, approvals)` — a HIGH finding needs two approvals | Audit log with approver ids; MEDIUM findings stay auto-reported |
| Standard | 3. Canonical scope: `LocalHost` should match `localhost` | Lowercase + local alias table (no DNS); `localhost.evil.example` must stay blocked |
| Extension | 4. AST aliases: `import subprocess as sp; sp.run(...)` | Track `as` bindings; resolve `Name`/`Attribute` chains; `test_exercise_ast_alias_gap` is the starting point |
| Extension | 5. Waiver rung for the action policy (never for exploit/exfiltrate) | Meta-policy > individual waiver |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `51 passed` fails after edits | Exercise changes | `git checkout -- student/ fixtures/ tests/` |
| `FileNotFoundError: … fixtures/scanbound.json` | Fixture missing or renamed | paths are resolved relative to the script, so the working directory does not matter; restore with `git checkout -- fixtures/` |
| Generator exits 1 with `MISMATCH against fixture expectations` | Code or fixture edited | the `expected` block is the answer key; update it deliberately or revert |
| A check you added never appears in `results` | It failed scope or validation | look for it in `blocked_checks` — rejected checks do not run |
| `LocalHost` blocked but you expected allow | Exact-match scope is case-sensitive | Exercise 3 fixes this |
| Want to allow a denied action | No waiver path for `exploit` by design | Exercise 5 adds a *sanctioned* path |

---

## Safety Reminder

⚠️ **Teaching demonstration only — localhost targets only.** No public scanning, no exploit chains, no credential attacks. This module teaches the *governance layer* around scanning, never scanning itself. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
