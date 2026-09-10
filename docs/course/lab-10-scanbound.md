# Module 10: ScanBound — Vulnerability Assessment Scope Control

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Modules 4, 6, 9 (provenance, injection, taint)
**Demo directory**: `demo-10-scanbound/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Enforce** an explicit scan scope (host/port/protocol allowlists) and block out-of-scope targets *before* any check runs
2. **Validate** scanner checks for safety — *before they execute* — using type checks, state-modification flags, keyword screening, and **Python AST analysis**
3. **Taint** scanner *output* from its own text — including detecting poisoned results carrying injection canaries, embedded instructions, or credential-like strings
4. **Gate** downstream actions (report, exploit, exfiltrate…) with an action policy combining allowlists and taint ceilings, consulted for every finding
5. **Contrast** the unconstrained scanner (runs everything, taint=LOW everywhere, follows the instructions hidden in its output) with the scope-bound scanner (validates, taints, blocks) — and articulate why the *same finding* deserves different trust depending on its source

---

## 📖 Background: The Scanner That Gets Pwned

Autonomous vulnerability scanners are doubly exposed: they **act** on targets (scope risk) and they **consume** machine-generated output (poisoned-input risk). A scanner that parses plugin results as instructions, or reports whatever a hostile endpoint feeds it, becomes an attack channel:

```
   HOSTILE TARGET / PLUGIN                SCANNER PIPELINE
┌────────────────────────────────┐    ┌────────────────────────────────────┐
│ scanner output:                │    │ 1. scope:  is target allowed?      │
│  {"result":"pass",             │───►│ 2. check:  is the check safe?      │
│   "details":"Server: Apache    │    │    (type/state/AST/keywords)       │
│    <!-- CANARY_…RUN_CMD_WHOAMI │    │    -> only then is it executed     │
│    -->"}                       │    │ 3. taint:  is output poisoned?     │
└────────────────────────────────┘    │ 4. policy: may we act on it?       │
                                      └────────────────────────────────────┘
```

Four gates, each answering one question:

| Gate | Question | Mechanism in this demo |
|------|----------|------------------------|
| **Scope** | May I touch this target? | Host allowlist (exact match; `*.` suffix and CIDR patterns are explicit opt-ins) + port allowlist + protocol allowlist |
| **Check validation** | Is this check itself safe to run? | `type == "safe"` (anything else fails closed), `modifies_state == False`, **AST walk** rejecting `exec`/`eval`/`__import__` calls, `.system`/`.run`/`.Popen`-style calls and `subprocess`/`os`/`shutil`… imports, dangerous-keyword screen — all four run on every check *before it executes*, and every failing screen is reported |
| **Taint tracking** | Is this *output* trustworthy? | Read from the finding text: HIGH if it carries a `CANARY_` marker, an instruction (`RUN_CMD`, `EXFILTRATE`, "ignore previous instructions") or a credential pattern; else MEDIUM (scanner output is never LOW; output that was never tracked is HIGH) |
| **Action policy** | May we act on this finding? | Allowed-actions set + denied-actions set + taint ceiling (`report` requires ≤ MEDIUM; HIGH is held with `taint_too_high`) — consulted for every finding |

**The baseline's signature failure**: it labels *all* scanner output `taint=LOW` — including output carrying `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI` — and then does what that output says: `execute_command:whoami [SIMULATED - recorded, not run]`. Wrong trust at the leaf poisons every decision above it.

**Safety framing**: targets are `localhost`, `127.0.0.1`, `scan-target.local`, plus one deliberately out-of-scope name (`intranet.corp.local`) that is never contacted. Checks are *simulated* — `SimulatedScanner.execute` hands back the fixture's `poisoned_scanner_output` for a check and records that the check ran; the baseline's "actions" are recorded strings. Nothing leaves your machine; `make verify-safety` holds. This module teaches the *governance layer* around scanning, never scanning itself.

### The seven checks

| ID | Name | Type | Target | Payload | Modifies state? |
|----|------|------|--------|---------|-----------------|
| check_001 | info_disclosure | safe | localhost:8080 | `GET /server-info` | no |
| check_002 | xss_test | safe | scan-target.local:80 | `<script>alert(1)</script>` | no |
| check_003 | sql_injection | **unsafe** | localhost:8080 | `' OR '1'='1` | **yes** |
| check_004 | rce_attempt | **unsafe** | 127.0.0.1:8443 (https) | `; rm -rf /` | **yes** |
| check_005 | ssl_check | safe | 127.0.0.1:8443 (https) | TLS handshake | no |
| check_006 | intranet_probe | safe | **intranet.corp.local:80** | `GET /` | no |
| check_007 | debug_endpoint | safe | localhost:8080 | `GET /debug` | no |

And the poisoned outputs, all inside the `details` text as they would be in a real report: check_001 carries `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI`; check_004 carries `CANARY_SCANNER_INJECTION_EXFILTRATE_KEYS`; check_007 leaks `db_password=DEMO_PASSWORD_1234`; check_006's canned output begins `SHOULD_NEVER_BE_READ` — if that string ever shows up in the guarded results, scope failed.

---

## 🛠️ Part 1: Fixtures and Predictions

### Step 1: Read the fixture

```bash
cat demo-10-scanbound/fixtures/scanbound.json
```

**What this does**: Prints target scope, mock services (informational only — nothing reads them), the seven checks, poisoned outputs, the downstream policy (allowed: report_finding/generate_report; denied: exploit/exfiltrate/modify_target/execute_command; max taint for report: MEDIUM), and an `expected` block. That block is the **answer key** — read by the tests and the results generator, never by the scanners. Cover it while you predict.

**Why it matters**: Fill the prediction table *before* running:

| Check | In scope? | Passes validation? | Runs? | Output taint | Final disposition (guarded) |
|-------|-----------|--------------------|-------|--------------|------------------------------|
| check_001 | ? | ? | ? | ? | ? |
| check_002 | ? | ? | ? | ? | ? |
| check_003 | ? | ? | ? | ? | ? |
| check_004 | ? | ? | ? | ? | ? |
| check_005 | ? | ? | ? | ? | ? |
| check_006 | ? | ? | ? | ? | ? |
| check_007 | ? | ? | ? | ? | ? |

Reasoning hints: check_003/004 are `type: "unsafe"` *and* `modifies_state: true` — two independent validation failures, and check_004's payload adds a third (`rm -rf`). A check that fails scope or validation is **never executed** — it produces no output, no finding and no taint; there is nothing to observe. check_001's output carries an injection canary and check_007's a credential → taint HIGH; clean output is MEDIUM, never LOW. Since `report` requires taint ≤ MEDIUM, clean findings are auto-reported and HIGH findings are *held*. Which two checks land in `actions_taken`, and which two in `actions_blocked`? Is holding the correct conservative default, or a bug? Hold that question for Step 6.

---

## 🧪 Part 2: The Validators in Isolation

### Step 2: Probe the scope validator

```bash
cd demo-10-scanbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import ScopeValidator, Target

sv = ScopeValidator(
    allowed_hosts=["localhost", "127.0.0.1", "scan-target.local"],
    allowed_ports=[80, 443, 8080, 8443],
    allowed_protocols=["http", "https"],
)
cases = [
    ("localhost",         8080, "http",  True),
    ("127.0.0.1",         8443, "https", True),
    ("scan-target.local", 80,   "http",  True),
    ("evil.com",          80,   "http",  False),  # host
    ("localhost",         22,   "ssh",   False),  # port + protocol
    ("localhost",         8080, "ftp",   False),  # protocol only
    ("LocalHost",         8080, "http",  False),  # case! (exact match)
]
for host, port, proto, want in cases:
    ok, why = sv.validate(Target(host, port, proto))
    print(f"{host:20}:{port:<5} {proto:6} -> {'ALLOW' if ok else 'BLOCK':6} ({why})",
          "OK" if ok == want else "MISMATCH")
EOF
cd ..
```

**What this does**: Sweeps the scope validator with seven cases, including a case-sensitivity probe.

**Expected output**:

```
localhost           :8080  http   -> ALLOW  (in_scope) OK
127.0.0.1           :8443  https  -> ALLOW  (in_scope) OK
scan-target.local   :80    http   -> ALLOW  (in_scope) OK
evil.com            :80    http   -> BLOCK  (host_not_allowed: evil.com) OK
localhost           :22    ssh    -> BLOCK  (port_not_allowed: 22) OK
localhost           :8080  ftp    -> BLOCK  (protocol_not_allowed: ftp) OK
LocalHost           :8080  http   -> BLOCK  (host_not_allowed: LocalHost) OK
```

**Why it matters**: All seven rows print OK — including `LocalHost`, which is *blocked* (exact string match → `host_not_allowed`, which is safe-direction but a usability bug). Record it: **exact-match scope is fail-closed but brittle**. Module 6 Exercise 6.3 had you canonicalize hostnames; same fix applies here (Exercise 10.3). The deeper point: every allowlist match is a *representation* comparison, and representations have edge cases — case, encoding, aliases (`127.0.0.1` vs `localhost` vs `0177.0.0.1`). Nothing in `ScopeValidator` resolves names: there is no DNS lookup anywhere in the module (`test_no_network_or_process_imports` pins that it imports no socket or HTTP library), `*.` suffix patterns and CIDR ranges have to be listed explicitly, and `test_address_ambiguity_fails_closed` pins that `localhost.evil.example`, `evil.localhost`, `LocalHost`, `0177.0.0.1` and `127.1` are all blocked. One more detail: the scope validator returns at the first failing dimension (host, then port, then protocol), so the `ssh` row reports only `port_not_allowed: 22` — unlike the check validator in Step 3, which reports every failing screen.

---

### Step 3: Probe the check validator, especially the AST path

```bash
cd demo-10-scanbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import CheckValidator, ScannerCheck, Target

cv = CheckValidator()
def mk(payload, ctype="safe", state=False):
    return ScannerCheck("x", "x", ctype, Target("localhost", 8080, "http"),
                        payload, "ok", state)

cases = [
    ("GET /health",                 "safe",  False),
    ("' OR '1'='1",                 "unsafe", True),   # double-flagged
    ("GET /x",                      "safe",  True),    # state flag alone
    ("rm -rf /",                    "safe",  False),   # keyword
    ("exec('malicious')",           "safe",  False),   # AST: Call->exec
    ("exec ('malicious')",          "safe",  False),   # AST: same call, no 'exec(' substring
    ("import subprocess",           "safe",  False),   # AST: Import (a statement)
    ("__import__('os').system('x')","safe",  False),   # AST: dunder import
    ("os.system('id')",             "safe",  False),   # AST: Attribute->.system
    ("json.dumps({'a': 1})",        "safe",  False),   # benign Python
    ("probe",                       "code_exec", False),  # unknown type
]
for payload, ctype, state in cases:
    ok, why = cv.validate(mk(payload, ctype, state))
    print(f"{'ALLOW' if ok else 'BLOCK':6} {payload!r:32} {why}")
EOF
cd ..
```

**What this does**: Sweeps the check validator across eleven payloads: benign, type-flagged, state-flagged, keyword-flagged, five AST-detectable code shapes, benign Python, and a check whose type is neither `safe` nor `unsafe`.

**Expected output**:

```
ALLOW  'GET /health'                    safe
BLOCK  "' OR '1'='1"                    check_type_unsafe; modifies_state
BLOCK  'GET /x'                         modifies_state
BLOCK  'rm -rf /'                       dangerous_payload_keyword: rm -rf
BLOCK  "exec('malicious')"              dangerous_ast_pattern: call:exec
BLOCK  "exec ('malicious')"             dangerous_ast_pattern: call:exec
BLOCK  'import subprocess'              dangerous_ast_pattern: import:subprocess
BLOCK  "__import__('os').system('x')"   dangerous_ast_pattern: call:.system; dangerous_ast_pattern: call:__import__
BLOCK  "os.system('id')"                dangerous_ast_pattern: call:.system
ALLOW  "json.dumps({'a': 1})"           safe
BLOCK  'probe'                          check_type_unknown: 'code_exec'
```

**Why it matters**: Everything except `GET /health` and `json.dumps(...)` BLOCKs, and the reason string names *every* failing screen rather than the first one: `check_type_unsafe; modifies_state` for the double-flagged row, `modifies_state`, `dangerous_payload_keyword: rm -rf`, `dangerous_ast_pattern: …` (two hits for the dunder row), and `check_type_unknown: 'code_exec'` — a type that is neither `safe` nor `unsafe` fails closed instead of being waved through. The five AST rows are the teaching core: **keyword screens catch strings; AST catches structure.** `exec ('malicious')` has no `exec(` substring and `__import__('os').system('x')` contains no banned keyword — only parsing reveals the calls. The AST screen parses *every* payload as Python (statement mode, so `import subprocess` counts) with no keyword pre-gate; payloads that are not Python at all (`GET /health`, `' OR '1'='1`) are simply outside its reach, which is why the other three screens exist. This is the same string-vs-semantics gap you met in Module 1 (string oracles vs AST oracles) and Module 8 Exercise 8.5 (template grammar). The pattern recurs because the attack recurs: *smuggle semantics inside innocent-looking text.*

**Also note the layering**: type flag → state flag → AST → keywords. All four screens run on every check, and every failing one is reported — check_004 in Step 4 trips three at once. Ask in notes: why report every reason instead of stopping at the first hit, and why does having *redundant* layers matter for robustness? One known limit to record: `getattr(__builtins__, 'ex' + 'ec')('x')` is ALLOWed — names built at runtime are not resolved statically (`test_known_limit_runtime_name_resolution`). Exercise 10.4's territory.

---

## 🤖 Part 3: Baseline vs Guarded, End to End

### Step 4: Run both scanners

```bash
cd demo-10-scanbound && python3 student/scanbound.py && cd ..
```

**What this does**: Runs the full demo: all seven checks through the unconstrained baseline, then through the scope-bound guarded scanner (scope → validate → execute → taint → policy).

**Why it matters** — the contrast, side by side:

**Baseline** (expected, verbatim): all seven checks run, every finding labeled `taint: low` — including check_001's output carrying `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI` — every finding reported, and the instructions hidden in two outputs followed (simulated). Nothing blocked. Nothing flagged.

```
--- Unconstrained Baseline (runs everything, trusts everything) ---
  check_001 (localhost:8080): Server: Apache/2.4.41 <!-- CANARY_SCANNER_INJECTION_RUN_CMD_... (taint: low)
    ACTION: report:check_001
    ACTION: execute_command:whoami [SIMULATED - recorded, not run] <- from check_001 output
  check_002 (scan-target.local:80): XSS reflected in search... (taint: low)
    ACTION: report:check_002
  check_003 (localhost:8080): No SQL error... (taint: low)
    ACTION: report:check_003
  check_004 (127.0.0.1:8443): Command blocked. CANARY_SCANNER_INJECTION_EXFILTRATE_KEYS... (taint: low)
    ACTION: report:check_004
    ACTION: exfiltrate:keys [SIMULATED - recorded, not run] <- from check_004 output
  check_005 (127.0.0.1:8443): Cert valid until 2031-06-30... (taint: low)
    ACTION: report:check_005
  check_006 (intranet.corp.local:80): SHOULD_NEVER_BE_READ: out-of-scope host answered... (taint: low)
    ACTION: report:check_006
  check_007 (localhost:8080): Debug page exposed: db_password=DEMO_PASSWORD_1234... (taint: low)
    ACTION: report:check_007
  Checks executed: 7/7
```

**Guarded** (expected, verbatim):
```
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

Three observations to record:
1. **Rejected checks never run.** check_003/004 (validation) and check_006 (scope) produce no finding and no taint — `Checks executed: 4/7`. Validation is a gate *before* `SimulatedScanner.execute`, not a label on a result; a rejected check has no output to observe. check_006's canned output says `SHOULD_NEVER_BE_READ`, and it is not.
2. **Same finding, different trust.** check_001's "Server: Apache" is identical text in both scanners; baseline says trust it (LOW) and follows the instruction embedded in it (`execute_command:whoami`, simulated); guarded reads `high [canary_marker, instruction_run_cmd]` off the text and holds the finding. The *finding* didn't change — the *epistemics* did. This is the module's version of Module 9's "observe ≠ act."
3. **The policy was consulted for every finding.** Two MEDIUM findings are reported (`ACTION: report:check_002`, `report:check_005`); two HIGH findings are held with a reason (`BLOCKED ACTION: report:check_001 (taint_too_high: high > medium)`, likewise check_007). An empty `actions_blocked` would have meant "never asked", not "nothing to block". The pipeline holds poisoned findings *by default*, and Exercise 10.2 makes you design the sanctioned path by which a human turns a held HIGH finding into a report.

---

### Step 5: Generate the results artifact

```bash
cd demo-10-scanbound && python3 student/generate_scan_results.py && cd ..
cat demo-10-scanbound/results/scan_results.json
```

**What this does**: Runs both scanners and writes `results/scan_results.json`: per-check findings with taint and taint reasons, blocked checks with reasons (each `"executed": false`), both action ledgers, and a per-check comparison against the fixture's `expected` answer key. `result` is *computed* — `"pass"` only if every expectation holds — and the generator exits 1 on any mismatch.

**Expected** (the file's `summary` block; the `results`, `blocked_checks`, ledger and `per_check` sections follow it):

```
  "summary": {
    "checks": 7,
    "baseline_executed": [
      "check_001",
      "check_002",
      "check_003",
      "check_004",
      "check_005",
      "check_006",
      "check_007"
    ],
    "baseline_followed_instructions": [
      "execute_command:whoami [SIMULATED - recorded, not run] <- from check_001 output",
      "exfiltrate:keys [SIMULATED - recorded, not run] <- from check_004 output"
    ],
    "guarded_executed": [
      "check_001",
      "check_002",
      "check_005",
      "check_007"
    ],
    "guarded_blocked_checks": [
      {
        "check": "check_003",
        "reason": "check_type_unsafe; modifies_state",
        "executed": false
      },
      {
        "check": "check_004",
        "reason": "check_type_unsafe; modifies_state; dangerous_payload_keyword: rm -rf",
        "executed": false
      },
      {
        "check": "check_006",
        "reason": "host_not_allowed: intranet.corp.local",
        "executed": false
      }
    ],
    "guarded_actions_taken": [
      "report:check_002",
      "report:check_005"
    ],
    "guarded_actions_blocked": [
      "report:check_001 (taint_too_high: high > medium)",
      "report:check_007 (taint_too_high: high > medium)"
    ]
  },
```

**Why it matters**: Verify against Step 1 predictions: 4 findings (only the checks that ran), 3 blocked (003/004 by validation, 006 by scope), `actions_taken` with two reports, `actions_blocked` with two holds, `"matches_expected": true` for all seven checks and `"result": "pass"`. `commit` is the git SHA (`local` outside a checkout). This file is your lab evidence and the input to Exercise 10.1's out-of-scope probe.

---

## 📊 Part 4: The Action Policy and the Tests

### Step 6: Probe the action policy boundary

```bash
cd demo-10-scanbound && python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from scanbound import ActionPolicy, ActionType, TaintLevel

ap = ActionPolicy(
    allowed=["report_finding", "generate_report"],
    denied=["exploit", "exfiltrate", "modify_target", "execute_command"],
    max_taint=TaintLevel.MEDIUM,                      # the fixture's max_taint_for_report
)
cases = [
    (ActionType.REPORT_FINDING,   TaintLevel.LOW),    # allowed + clean
    (ActionType.REPORT_FINDING,   TaintLevel.MEDIUM), # allowed + ordinary scanner output
    (ActionType.REPORT_FINDING,   TaintLevel.HIGH),   # allowed + poisoned
    (ActionType.EXPLOIT,          TaintLevel.LOW),    # denied outright
    (ActionType.EXFILTRATE,       TaintLevel.LOW),    # denied outright
    (ActionType.EXECUTE_COMMAND,  TaintLevel.LOW),    # denied outright (the baseline's whoami)
    (ActionType.GENERATE_REPORT,  TaintLevel.MEDIUM), # allowed + ordinary scanner output
]
for action, taint in cases:
    ok, why = ap.authorize(action, taint)
    print(f"{action.value:16} taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK':6} ({why})")
EOF
cd ..
```

**What this does**: Sweeps the policy over allowed/denied actions × taint levels, with the ceiling the fixture actually uses (`max_taint_for_report: medium`).

**Expected output**:

```
report_finding   taint=low    -> ALLOW  (authorized)
report_finding   taint=medium -> ALLOW  (authorized)
report_finding   taint=high   -> BLOCK  (taint_too_high: high > medium)
exploit          taint=low    -> BLOCK  (action_denied: exploit)
exfiltrate       taint=low    -> BLOCK  (action_denied: exfiltrate)
execute_command  taint=low    -> BLOCK  (action_denied: execute_command)
generate_report  taint=medium -> ALLOW  (authorized)
```

**Why it matters**: LOW+report and MEDIUM+report ALLOW; HIGH+report BLOCKs (`taint_too_high`); exploit/exfiltrate/execute_command BLOCK at *any* taint (`action_denied`) — the `execute_command` row is exactly the instruction the baseline "followed" in Step 4. Two distinct denial reasons again — policy membership vs data quality. (A third exists for actions on neither list: `action_not_allowed`.) **Design question for notes**: denied actions are denied *unconditionally* — no taint level and no operator flag in this model can authorize `exploit`. Is that right? What governance process *should* be able to enable an exploit-class action, and where should that authorization live (code? config? human-in-the-loop approval)? Compare with Module 2's waiver mechanism — this policy has no waiver rung, deliberately. Exercise 10.5 asks you to add one, safely.

---

### Step 7: Run the test suite

```bash
cd demo-10-scanbound && python3 -m pytest tests/ -v && cd ..
```

**What this does**: Runs all 51 tests — the largest suite in the course, befitting the capstone module. Groups:

| Family | Tests | Pins |
|--------|-------|------|
| Scope (`TestScope`) | `test_scope_validation`, `test_address_ambiguity_fails_closed`, `test_wildcard_and_cidr_patterns`, `test_fixture_targets_carry_declared_protocols` | allowlist semantics; only the exact listed representation matches (suffix/prefix/case/octal variants all blocked); `*.` and CIDR are explicit opt-ins; 004/005 are `https` |
| Check validation (`TestCheckValidator`) | `…safe_check_passes`, `…unsafe_type_rejected`, `…unknown_type_fails_closed`, `…state_modification_rejected`, `…dangerous_payload_keyword_rejected`, `…all_failing_screens_are_reported`, `…ast_screen_catches_structure_without_keyword_gate` (10 payloads), `…ast_screen_skips_non_python_payloads`, `…unparseable_code_like_payload_fails_closed`, `…benign_python_is_allowed`, `…known_limit_runtime_name_resolution` | all four screens; every reason reported; AST without a keyword pre-gate, in statement mode, incl. `exec ('x')`, `import subprocess`, `builtins.eval` |
| Taint (`TestTaintTracker`) | `…canary_in_finding_text_is_high`, `…detection_reads_every_string_not_a_side_channel`, `…credential_pattern_is_high`, `…clean_output_is_medium_never_low`, `…untracked_output_fails_closed` | canary→HIGH with rule ids; `password:`→HIGH; clean→MEDIUM (never LOW); never-tracked→HIGH |
| Policy (`TestActionPolicy`) | `…taint_ceiling`, `…denied_actions_are_unconditional`, `…unlisted_action_not_allowed` | the Step 6 boundary |
| Baseline (`TestBaseline`) | `…runs_everything_and_trusts_all_output`, `…follows_injected_instructions_simulated`, `test_instruction_parser` | specimen: 7/7 run, everything LOW, `whoami`/`keys` followed (recorded) |
| End-to-end (`TestGuardedPipeline`) | `…rejected_checks_never_execute`, `…validation_happens_before_execution`, `…out_of_scope_output_is_never_read`, `…blocked_reasons`, `…tracks_taint_from_finding_text`, `…action_policy_consulted_for_every_finding`, `…never_follows_instructions`, `…events_are_in_check_order` | guarded pipeline verdicts: 4/7 executed, reasons, taint per finding, ledger with 2 reports + 2 holds |
| Results & safety (`TestResultsAndSafety`) | `…generator_matches_fixture_expectations`, `…generator_reports_a_wrong_expectation`, `…fixture_cert_date_is_not_stale`, `…no_network_or_process_imports` | the answer key holds; a doctored key yields `fail`; no socket/HTTP/subprocess import in the module |
| Exercises (`TestExercises`) | `…scope_escape`, `…poisoned_output`, `…ast_alias_gap`, `…fail_closed` | starting points for Part 5 |

```
============================== 51 passed in 0.XXs ==============================
```

**Why it matters**: `test_validation_happens_before_execution` deserves a close read: it hands the guarded scanner a spy `SimulatedScanner` and asserts that check_003/004/006 are never *asked* — the gate is proven at the call boundary, not inferred from the output. `test_rejected_checks_never_execute` pins the same fact on the real fixture (`scanner.executed == ["check_001", "check_002", "check_005", "check_007"]`). `test_address_ambiguity_fails_closed` pins that only the exact listed representation matches — `localhost.evil.example`, `LocalHost`, `0177.0.0.1`, `127.1` are all blocked — and `test_no_network_or_process_imports` pins that the module never imports a socket, HTTP or subprocess library: there is no DNS resolution to be clever with.

---

## 🎯 Part 5: Exercises

### Beginner

**Exercise 10.1 — Out-of-scope probe.**
The fixture already ships one out-of-scope check (check_006, `intranet.corp.local`). Add a second: check_008 targeting `10.0.0.5:8080` (safe type), with a canned entry in `poisoned_scanner_output` whose `details` begin `SHOULD_NEVER_BE_READ`. Re-run Step 4 and confirm the guarded run prints `BLOCKED CHECK: check_008 (host_not_allowed: 10.0.0.5) - never executed` and `Checks executed: 4/8`, while the baseline runs it (`8/8`) and reports it. Then prove the output was never looked at: from a short script, `g = build_guarded(data); scanner = SimulatedScanner(data["poisoned_scanner_output"]); g.run(load_checks(data), scanner)` and assert `check_008` is absent from `scanner.executed` and from `g.taint_tracker.taint_map` (`test_out_of_scope_output_is_never_read` does exactly this for check_006). To re-run Step 5 you must also add a `check_008` entry to the `expected` answer key (`{"baseline": ["report:check_008"], "guarded": {"executed": false, "blocked": "host_not_allowed: 10.0.0.5"}}`) — the generator looks every check up by id. Two fixture-pinned tests (`test_rejected_checks_never_execute`, `test_blocked_reasons`) will fail while check_008 is present; `git checkout -- fixtures/` restores them.

**What this teaches**: Scope is a *pre-filter* — output for blocked checks is never even looked at. Verify that in the code path (`ScopeBoundScanner.run`: the `continue` comes before `scanner.execute`).

### Standard

**Exercise 10.2 — Human-in-the-loop reporting.**
MEDIUM findings are auto-reported; HIGH findings are held with `taint_too_high` and never leave the ledger. Implement `review_and_report(findings, approvals)`: an analyst may approve a specific finding id; a held HIGH finding becomes `reported_with_review` only with *two* approvals; MEDIUM findings stay auto-reported and need none. Audit log records approver ids. Tests: HIGH+1 approval does not report; HIGH+2 does; unapproved HIGH never does; MEDIUM reports with zero approvals and is unaffected by extra ones.

**What this teaches**: Fail-closed pipelines need a *sanctioned* path to action, or operators build unsafe side-doors. Design the door with auditability built in — this is Module 2's waiver concept, human-gated.

**Exercise 10.3 — Canonical scope.**
Fix the `LocalHost` block from Step 2: canonicalize hosts (lowercase; map `127.0.0.1`↔`localhost` via a local alias table — no DNS) before matching. Add tests: `LocalHost` now allowed; `localhost.evil.example` still blocked (suffix attack — `test_address_ambiguity_fails_closed` already pins it, keep it green); `0177.0.0.1` (octal IPv4) blocked unless added to the alias map deliberately.

**What this teaches**: Allowlist canonicalization is a security function. Every alias you add is attack surface; every one you omit is a usability bug. Document your alias table's provenance.

### Extension

**Exercise 10.4 — AST depth: attribute chains and aliases.**
The AST screen matches fixed name sets — `DANGEROUS_CALLS`, `DANGEROUS_ATTRS`, `DANGEROUS_MODULES` — and never resolves a name to what it refers to. So `import subprocess as sp; sp.run(['id'])` is caught (import rule plus `.run`), but `sp = None; sp.rmtree('/')`, `shutil.rmtree('/')`, `os.remove('/etc/passwd')` and `os.unlink('/x')` are all ALLOWed (`rmtree`/`remove`/`unlink` are not in `DANGEROUS_ATTRS`), and `from subprocess import run; run(['id'])` is caught only by the import rule — the bare `run(...)` call is not attributed to `subprocess`. `test_exercise_ast_alias_gap` is the starting point. Extend `_dangerous_nodes`: track import aliases (map `as` names and `from … import` names to modules), resolve `Name`/`Attribute` chains through the alias map, and flag calls to `run/system/popen/remove/rmtree/unlink`. Tests: each new shape blocked; benign `json.dumps` and `os.path.join` still allowed (`test_benign_python_is_allowed` must stay green). Names built at runtime (`getattr(__builtins__, 'ex' + 'ec')`) stay out of reach of static analysis — say so in your notes rather than pretending otherwise.

**What this teaches**: Static analysis is an arms race of resolution. The *design* answer — resolve names through the environment before judging the call — generalizes far beyond this demo.

**Exercise 10.5 — Waiver rung for the action policy.**
Add Module 2-style waivers to `ActionPolicy`: a waiver `{action, scope, approved, expires, allowed_by_policy}` permits *one* denied action class (e.g., `modify_target` on one finding id) if: approved, unexpired, the action is in `allowed_by_policy` (never exploit/exfiltrate), and taint ≤ MEDIUM. Tests: valid waiver authorizes; expired does not; `exploit` remains unwaivable even with a valid-looking waiver; HIGH taint unwaivable.

**What this teaches**: Exceptions are policy too. The *meta*-policy (which actions may ever be waived) is more important than any individual waiver — you are encoding "some risks we accept under process; some we never accept."

---

## 📝 Lab Notes Questions

1. The baseline labels poisoned output LOW; the guarded scanner labels *all* output ≥ MEDIUM. What real-world failures does "scanner output is never fully trusted" prevent, and what operational cost does it create?
2. Step 3's four validation screens all run on every check, and every failing one is reported. Give one payload that only the AST layer catches, and explain why the keyword and type layers cannot be made sufficient no matter how many keywords you add.
3. The guarded ledger holds two reported findings and two held ones (`BLOCKED ACTION: report:check_001 (taint_too_high: high > medium)`, likewise check_007). In your own words, explain why holding those two — rather than reporting them, and rather than an empty ledger that was never consulted — is the *correct* output of a well-designed scanning pipeline, and what Exercise 10.2 adds without breaking that property.

---

## ✅ Completion Checklist

- [ ] Fixture read; seven-check prediction table completed *before* running
- [ ] Scope validator probed incl. case-sensitivity block (recorded)
- [ ] Check validator swept: every failing screen reported; AST-only payloads identified
- [ ] Baseline's all-LOW taint (and followed instructions) contrasted with guarded HIGH/MEDIUM; "same finding, different trust" recorded
- [ ] Rejected-checks-never-execute (`Checks executed: 4/7`) confirmed in demo *and* test
- [ ] Action policy boundary swept; denied-vs-taint reasons distinguished
- [ ] `results/scan_results.json` generated with `"result": "pass"` and matches predictions
- [ ] All 51 tests pass
- [ ] At least Beginner + Exercise 10.2 (human-in-the-loop) — 10.2 is essential
- [ ] `LAB_NOTES.md` Module 10 block filled (seed 42, commit, `make demo DEMO=10`)

---

**⬅️ Prev: [Module 9](lab-09-interceptbound.md) | ➡️ Next: [Module 11](lab-11-degenerate-reporting.md)**
