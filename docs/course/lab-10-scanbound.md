# Module 10: ScanBound — Vulnerability Assessment Scope Control

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Modules 4, 6, 9 (provenance, injection, taint)
**Demo directory**: `demo-10-scanbound/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Enforce** an explicit scan scope (host/port/protocol allowlists) and block out-of-scope targets *before* any check runs
2. **Validate** scanner checks for safety using type checks, state-modification flags, keyword screening, and **Python AST analysis**
3. **Taint** scanner *output* — including detecting poisoned results carrying injection canaries or credential-like strings
4. **Gate** downstream actions (report, exploit, exfiltrate…) with an action policy combining allowlists and taint ceilings
5. **Contrast** the unconstrained scanner (trusts everything, taint=LOW everywhere) with the scope-bound scanner (validates, taints, blocks) — and articulate why the *same finding* deserves different trust depending on its source

---

## 📖 Background: The Scanner That Gets Pwned

Autonomous vulnerability scanners are doubly exposed: they **act** on targets (scope risk) and they **consume** machine-generated output (poisoned-input risk). A scanner that parses plugin results as instructions, or reports whatever a hostile endpoint feeds it, becomes an attack channel:

```
   HOSTILE TARGET / PLUGIN                SCANNER PIPELINE
┌────────────────────────────────┐    ┌────────────────────────────────────┐
│ scanner output:                │    │ 1. scope:  is target allowed?      │
│  {"result":"pass",             │───►│ 2. check:  is the check safe?      │
│   "details":"Server: Apache",  │    │    (type/state/keywords/AST)       │
│   "injected":"RUN_CMD whoami"} │    │ 3. taint:  is output poisoned?     │
└────────────────────────────────┘    │ 4. policy: may we act on it?       │
                                      └────────────────────────────────────┘
```

Four gates, each answering one question:

| Gate | Question | Mechanism in this demo |
|------|----------|------------------------|
| **Scope** | May I touch this target? | Host allowlist + port allowlist + protocol allowlist |
| **Check validation** | Is this check itself safe to run? | `type != "unsafe"`, `modifies_state == False`, dangerous-keyword screen, **AST walk** rejecting `exec`/`eval`/`subprocess`/`os.system`/dangerous imports |
| **Taint tracking** | Is this *output* trustworthy? | HIGH if injection canary or credential pattern; else MEDIUM (scanner output is never LOW) |
| **Action policy** | May we act on this finding? | Allowed-actions set + denied-actions set + taint ceiling (`report` requires LOW) |

**The baseline's signature failure**: it labels *all* scanner output `taint=LOW` — including output carrying `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI`. Wrong trust at the leaf poisons every decision above it.

**Safety framing**: targets are `localhost`, `127.0.0.1`, `scan-target.local`. Checks are *simulated* — the fixture's `poisoned_scanner_output` *is* the "result." Nothing leaves your machine; `make verify-safety` holds. This module teaches the *governance layer* around scanning, never scanning itself.

### The five checks

| ID | Name | Type | Target | Payload | Modifies state? |
|----|------|------|--------|---------|-----------------|
| check_001 | info_disclosure | safe | localhost:8080 | `GET /server-info` | no |
| check_002 | xss_test | safe | scan-target.local:80 | `<script>alert(1)</script>` | no |
| check_003 | sql_injection | **unsafe** | localhost:8080 | `' OR '1'='1` | **yes** |
| check_004 | rce_attempt | **unsafe** | 127.0.0.1:8443 | `; rm -rf /` | **yes** |
| check_005 | ssl_check | safe | 127.0.0.1:8443 | TLS handshake | no |

And the poisoned outputs: check_001 carries `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI`; check_004 carries `CANARY_SCANNER_INJECTION_EXFILTRATE_KEYS`.

---

## 🛠️ Part 1: Fixtures and Predictions

### Step 1: Read the fixture

```bash
cat demo-10-scanbound/fixtures/scanbound.json
```

**What this does**: Prints target scope, mock services, the five checks, poisoned outputs, and the downstream policy (allowed: report/generate_report; denied: exploit/exfiltrate/modify_target/execute_command; max taint for report: LOW).

**Why it matters**: Fill the prediction table *before* running:

| Check | In scope? | Passes validation? | Output taint | Final disposition (guarded) |
|-------|-----------|--------------------|--------------|------------------------------| 
| check_001 | ? | ? | ? | ? |
| check_002 | ? | ? | ? | ? |
| check_003 | ? | ? | ? | ? |
| check_004 | ? | ? | ? | ? |
| check_005 | ? | ? | ? | ? |

Reasoning hints: check_003/004 are `type: "unsafe"` *and* `modifies_state: true` — two independent validation failures. check_001 and check_004's outputs carry injection canaries → taint HIGH. And since `report` requires taint LOW, **no finding in this fixture can be auto-reported** — every output is MEDIUM or HIGH. Is that a bug or the correct conservative default? Hold that question for Step 6.

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
cd ../..
```

**What this does**: Sweeps the scope validator with seven cases, including a case-sensitivity probe.

**Why it matters**: Six rows should be OK; the `LocalHost` row likely *mismatches* (exact string match → blocked, which is safe-direction but a usability bug). Record it: **exact-match scope is fail-closed but brittle**. Module 6 Exercise 6.3 had you canonicalize hostnames; same fix applies here (Exercise 3). The deeper point: every allowlist match is a *representation* comparison, and representations have edge cases — case, encoding, aliases (`127.0.0.1` vs `localhost` vs `0177.0.0.1`).

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
    ("import subprocess",           "safe",  False),   # AST: Import
    ("__import__('os').system('x')","safe",  False),   # AST: dunder import
    ("os.system('id')",             "safe",  False),   # keyword os. + AST
]
for payload, ctype, state in cases:
    ok, why = cv.validate(mk(payload, ctype, state))
    print(f"{'ALLOW' if ok else 'BLOCK':6} {why:32} {payload[:34]}")
EOF
cd ../..
```

**What this does**: Sweeps the check validator across eight payloads: benign, type-flagged, state-flagged, keyword-flagged, and four AST-detectable code shapes.

**Why it matters**: Everything except row 1 should BLOCK, each with a *distinct reason*: `check_type_unsafe`, `modifies_state`, `dangerous_payload_keyword: rm -rf`, `dangerous_ast_pattern`. The four AST rows are the teaching core: **keyword screens catch strings; AST catches structure.** `__import__('os')` contains no banned keyword — only parsing the expression reveals the call. This is the same string-vs-semantics gap you met in Module 1 (string oracles vs AST oracles) and Module 8 Exercise 8.5 (template grammar). The pattern recurs because the attack recurs: *smuggle semantics inside innocent-looking text.*

**Also note the layering**: type flag → state flag → AST → keywords. Four cheap-to-expensive screens in escalating order. Ask in notes: why does order matter for cost, and why does having *redundant* layers matter for robustness?

---

## 🤖 Part 3: Baseline vs Guarded, End to End

### Step 4: Run both scanners

```bash
cd demo-10-scanbound && python3 student/scanbound.py && cd ../..
```

**What this does**: Runs the full demo: unconstrained baseline, then scope-bound guarded scanner.

**Why it matters** — the contrast, side by side:

**Baseline** (expected): all five checks "run," every finding labeled `taint: low` — including check_001's output carrying `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI`. Nothing blocked. Nothing flagged.

**Guarded** (expected):
```
check_001 … (taint: high)      ◄── canary detected, taint escalated
check_002 … (taint: medium)
check_003 … (taint: medium)    + BLOCKED CHECK (check_type_unsafe)
check_004 … (taint: high)      + BLOCKED CHECK (check_type_unsafe)
check_005 … (taint: medium)
```

Three observations to record:
1. **Blocked checks still got taint-tracked.** The guarded scanner records check_003/004's output taint *and* blocks them. Validation blocks *execution/forwarding*; tracking still observes. You keep the forensic trail without acting on it.
2. **Same finding, different trust.** check_001's "Server: Apache" is identical text in both scanners; baseline says trust it (LOW), guarded says HIGH (canary). The *finding* didn't change — the *epistemics* did. This is the module's version of Module 9's "observe ≠ act."
3. **No finding is reportable.** All taints are MEDIUM/HIGH; report needs LOW; so `actions_taken` is empty. The pipeline ends safely *by default*, and Exercise 2 makes you design the sanctioned path by which a human turns a MEDIUM finding into a report.

---

### Step 5: Generate the results artifact

```bash
cd demo-10-scanbound && python3 student/generate_scan_results.py && cd ../..
cat demo-10-scanbound/results/scan_results.json
```

**What this does**: Runs the guarded scanner and writes `results/scan_results.json`: per-check findings with taint, blocked checks with reasons, and action ledgers.

**Why it matters**: Verify against Step 1 predictions: 5 findings (all checks tracked), 2 blocked (003/004, `check_type_unsafe`), `actions_taken: []`. This file is your lab evidence and the input to Exercise 1's out-of-scope probe.

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
    max_taint=TaintLevel.LOW,
)
cases = [
    (ActionType.REPORT_FINDING,   TaintLevel.LOW),    # allowed + clean
    (ActionType.REPORT_FINDING,   TaintLevel.MEDIUM), # allowed + dirty
    (ActionType.REPORT_FINDING,   TaintLevel.HIGH),
    (ActionType.EXPLOIT,          TaintLevel.LOW),    # denied outright
    (ActionType.EXFILTRATE,       TaintLevel.LOW),    # denied outright
    (ActionType.GENERATE_REPORT,  TaintLevel.LOW),    # allowed + clean
]
for action, taint in cases:
    ok, why = ap.authorize(action, taint)
    print(f"{action.value:16} taint={taint.value:6} -> {'ALLOW' if ok else 'BLOCK':6} ({why})")
EOF
cd ../..
```

**What this does**: Sweeps the policy over allowed/denied actions × taint levels.

**Why it matters**: Expected: LOW+report ALLOWs; MEDIUM/HIGH+report BLOCKs (`taint_too_high`); exploit/exfiltrate BLOCK at *any* taint (`action_denied`). Two distinct denial reasons again — policy membership vs data quality. **Design question for notes**: denied actions are denied *unconditionally* — no taint level and no operator flag in this model can authorize `exploit`. Is that right? What governance process *should* be able to enable an exploit-class action, and where should that authorization live (code? config? human-in-the-loop approval)? Compare with Module 2's waiver mechanism — this policy has no waiver rung, deliberately. Exercise 5 asks you to add one, safely.

---

### Step 7: Run the test suite

```bash
cd demo-10-scanbound && python3 -m pytest tests/ -v && cd ../..
```

**What this does**: Runs all 21 tests — the largest suite, befitting the capstone module. Groups:

| Family | Tests | Pins |
|--------|-------|------|
| Scope | `test_scope_validation`, `test_address_ambiguity_prevented` | allowlist semantics; explicit hosts only, no wildcard resolution |
| Check validation | `…unsafe_type_rejected`, `…state_modification_rejected`, `…dangerous_payload_rejected`, `…ast_detection` | all four screens, incl. AST `exec` |
| Taint | `…injection`, `…credentials`, `…default_medium` | canary→HIGH; `password:`→HIGH; clean→MEDIUM (never LOW) |
| Baseline | `test_unconstrained_trusts_all_output` | specimen: everything LOW |
| End-to-end | `…out_of_scope`, `…unsafe_checks`, `…tracks_taint` | guarded pipeline verdicts incl. blocked-checks-still-tracked |
| Policy | `…high_taint`, `…denied_actions` | the Step 6 boundary |

**Why it matters**: `test_guarded_tracks_taint` deserves a close read: it asserts check_004 (an *unsafe, blocked* check) still appears in results with HIGH taint. That assertion *is* observation-vs-action, encoded. And `test_address_ambiguity_prevented` pins that only explicitly-listed names resolve — no clever DNS or aliasing.

---

## 🎯 Part 5: Exercises

### Beginner

**Exercise 10.1 — Out-of-scope probe.**
Add check_006 targeting `intranet.corp.local:80` (safe type, clean output). Re-run Step 5 and confirm it lands in `blocked_checks` with `host_not_allowed`. Then add its output to `poisoned_scanner_output` anyway and confirm the guarded scanner never taints or reports it.

**What this teaches**: Scope is a *pre-filter* — output for blocked checks is never even looked at. Verify that in the code path.

### Standard

**Exercise 10.2 — Human-in-the-loop reporting.**
Currently no finding can be reported (all taint > LOW). Implement `review_and_report(findings, approvals)`: an analyst may approve a specific finding id; approved MEDIUM findings become `reported_with_review`, HIGH findings require *two* approvals. Audit log records approver ids. Tests: MEDIUM+1 approval reports; HIGH+1 does not; HIGH+2 does; unapproved never does.

**What this teaches**: Fail-closed pipelines need a *sanctioned* path to action, or operators build unsafe side-doors. Design the door with auditability built in — this is Module 2's waiver concept, human-gated.

**Exercise 10.3 — Canonical scope.**
Fix the `LocalHost` mismatch from Step 2: canonicalize hosts (lowercase; map `127.0.0.1`↔`localhost` via a local alias table — no DNS) before matching. Add tests: `LocalHost` now allowed; `localhost.evil.com` still blocked (suffix attack); `0177.0.0.1` (octal IPv4) blocked unless added to the alias map deliberately.

**What this teaches**: Allowlist canonicalization is a security function. Every alias you add is attack surface; every one you omit is a usability bug. Document your alias table's provenance.

### Extension

**Exercise 10.4 — AST depth: attribute chains and aliases.**
The current AST check misses `subprocess` reached via alias (`import subprocess as sp; sp.run(...)`) and attribute chains (`os.path.rmtree`). Extend `_has_dangerous_nodes`: track import aliases (map `as` names to modules), resolve `Name`/`Attribute` chains through the alias map, and flag calls to `run/system/popen/remove/rmtree/unlink`. Tests: each new shape blocked; benign `json.dumps` and `os.path.join` still allowed.

**What this teaches**: Static analysis is an arms race of resolution. The *design* answer — resolve names through the environment before judging the call — generalizes far beyond this demo.

**Exercise 10.5 — Waiver rung for the action policy.**
Add Module 2-style waivers to `ActionPolicy`: a waiver `{action, scope, approved, expires, allowed_by_policy}` permits *one* denied action class (e.g., `modify_target` on one finding id) if: approved, unexpired, the action is in `allowed_by_policy` (never exploit/exfiltrate), and taint ≤ MEDIUM. Tests: valid waiver authorizes; expired does not; `exploit` remains unwaivable even with a valid-looking waiver; HIGH taint unwaivable.

**What this teaches**: Exceptions are policy too. The *meta*-policy (which actions may ever be waived) is more important than any individual waiver — you are encoding "some risks we accept under process; some we never accept."

---

## 📝 Lab Notes Questions

1. The baseline labels poisoned output LOW; the guarded scanner labels *all* output ≥ MEDIUM. What real-world failures does "scanner output is never fully trusted" prevent, and what operational cost does it create?
2. Step 3's four validation screens are layered cheap-to-expensive. Give one payload that only the AST layer catches, and explain why the keyword and type layers cannot be made sufficient no matter how many keywords you add.
3. `actions_taken` is empty for the whole fixture. In your own words, explain why an empty action ledger can be the *correct* output of a well-designed scanning pipeline, and what Exercise 10.2 adds without breaking that property.

---

## ✅ Completion Checklist

- [ ] Fixture read; five-check prediction table completed *before* running
- [ ] Scope validator probed incl. case-sensitivity mismatch (recorded)
- [ ] Check validator swept: four distinct rejection reasons observed; AST-only payloads identified
- [ ] Baseline's all-LOW taint contrasted with guarded HIGH/MEDIUM; "same finding, different trust" recorded
- [ ] Blocked-checks-still-tracked behavior confirmed in demo *and* test
- [ ] Action policy boundary swept; denied-vs-taint reasons distinguished
- [ ] `results/scan_results.json` generated and matches predictions
- [ ] All 21 tests pass
- [ ] At least Beginner + Exercise 10.2 (human-in-the-loop) — 10.2 is essential
- [ ] `LAB_NOTES.md` Module 10 block filled (seed 42, commit, `make demo DEMO=10`)

---

**⬅️ Prev: [Module 9](lab-09-interceptbound.md) | ➡️ Next: [Final Assessment](lab-11-final-assessment.md)**
