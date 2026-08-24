# Demo 02: Supply Chain & AIBOM Drift — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md). Full course lab: [../docs/course/lab-02-supply-chain-aibom.md](../../docs/course/lab-02-supply-chain-aibom.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the policy gate | 2 min | `python3 student/policy_gate.py` |
| Run the CI validator | 1 min | `python3 student/validate_aibom.py` |
| Generate results | 1 min | `python3 student/generate_results.py` |
| **Total** | **~10 min** | |

**Safety**: 100% offline. Synthetic package names only (`secure-parser-123`, etc.). No registries, no network.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-02-supply-chain-aibom
ls
# Expected: Makefile  README.md  INSTRUCTIONS.md  fixtures  results  student  tests
```

**What this does**: All commands below use relative paths (`fixtures/aibom.json`), so you must be inside this directory.

---

## Step 1 — Read the Fixture Before Running (Predict First)

```bash
cat fixtures/aibom.json
```

**What this does**: Shows the AIBOM (declared components + capabilities), the policy (allowed / denied / waiver rules), and the four drift scenarios.

**Before running anything, write down your predictions**:

| Scenario | Expected result | Why |
|----------|-----------------|-----|
| `compliant-001` | ? | |
| `drifted-002` | ? | |
| `invalid-waiver-003` | ? | |
| `valid-waiver-004` | ? | |

**Key things to notice while reading**:
- The deny list contains `net:http:*` (very broad) while the allow list contains `net:http:api.internal/*` (specific) — which wins?
- `waiver_rules.allowed_scopes` lists only `exec:tools:scanner` and `net:http:specific.host` — what does that mean for a waiver requesting `exec:shell:*`?

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **12 tests**: compliant-passes, drifted-blocked, invalid-waiver-rejected, valid-waiver-accepted, expired-waiver-rejected, explicit-deny-overrides-waiver, least-privilege, CI script, plus exercises.

**Expected output (end of run)**:

```
tests/test_aibom_drift.py::TestExercises::test_exercise_json_results PASSED
============================== 12 passed in 0.XXs ==============================
```

✅ **Checkpoint**: `12 passed`. Fix environment before continuing if not.

---

## Step 3 — Run the Policy Gate on All Scenarios

```bash
python3 student/policy_gate.py
```

**What this does**: Loads the AIBOM and policy, then evaluates each scenario's runtime capabilities against the gate. The gate's decision order is: **explicit allow → valid waiver → explicit deny → default deny (fail-closed)**.

**Expected output** (annotated — match each ✓ against your Step 1 predictions):

```
=== compliant-001: System matches declared AIBOM ===
Compliant: True
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: write:files:/workspace/output/* (explicitly_allowed)
  ALLOW: exec:tools:parser,validator (explicitly_allowed)
  ALLOW: net:http:api.internal/* (explicitly_allowed)
✓ Matches expected: PASS

=== drifted-002: Agent gained scanner execution capability ===
Compliant: False
  DENY: exec:tools:parser,validator,scanner (not_allowed_default_deny)
✓ Matches expected: BLOCKED

=== invalid-waiver-003: Waiver for shell access without approval ===
Compliant: False
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  DENY: exec:shell:* (explicitly_denied)
✓ Matches expected: WAIVER REJECTED

=== valid-waiver-004: Properly scoped, approved, time-limited waiver ===
Compliant: True
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: exec:tools:scanner (waiver_granted)
✓ Matches expected: WAIVER ACCEPTED
```

**What to record in your notes**: the **reason string** for each decision (`explicitly_allowed`, `not_allowed_default_deny`, `explicitly_denied`, `waiver_granted`). These strings are audit evidence — being able to predict them means you understand the gate.

---

## Step 4 — Run the GitHub Actions Validator (CI Simulation)

```bash
python3 student/validate_aibom.py; echo "exit code: $?"
```

**What this does**: Runs the standalone validator that CI would invoke. It re-evaluates all scenarios and asserts each behaves as its `expected` field declares.

**Expected output**:

```
(no output — silent success)
exit code: 0
```

**Exit code meaning**: `0` = all scenarios behave as declared · `1` = unexpected drift behavior · `2` = error.

**Why this step exists**: This is the bridge from teaching demo to practice — in a real pipeline, a non-zero exit blocks the deployment.

---

## Step 5 — Generate the Results File

```bash
python3 student/generate_results.py
```

**What this does**: Re-runs all scenarios through the gate and writes `results/drift_results.json` in the standardized result schema.

**Expected output** (printed and saved):

```json
{
  "demo": "demo-02-supply-chain-aibom",
  "experiment": "drift_detection",
  "seed": 42,
  "commit": "local",
  "environment": "test",
  "command": "make demo DEMO=02",
  "result": "pass",
  "notes": "Synthetic teaching fixture",
  "scenarios": [
    {"scenario": "compliant-001", "expected": "pass", "compliant": true},
    {"scenario": "drifted-002", "expected": "block", "compliant": false},
    {"scenario": "invalid-waiver-003", "expected": "reject_waiver", "compliant": false},
    {"scenario": "valid-waiver-004", "expected": "accept_waiver", "compliant": true}
  ]
}
```

✅ **Checkpoint**: every scenario's `compliant` value matches its `expected` semantics.

---

## Step 6 — Waiver Expiry Experiment (Recommended)

```bash
python3 - << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, "student")
from policy_gate import PolicyGate, Waiver

gate = PolicyGate(Path("fixtures/aibom.json"))
for label, exp in [("expired (2020)", "2020-01-01T00:00:00Z"),
                   ("valid (2099)",   "2099-12-31T23:59:59Z")]:
    w = Waiver("exec:tools:scanner", "test", True, exp)
    r = gate.evaluate_system(["exec:tools:scanner"], w)
    print(f"{label:15} -> compliant={r['compliant']}")
EOF
```

**What this does**: Evaluates the same capability twice with waivers differing *only* in expiry date.

**Expected output**:

```
expired (2020)  -> compliant=False
valid (2099)    -> compliant=True
```

**Lesson**: a waiver is a *lease*. Record in your notes what happens silently the day an unmonitored waiver expires.

---

## Step 7 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy exactly from Steps 2–5 |
| Tests passed | | `12 passed` |
| Gate verdicts | | 4 × ✓ "Matches expected" (Step 3) |
| CI exit code | | `0` (Step 4) |
| Result file | | `results/drift_results.json` |

**Reproducibility check**: `rm -rf results/` and re-run Steps 3–5. The JSON must be byte-identical (except nothing time-dependent exists in this demo — output should match exactly).

---

## Alternative: One-Command Run

From the **repository root**:

```bash
make demo DEMO=02
```

This chains Steps 3–5 automatically and prints the results JSON.

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Add `drifted-005`: runtime gains `net:http:evil.example/*` | Add to `drift_scenarios`, `expected: "block"`; predict the reason string first |
| Standard | Waiver expiry monitor script | Classify waivers as EXPIRED / EXPIRES_SOON / VALID |
| Standard | Fix composite-tool matching so `exec:tools:parser,validator,scanner` matches per-tool | Split on commas before pattern matching |
| Extension | Reject waivers with weak justifications (< 20 chars or "TODO"/"test") | Extend `Waiver` validation; add fixtures |

After any exercise: re-run Step 2 (tests) and Step 3 (gate) and record what changed.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: cryptography` etc. | Deps not installed | Repo root: `make setup` |
| `FileNotFoundError: fixtures/aibom.json` | Wrong directory | `cd demo-02-supply-chain-aibom` |
| `valid-waiver-004` shows `compliant=False` | System clock past waiver expiry, or fixture edited | Fixture uses `2099` expiry; restore with `git checkout -- fixtures/` |
| Tests fail after your edits | Exercise changes broke invariants | `git checkout -- student/ tests/ fixtures/` to reset |
| Exit code 2 from validator | Exception in validator | Read the traceback; usually a fixture JSON typo |

---

## Safety Reminder

⚠️ **Teaching demonstration only.** Synthetic package names; no real dependencies, registries, or credentials; local validation only. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
