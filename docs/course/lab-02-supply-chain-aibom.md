# Module 2: Supply Chain & AIBOM Drift

**Duration**: 1 hour | **Difficulty**: ⭐⭐ | **Prerequisites**: Module 0 (Module 1 recommended)
**Demo directory**: `demo-02-supply-chain-aibom/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Define** an AI Bill of Materials (AIBOM) and explain how it differs from a classic SBOM
2. **Model** agent capabilities as structured strings (`action:resource:scope`) and match them with prefix wildcards
3. **Implement** a fail-closed policy gate with correct precedence: allow → waiver → deny → default-deny
4. **Design** waivers that are scoped, approved, *and* time-limited — and explain why each property is necessary
5. **Explain** least-privilege analysis and identify over-privileged capabilities in a runtime set

---

## 📖 Background: When Reality Drifts from the Manifest

A classic SBOM lists the software components in a product. An **AIBOM** extends this to agentic systems: it declares not just libraries, but *what the agent is allowed to do* — which files it may read, which tools it may execute, which network endpoints it may contact.

The security failure mode is **drift**: the running system's actual capabilities exceed the declaration. Drift happens innocently (a developer adds a tool during debugging and forgets to update the manifest) and maliciously (a compromised dependency quietly requests new permissions).

```
   DECLARED (AIBOM)                RUNTIME (observed)
   ─────────────────               ──────────────────────
   read:files:/workspace/*         read:files:/workspace/*        ✅ match
   write:files:/workspace/out/*    write:files:/workspace/out/*   ✅ match
   exec:tools:parser,validator     exec:tools:parser,validator,   ⚠️ DRIFT!
   net:http:api.internal/*         net:http:api.internal/*           scanner added
```

The defense is a **policy gate** that sits between "capabilities requested" and "capabilities granted," with a strict decision procedure:

```
        capability requested
                │
                ▼
     ┌─────────────────────┐
     │ matches ALLOW list? │──yes──► GRANT (explicitly_allowed)
     └─────────┬───────────┘
               │ no
               ▼
     ┌─────────────────────┐
     │ valid WAIVER covers │──yes──► GRANT (waiver_granted)
     │ this scope?         │        [must be: approved by a named approver
     └─────────┬───────────┘         + in force at evaluation time
               │ no                  + no longer than max_duration_hours
               ▼                     + scope listed in waiver_rules]
     ┌─────────────────────┐
     │ matches DENY list?  │──yes──► DENY (explicitly_denied)
     └─────────┬───────────┘
               │ no
               ▼
            DENY  ◄── fail-closed: not_allowed_default_deny
```

**The precedence order is the whole lesson.** Allow before waiver (explicit grants beat exceptions), waiver before deny (a *properly scoped, policy-sanctioned* waiver can lift a deny — but only for scopes the waiver rules explicitly permit), deny before default (explicit prohibitions are enforced), default deny always.

The gate answers a second question separately from that ladder: **drift** — does the runtime use anything the AIBOM does not declare? Compliance is a policy decision; drift is a fact about the manifest. A waiver can make drift *compliant*; it never removes it from the report.

---

## 🛠️ Part 1: Read the AIBOM and Policy

### Step 1: Inspect the AIBOM fixture

```bash
cat demo-02-supply-chain-aibom/fixtures/aibom.json
```

**What this does**: Prints the full fixture: components, declared agent capabilities, policy (allowed/denied/waiver rules), the pinned evaluation time, and four drift scenarios.

**Why it matters**: Map the structure in your notes:

| Section | Purpose |
|---------|---------|
| `aibom.components` | Declared libraries/tools with version + hash (listed only — this demo never checks the hashes) |
| `aibom.agent_capabilities` | The *declared* capability set (the manifest) — anything the runtime uses beyond it is **drift** |
| `aibom.policy.allowed_capabilities` | What the gate grants outright |
| `aibom.policy.denied_capabilities` | Hard prohibitions (`exec:shell:*`, `write:files:/etc/*`) — and `exec:tools:scanner` |
| `aibom.policy.waiver_rules` | Governance: max duration (24 h), approval required, **which scopes are even waivable** — all three are enforced |
| `evaluation_time` | The clock every scenario is judged against (`2025-01-14T12:00:00Z`), so waiver validity is reproducible |
| `drift_scenarios[]` | The four test cases you're about to run |

**Key detail**: `waiver_rules.allowed_scopes` contains only `exec:tools:scanner` and `net:http:specific.host`. This means *no waiver can ever authorize* `exec:shell:*` or `write:files:/etc/*`. The waivable surface itself is a policy decision — this is governance, not just code. Notice that `exec:tools:scanner` is on the deny list *and* on the waivable list: `drifted-002` and `valid-waiver-004` are the same drift, with and without a valid waiver.

---

### Step 2: Understand the capability string grammar

```bash
grep -n "def expand_capability\|def match_pattern" demo-02-supply-chain-aibom/student/policy_gate.py
```

**What this does**: Locates the two functions that turn capability strings into decisions:

```
31:def expand_capability(cap: str) -> List[str]:
45:def match_pattern(pattern: str, cap: str) -> bool:
```

`expand_capability` splits a composite tool list into one capability per tool; `match_pattern` does the wildcard matching.

**Why it matters**: Capabilities use a simple grammar: `action:resource:scope`, where a trailing `*` is a prefix wildcard. Test your understanding against these examples *before* running anything (write predictions in your notes):

| Pattern | `read:files:/workspace/a.txt` | `read:files:/etc/passwd` |
|---------|-------------------------------|--------------------------|
| `read:files:/workspace/*` | ✅ matches | ❌ no |

| Pattern | `exec:tools:scanner` |
|---------|----------------------|
| `exec:tools:scanner` | ✅ exact match |
| `exec:tools:*` | ✅ prefix match |

Now the subtle one — in `drifted-002` the runtime capability is `exec:tools:parser,validator,scanner` while the allow list has `exec:tools:parser,validator`. Neither string is matched whole: `expand_capability` splits both on commas into one capability per tool, so `exec:tools:parser` and `exec:tools:validator` each match the allow list and `exec:tools:scanner` is judged on its own — where it meets the deny list. Matching per tool is what makes least privilege work in both directions: a runtime with *fewer* tools than declared (`exec:tools:parser` alone, or the same tools in a different order) is neither drift nor a violation (`test_subset_of_declared_tools_is_allowed`). Only `exec:tools:` lists are expanded — a comma-separated *host* list is still matched as one opaque string, and Exercise 2.3 (standard) has you close that gap.

---

## ⚙️ Part 2: Run the Policy Gate on All Scenarios

### Step 3: Execute the gate

```bash
cd demo-02-supply-chain-aibom && python3 student/policy_gate.py && cd ..
```

**What this does**: Instantiates `PolicyGate` from the fixture and prints the expanded declared capability set and the pinned evaluation time. Then, for each of the four drift scenarios, it prints a drift line (which runtime capabilities are undeclared), the waiver verdict where the scenario supplies a waiver, per-capability ALLOW/DENY verdicts with reasons, the compliance verdict, and a ✓/✗ against the scenario's expectation.

**Why it matters**: This is your first live view of the precedence ladder from the background section. Read each scenario's output against the flowchart.

**Expected output** (annotated):

```
Declared capabilities (AIBOM): ['exec:tools:parser', 'exec:tools:validator', 'net:http:api.internal/*', 'read:files:/workspace/*', 'write:files:/workspace/output/*']
Evaluation time: 2025-01-14T12:00:00Z (fixed by the fixture for reproducibility)
```
The declared `exec:tools:parser,validator` has already become two capabilities. Every timestamp check below is made against 2025-01-14T12:00Z, not your wall clock.

```
=== compliant-001: System matches declared AIBOM ===
Drift detected: False
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: write:files:/workspace/output/* (explicitly_allowed)
  ALLOW: exec:tools:parser (explicitly_allowed)
  ALLOW: exec:tools:validator (explicitly_allowed)
  ALLOW: net:http:api.internal/* (explicitly_allowed)
Compliant: True
✓ Matches expected: PASS
```
All five expanded capabilities sit on the allow list, and nothing is undeclared. No waiver needed. Trivial case — but it proves the gate doesn't over-block.

```
=== drifted-002: Agent gained scanner execution capability ===
Drift detected: True (undeclared: exec:tools:scanner)
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: write:files:/workspace/output/* (explicitly_allowed)
  ALLOW: exec:tools:parser (explicitly_allowed)
  ALLOW: exec:tools:validator (explicitly_allowed)
  DENY: exec:tools:scanner (explicitly_denied)
  ALLOW: net:http:api.internal/* (explicitly_allowed)
Compliant: False
✓ Matches expected: BLOCKED
```
The composite tool list is expanded, so `parser` and `validator` stay allowed and only `exec:tools:scanner` is judged on its own: it misses allow, misses waiver (none supplied), and hits the deny list's exact entry `exec:tools:scanner` → **`explicitly_denied`**. The drift line reports the same capability as undeclared. Note the reason string — the gate *tells you* which rung fired, which is exactly what you want in an audit log. (`not_allowed_default_deny` is the rung for capabilities on neither list — add `exec:tools:formatter` to a runtime set and you will see it.)

```
=== invalid-waiver-003: Waiver for shell access without approval ===
Drift detected: True (undeclared: exec:shell:*)
Waiver exec:shell:*: REJECTED: not approved; scope exec:shell:* is not waivable
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  DENY: exec:shell:* (explicitly_denied)
Compliant: False
✓ Matches expected: WAIVER REJECTED
```
The gate prints every reason the waiver fails, and there are two independent ones: the waiver has `approved: false`, **and** `exec:shell:*` isn't in `waiver_rules.allowed_scopes`. Even an approved, unexpired waiver couldn't authorize this scope. Defense in depth. With the waiver out of the way, `exec:shell:*` hits the deny list.

```
=== valid-waiver-004: Properly scoped, approved, time-limited waiver ===
Drift detected: True (undeclared: exec:tools:scanner)
Waiver exec:tools:scanner: ACCEPTED
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: exec:tools:scanner (waiver_granted)
Compliant: True
✓ Matches expected: WAIVER ACCEPTED
```
The waiver is approved by a named approver (`security-lead@example.com`), in force at the evaluation time (issued `2025-01-14T09:00Z`, expires `2025-01-15T09:00Z` — a 24-hour lease, exactly `max_duration_hours`), and its scope `exec:tools:scanner` is in the waivable list. All conditions satisfied → the deny-list entry for `exec:tools:scanner` is lifted and the capability is granted with reason `waiver_granted`. Read the two verdict lines together: **`Drift detected: True` and `Compliant: True`**. The waiver sanctions the drift; it does not erase it.

---

### Step 4: Trace one decision by hand

Open `demo-02-supply-chain-aibom/student/policy_gate.py` and find `check_capability`. 

**What to do**: `evaluate_system` expands `drifted-002`'s `exec:tools:parser,validator,scanner` into three capabilities before calling `check_capability` on each one. Take `exec:tools:scanner`, walk the method line by line and write in your notes which branch fires and why. Confirm your trace matches the `explicitly_denied` output from Step 3, then repeat for `exec:tools:parser` (`explicitly_allowed`).

**Why it matters**: Being able to *hand-execute* the policy engine is the difference between "I ran the demo" and "I understand the demo." This trace is also your study sheet for the final quiz.

---

## ⏰ Part 3: Explore Waiver Expiry

### Step 5: Test the expiry boundary

```bash
cd demo-02-supply-chain-aibom && python3 - << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, "student")
from policy_gate import PolicyGate, Waiver

gate = PolicyGate(Path("fixtures/aibom.json"))   # evaluation_time pinned at 2025-01-14T12:00Z
caps = ["exec:tools:scanner"]

for label, issued, expires in [("expired",  "2025-01-13T09:00:00Z", "2025-01-14T09:00:00Z"),
                               ("in force", "2025-01-14T09:00:00Z", "2025-01-15T09:00:00Z"),
                               ("too long", "2025-01-14T09:00:00Z", "2025-01-21T09:00:00Z")]:
    w = Waiver("exec:tools:scanner", "audit scan", True, expires, issued, "security-lead@example.com")
    r = gate.evaluate_system(caps, w)
    print(f"{label:9} -> compliant={r['compliant']}  {r['waiver']['reasons']}")
EOF
cd ..
```

**What this does**: Evaluates the *same* capability with the *same* approved, scoped waiver three times, differing only in the `issued`/`expires` timestamps — all judged against the fixture's pinned clock.

**Why it matters**: Output should be:
```
expired   -> compliant=False  ['expired at 2025-01-14T09:00:00Z']
in force  -> compliant=True  []
too long  -> compliant=False  ['duration exceeds max_duration_hours=24']
```
A waiver is a *lease*, not a grant — and the lease length is policy (`max_duration_hours`), not the requester's choice: the third waiver is approved, scoped and unexpired, yet a week-long lease is rejected. `Waiver.validate()` compares `issued` and `expires` against the evaluation time (timezone-aware) and returns *every* reason for rejection, not just the first. Because the fixture pins `evaluation_time`, this experiment gives the same answer every day; against the real clock the fixture's 2025 waiver has already lapsed — Step 7 shows that. **Time is an attack surface**: an unmonitored waiver quietly becomes a permanent hole the day it expires, unless something re-checks. Exercise 2.2 has you build that monitor.

---

## 🧵 Part 4: Run the Tests

### Step 6: Run Demo 02's test suite

```bash
cd demo-02-supply-chain-aibom && python3 -m pytest tests/ -v && cd ..
```

**What this does**: Runs all 17 tests (expect `17 passed`). The key ones:

| Test | Proves |
|------|--------|
| `test_compliant_system_passes` | Gate doesn't over-block legitimate capability sets: no drift, every reason `explicitly_allowed` |
| `test_drifted_system_blocked` | Extra tool → drift *and* non-compliant, with `exec:tools:scanner` specifically `explicitly_denied` while `parser`/`validator` stay allowed |
| `test_subset_of_declared_tools_is_allowed` | Running with *fewer* tools than declared (or the same tools reordered) is neither drift nor a violation |
| `test_invalid_waiver_rejected` | Unapproved waiver for an unwaivable scope is rejected for *both* reasons |
| `test_unapproved_waiver_for_waivable_scope_rejected` | Approval is checked on its own: same waivable scope, only `approved` (or the approver name) differs |
| `test_valid_waiver_accepted` | Fully-valid waiver grants, with reason `waiver_granted` — and the scanner is still reported as drift |
| `test_expired_waiver_rejected` | Time boundary enforced: the fixture's waiver is rejected against the real clock, valid at the pinned time |
| `test_waiver_duration_limit_enforced` | An otherwise valid waiver that expires in 2099 is rejected: `max_duration_hours` is policy, not the requester's choice |
| `test_waiver_without_issue_time_rejected` | No `issued` timestamp → the duration cannot be checked → fail closed |
| `test_unwaivable_scope_stays_denied` | **Critical**: `write:files:/etc/passwd` denied even with a well-formed waiver for `write:files:/etc/*` — because `/etc/*` is not in the waivable scopes |
| `test_least_privilege_analysis` | The deny list actually blocks `exec:shell:bash`, `write:files:/etc/passwd` and `net:http:evil.example/*`; the specific allow `net:http:api.internal/v1` beats the broad `net:http:*` deny because allow is checked first |
| `test_scenarios_behave_as_labelled` | Every fixture scenario's outcome is computed and matches its `expected` label |
| `test_github_actions_validation_script` | `validate_aibom.py` exits 0 for `compliant-001`, 1 for `drifted-002`, 1 for `valid-waiver-004 --now now`, 2 for an unknown scenario; `--self-test` exits 0 |

**Why it matters**: `test_unwaivable_scope_stays_denied` is the rung to study. A valid waiver *does* override an explicit deny — that is exactly how `valid-waiver-004` gets `exec:tools:scanner` past the deny list — so what protects the deny list is not the ordering but `waiver_rules.allowed_scopes`. Waivers are powerful, so the *power to waive* is itself restricted. If your Step 4 trace didn't cover this path, trace it now.

---

## 🔄 Part 5: CI Integration

### Step 7: Run the CI validator directly

```bash
cd demo-02-supply-chain-aibom
python3 student/validate_aibom.py --scenario compliant-001; echo "exit code: $?"
python3 student/validate_aibom.py --scenario drifted-002; echo "exit code: $?"
python3 student/validate_aibom.py --self-test; echo "exit code: $?"
python3 student/validate_aibom.py --scenario valid-waiver-004 --now now; echo "exit code: $?"
cd ..
```

**What this does**: Runs the standalone validator that a GitHub Actions workflow would invoke. Unlike Step 3, it validates *one* observed runtime capability set: `--scenario ID` takes the set (and any waiver) from a fixture scenario; in a pipeline you would pass `--runtime observed.json` (`{"runtime_capabilities": [...], "waiver": {...}}`). Exit codes: `0` = compliant, `1` = non-compliant, `2` = error. `--self-test` (also what you get with no arguments) instead re-evaluates all four scenarios and exits 0 only if each behaves as its `expected` field says. The clock defaults to the fixture's `evaluation_time`; `--now now` uses the real clock.

**Expected output** (the last timestamp is your wall clock):

```
compliant-001: COMPLIANT (evaluated at 2025-01-14T12:00:00+00:00)
exit code: 0
DENY: exec:tools:scanner (explicitly_denied)
drift: undeclared capabilities ['exec:tools:scanner']
drifted-002: NON-COMPLIANT (evaluated at 2025-01-14T12:00:00+00:00)
exit code: 1
self-test: 4/4 scenarios behave as their expected label
exit code: 0
DENY: exec:tools:scanner (explicitly_denied)
drift: undeclared capabilities ['exec:tools:scanner']
waiver exec:tools:scanner rejected: expired at 2025-01-15T09:00:00Z
valid-waiver-004: NON-COMPLIANT (evaluated at 2026-08-27T17:01:39.055212+00:00)
exit code: 1
```

**Why it matters**: This is the bridge from teaching demo to practice. In a real pipeline, the "runtime capabilities" input would come from observing the live agent (instrumented tool calls), and the non-zero exit on `drifted-002` is what blocks the deploy. The last command shows the other way a deploy gets blocked: judged against today's clock instead of the pinned one, the 2025 waiver has lapsed and the same `valid-waiver-004` runtime is non-compliant — the "silent permanent hole" from Step 5, caught. You now know both ends: the gate (Step 3) and the gate's CI harness (this step).

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 2.1 — Add a network-drift scenario.**
Add `drifted-005` to the fixture: runtime gains `net:http:evil.example/*` on top of the compliant set. Set `expected: "block"`. Re-run Step 3. Which reason string fires? (Prediction: `not_allowed_default_deny` — `net:http:evil.example/*` matches no allow, and `net:http:*` in the deny list *does* match... verify which one actually fires and explain the precedence.) Check the `Drift detected` line too: the new capability is undeclared as well as denied.

**What this teaches**: Reason strings are audit evidence. Learning to *predict* them means you've internalized the ladder.

### Standard

**Exercise 2.2 — Waiver expiry monitor.**
Write `student/waiver_monitor.py`: given a list of waivers, print each as `EXPIRED`, `EXPIRES_IN_<24H` (action needed), or `VALID`, and exit non-zero if any waiver is expired *but its capability still appears in a runtime set you pass in*. This models the "silent permanent hole" failure.

**What this teaches**: Policies decay. Monitoring the *policy objects themselves* is as important as enforcing them at gate time.

**Exercise 2.3 — Generalize per-tool matching to host lists.**
`expand_capability` only splits `exec:tools:` lists. As shipped, the gate therefore matches `net:http:api.internal/v1,evil.example` as one string — and the `net:http:api.internal/*` allow pattern is a prefix of it, so the whole thing comes back `explicitly_allowed`. Confirm that with `gate.check_capability(...)` first. Then extend `expand_capability` so a comma-separated host list is split and each host checked individually against patterns, and add a test for that mixed case: `api.internal/v1` allowed, `evil.example` reported as denied on its own line.

**What this teaches**: Grammar design flaws become policy bypasses. Composite fields need composite handling.

### Extension

**Exercise 2.4 — Waiver justification quality gate.**
Extend `Waiver.validate()`: reject waivers whose `justification` is under 20 characters or matches a placeholder pattern (`TODO`, `test`, `N/A`), returning the reason alongside the existing ones. Add fixtures: one rejected for weak justification, one accepted. Defend your minimum length in lab notes — what attack does this actually slow down?

**What this teaches**: Governance controls (approval, justification) are only as strong as their weakest verification. Think about who reviews and what "review" means under deadline pressure.

---

## 📝 Lab Notes Questions

1. Explain the four-rung precedence ladder (allow → waiver → deny → default-deny) and give one concrete attack each rung prevents.
2. Why must `waiver_rules.allowed_scopes` exist at all? What would go wrong if any scope could be waived?
3. Your Step 5 experiment showed time silently flips a waiver from valid to expired. Describe where this check should live in a production system (gate-time? cron? both?) and why.
4. `valid-waiver-004` is reported as *both* `Drift detected: True` and `Compliant: True`. Why should a waiver never remove a capability from the drift report? What would an auditor lose if it did?

---

## ✅ Completion Checklist

- [ ] AIBOM structure mapped in lab notes
- [ ] Capability grammar understood; prefix-match predictions written *before* running
- [ ] All four scenarios run; each ✓ Matches expected
- [ ] Hand-trace of `drifted-002` recorded
- [ ] Expiry boundary experiment run (expired vs in force vs too long)
- [ ] All 17 tests pass
- [ ] CI validator exits 0 for `compliant-001` and 1 for `drifted-002`
- [ ] At least Beginner exercise; Standard 2.3 strongly recommended
- [ ] `LAB_NOTES.md` Module 2 block filled with reproducibility fields (seed 42, commit, `make demo DEMO=02`)

---

**⬅️ Prev: [Module 1](lab-01-blind-verification.md) | ➡️ Next: [Module 3: Evaluation Invariants](lab-03-eval-invariants.md)**
