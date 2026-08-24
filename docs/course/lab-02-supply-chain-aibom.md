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
     │ this scope?         │        [must be: approved + unexpired
     └─────────┬───────────┘         + scope listed in waiver_rules]
               │ no
               ▼
     ┌─────────────────────┐
     │ matches DENY list?  │──yes──► DENY (explicitly_denied)
     └─────────┬───────────┘
               │ no
               ▼
            DENY  ◄── fail-closed: not_allowed_default_deny
```

**The precedence order is the whole lesson.** Allow before waiver (explicit grants beat exceptions), waiver before deny (a *properly scoped, policy-sanctioned* waiver can lift a deny — but only for scopes the waiver rules explicitly permit), deny before default (explicit prohibitions are enforced), default deny always.

---

## 🛠️ Part 1: Read the AIBOM and Policy

### Step 1: Inspect the AIBOM fixture

```bash
cat demo-02-supply-chain-aibom/fixtures/aibom.json
```

**What this does**: Prints the full fixture: components, declared agent capabilities, policy (allowed/denied/waiver rules), and four drift scenarios.

**Why it matters**: Map the structure in your notes:

| Section | Purpose |
|---------|---------|
| `aibom.components` | Declared libraries/tools with version + hash |
| `aibom.agent_capabilities` | The *declared* capability set (the manifest) |
| `aibom.policy.allowed_capabilities` | What the gate grants outright |
| `aibom.policy.denied_capabilities` | Hard prohibitions (`exec:shell:*`, `write:files:/etc/*`) |
| `aibom.policy.waiver_rules` | Governance: max duration, approval required, **which scopes are even waivable** |
| `drift_scenarios[]` | The four test cases you're about to run |

**Key detail**: `waiver_rules.allowed_scopes` contains only `exec:tools:scanner` and `net:http:specific.host`. This means *no waiver can ever authorize* `exec:shell:*` or `write:files:/etc/*`. The waivable surface itself is a policy decision — this is governance, not just code.

---

### Step 2: Understand the capability string grammar

```bash
grep -n "_match_pattern" demo-02-supply-chain-aibom/student/policy_gate.py
```

**What this does**: Locates the wildcard-matching function.

**Why it matters**: Capabilities use a simple grammar: `action:resource:scope`, where a trailing `*` is a prefix wildcard. Test your understanding against these examples *before* running anything (write predictions in your notes):

| Pattern | `read:files:/workspace/a.txt` | `read:files:/etc/passwd` |
|---------|-------------------------------|--------------------------|
| `read:files:/workspace/*` | ✅ matches | ❌ no |

| Pattern | `exec:tools:scanner` |
|---------|----------------------|
| `exec:tools:scanner` | ✅ exact match |
| `exec:tools:*` | ✅ prefix match |

Now the subtle one — in `drifted-002` the runtime capability is `exec:tools:parser,validator,scanner` while the allow list has `exec:tools:parser,validator`. Since the runtime string is not a *prefix* of the allowed pattern (it's longer), it does **not** match, and falls through toward deny/default-deny. Composite tool lists make wildcard matching brittle — Exercise 3 (standard) has you fix this by splitting on commas and matching per-tool.

---

## ⚙️ Part 2: Run the Policy Gate on All Scenarios

### Step 3: Execute the gate

```bash
cd demo-02-supply-chain-aibom && python3 student/policy_gate.py && cd ../..
```

**What this does**: Instantiates `PolicyGate` from the fixture, then evaluates each of the four drift scenarios, printing per-capability ALLOW/DENY verdicts with reasons, plus a ✓/✗ against the scenario's expectation.

**Why it matters**: This is your first live view of the precedence ladder from the background section. Read each scenario's output against the flowchart.

**Expected output** (annotated):

```
=== compliant-001: System matches declared AIBOM ===
Compliant: True
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: write:files:/workspace/output/* (explicitly_allowed)
  ALLOW: exec:tools:parser,validator (explicitly_allowed)
  ALLOW: net:http:api.internal/* (explicitly_allowed)
✓ Matches expected: PASS
```
All four capabilities sit on the allow list. No waiver needed. Trivial case — but it proves the gate doesn't over-block.

```
=== drifted-002: Agent gained scanner execution capability ===
Compliant: False
  DENY: exec:tools:parser,validator,scanner (not_allowed_default_deny)
✓ Matches expected: BLOCKED
```
The drifted capability misses allow (not a prefix match), misses waiver (none supplied), misses deny (no pattern covers it), and lands on **default deny**. Note the reason string: `not_allowed_default_deny` — the gate *tells you* it failed closed, which is exactly what you want in an audit log.

```
=== invalid-waiver-003: Waiver for shell access without approval ===
  DENY: exec:shell:* (explicitly_denied)
✓ Matches expected: WAIVER REJECTED
```
Two independent reasons this fails: the waiver has `approved: false`, **and** `exec:shell:*` isn't in `waiver_rules.allowed_scopes`. Even a signed, unexpired waiver couldn't authorize this scope. Defense in depth.

```
=== valid-waiver-004: Properly scoped, approved, time-limited waiver ===
  ALLOW: exec:tools:scanner (waiver_granted)
✓ Matches expected: WAIVER ACCEPTED
```
The waiver is approved, unexpired (expires `2099-12-31` in fixture — far future), and its scope `exec:tools:scanner` is in the waivable list. All three waiver conditions satisfied → grant with reason `waiver_granted`.

---

### Step 4: Trace one decision by hand

Open `demo-02-supply-chain-aibom/student/policy_gate.py` and find `check_capability`. 

**What to do**: With `drifted-002`'s capability `exec:tools:parser,validator,scanner` in mind, walk the method line by line and write in your notes which branch fires and why. Confirm your trace matches the `not_allowed_default_deny` output from Step 3.

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

gate = PolicyGate(Path("fixtures/aibom.json"))
caps = ["exec:tools:scanner"]

for label, exp in [("expired (2020)", "2020-01-01T00:00:00Z"),
                   ("valid (2099)",   "2099-12-31T23:59:59Z")]:
    w = Waiver("exec:tools:scanner", "test", True, exp)
    r = gate.evaluate_system(caps, w)
    print(f"{label:15} -> compliant={r['compliant']}")
EOF
cd ../..
```

**What this does**: Evaluates the *same* capability and *same* approved scope twice, differing only in expiry.

**Why it matters**: Output should be:
```
expired (2020)  -> compliant=False
valid (2099)    -> compliant=True
```
A waiver is a *lease*, not a grant. The `is_valid()` check compares the expiry against current time (timezone-aware). This is why the fixture's original `2025-01-15` date had to be bumped — real time moved past it. **Time is an attack surface**: an unmonitored waiver quietly becomes a permanent hole the day it expires, unless something re-checks. Exercise 2 has you build that monitor.

---

## 🧵 Part 4: Run the Tests

### Step 6: Run Demo 02's test suite

```bash
cd demo-02-supply-chain-aibom && python3 -m pytest tests/ -v && cd ../..
```

**What this does**: Runs all 12 tests. The key ones:

| Test | Proves |
|------|--------|
| `test_compliant_system_passes` | Gate doesn't over-block legitimate capability sets |
| `test_drifted_system_blocked` | Extra capability → non-compliant, with scanner specifically denied |
| `test_invalid_waiver_rejected` | Unapproved waiver grants nothing |
| `test_valid_waiver_accepted` | Fully-valid waiver grants, with reason `waiver_granted` |
| `test_expired_waiver_rejected` | Time boundary enforced |
| `test_explicit_deny_overrides_waiver` | **Critical**: `write:files:/etc/passwd` denied even with a waiver for `write:files:/etc/*` — because `/etc/*` is not in the waivable scopes |
| `test_least_privilege_analysis` | The deny list actually contains the broad dangerous patterns |
| `test_github_actions_validation_script` | `validate_aibom.py` exits 0 when all scenarios behave as expected |

**Why it matters**: `test_explicit_deny_overrides_waiver` is the precedence ladder's most important rung. Waivers are powerful, so the *power to waive* is itself restricted. If your Step 4 trace didn't cover this path, trace it now.

---

## 🔄 Part 5: CI Integration

### Step 7: Run the CI validator directly

```bash
cd demo-02-supply-chain-aibom && python3 student/validate_aibom.py; echo "exit code: $?" && cd ../..
```

**What this does**: Runs the standalone validator that a GitHub Actions workflow would invoke. It re-evaluates all scenarios and asserts each behaves as its `expected` field says. Exit codes: `0` = all as expected, `1` = unexpected drift behavior, `2` = error.

**Why it matters**: This is the bridge from teaching demo to practice. In a real pipeline, the "runtime capabilities" input would come from observing the live agent (instrumented tool calls), and a non-zero exit blocks the deploy. You now know both ends: the gate (Step 3) and the gate's CI harness (this step).

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 2.1 — Add a network-drift scenario.**
Add `drifted-005` to the fixture: runtime gains `net:http:evil.example/*` on top of the compliant set. Set `expected: "block"`. Re-run Step 3. Which reason string fires? (Prediction: `not_allowed_default_deny` — `net:http:evil.example/*` matches no allow, and `net:http:*` in the deny list *does* match... verify which one actually fires and explain the precedence.)

**What this teaches**: Reason strings are audit evidence. Learning to *predict* them means you've internalized the ladder.

### Standard

**Exercise 2.2 — Waiver expiry monitor.**
Write `student/waiver_monitor.py`: given a list of waivers, print each as `EXPIRED`, `EXPIRES_IN_<24H` (action needed), or `VALID`, and exit non-zero if any waiver is expired *but its capability still appears in a runtime set you pass in*. This models the "silent permanent hole" failure.

**What this teaches**: Policies decay. Monitoring the *policy objects themselves* is as important as enforcing them at gate time.

**Exercise 2.3 — Fix composite-tool matching.**
Modify `_match_pattern` usage so `exec:tools:parser,validator,scanner` is split on commas and each tool checked individually against patterns. Then `exec:tools:parser,validator` remains allowed while adding `scanner` correctly triggers drift. Add a test for the mixed case `exec:tools:validator,scanner`.

**What this teaches**: Grammar design flaws become policy bypasses. Composite fields need composite handling.

### Extension

**Exercise 2.4 — Waiver justification quality gate.**
Extend `Waiver` validation: reject waivers whose `justification` is under 20 characters or matches a placeholder pattern (`TODO`, `test`, `N/A`). Add fixtures: one rejected for weak justification, one accepted. Defend your minimum length in lab notes — what attack does this actually slow down?

**What this teaches**: Governance controls (approval, justification) are only as strong as their weakest verification. Think about who reviews and what "review" means under deadline pressure.

---

## 📝 Lab Notes Questions

1. Explain the four-rung precedence ladder (allow → waiver → deny → default-deny) and give one concrete attack each rung prevents.
2. Why must `waiver_rules.allowed_scopes` exist at all? What would go wrong if any scope could be waived?
3. Your Step 5 experiment showed time silently flips a waiver from valid to expired. Describe where this check should live in a production system (gate-time? cron? both?) and why.

---

## ✅ Completion Checklist

- [ ] AIBOM structure mapped in lab notes
- [ ] Capability grammar understood; prefix-match predictions written *before* running
- [ ] All four scenarios run; each ✓ Matches expected
- [ ] Hand-trace of `drifted-002` recorded
- [ ] Expiry boundary experiment run (expired vs valid)
- [ ] All 12 tests pass
- [ ] CI validator exits 0
- [ ] At least Beginner exercise; Standard 2.3 strongly recommended
- [ ] `LAB_NOTES.md` Module 2 block filled with reproducibility fields (seed 42, commit, `make demo DEMO=02`)

---

**⬅️ Prev: [Module 1](lab-01-blind-verification.md) | ➡️ Next: [Module 3: Evaluation Invariants](lab-03-eval-invariants.md)**
