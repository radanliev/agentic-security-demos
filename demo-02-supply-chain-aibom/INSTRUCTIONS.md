# Demo 02: Supply Chain & AIBOM Drift — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md). Full course lab: [../docs/course/lab-02-supply-chain-aibom.md](../docs/course/lab-02-supply-chain-aibom.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the policy gate | 2 min | `python3 student/policy_gate.py` |
| Run the CI validator | 1 min | `python3 student/validate_aibom.py --scenario drifted-002` |
| Generate results | 1 min | `python3 student/generate_results.py` |
| **Total** | **~10 min** | |

**Safety**: 100% offline. Synthetic package names only (`secure-parser-123`, etc.). No registries, no network.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-02-supply-chain-aibom
ls
# Expected: INSTRUCTIONS.md  Makefile  README.md  fixtures  student  tests
# (results/ is git-ignored; it is created by `make setup` or by generate_results.py)
```

**What this does**: All commands below use relative paths (`fixtures/aibom.json`), so you must be inside this directory.

---

## Step 1 — Read the Fixture Before Running (Predict First)

```bash
cat fixtures/aibom.json
```

**What this does**: Shows the AIBOM (declared components + capabilities), the policy (allowed / denied / waiver rules), the pinned `evaluation_time` (the clock every scenario is judged against, so the demo gives the same answer every day), and the four drift scenarios.

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
- `waiver_rules.max_duration_hours` is 24 and `valid-waiver-004` runs from `issued` 09:00 to `expires` 09:00 the next day — what happens if you push `expires` out by a week?
- `exec:tools:scanner` is on the deny list *and* on the waivable list — which wins, and in which order are the checks made?

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **17 tests**: compliant-passes, drifted-blocked (scanner explicitly denied, the rest still allowed), subset-of-declared-tools-allowed, invalid-waiver-rejected, unapproved-waiver-rejected (approval checked on its own), valid-waiver-accepted (still reported as drift), expired-waiver-rejected, duration-limit-enforced, waiver-without-issue-time-rejected, unwaivable-scope-stays-denied, least-privilege, scenarios-behave-as-labelled, CI script exit codes, plus exercises.

**Expected output (end of run)**:

```
tests/test_aibom_drift.py::TestExercises::test_exercise_json_results PASSED
============================== 17 passed in 0.XXs ==============================
```

✅ **Checkpoint**: `17 passed`. Fix environment before continuing if not.

---

## Step 3 — Run the Policy Gate on All Scenarios

```bash
python3 student/policy_gate.py
```

**What this does**: Loads the AIBOM and policy, expands composite tool lists into one capability per tool, then answers two separate questions for each scenario: **drift** (is anything used that the AIBOM does not declare?) and **compliance** (is every capability permitted?). The gate's decision order per capability is: **explicit allow → valid waiver → explicit deny → default deny (fail-closed)**. A waiver is valid only if it is approved by a named approver, in force at the evaluation time, no longer than `max_duration_hours`, and for a scope in `allowed_scopes`.

**Expected output** (verbatim — match each ✓ against your Step 1 predictions):

```
Declared capabilities (AIBOM): ['exec:tools:parser', 'exec:tools:validator', 'net:http:api.internal/*', 'read:files:/workspace/*', 'write:files:/workspace/output/*']
Evaluation time: 2025-01-14T12:00:00Z (fixed by the fixture for reproducibility)

=== compliant-001: System matches declared AIBOM ===
Drift detected: False
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: write:files:/workspace/output/* (explicitly_allowed)
  ALLOW: exec:tools:parser (explicitly_allowed)
  ALLOW: exec:tools:validator (explicitly_allowed)
  ALLOW: net:http:api.internal/* (explicitly_allowed)
Compliant: True
✓ Matches expected: PASS

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

=== invalid-waiver-003: Waiver for shell access without approval ===
Drift detected: True (undeclared: exec:shell:*)
Waiver exec:shell:*: REJECTED: not approved; scope exec:shell:* is not waivable
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  DENY: exec:shell:* (explicitly_denied)
Compliant: False
✓ Matches expected: WAIVER REJECTED

=== valid-waiver-004: Properly scoped, approved, time-limited waiver ===
Drift detected: True (undeclared: exec:tools:scanner)
Waiver exec:tools:scanner: ACCEPTED
  ALLOW: read:files:/workspace/* (explicitly_allowed)
  ALLOW: exec:tools:scanner (waiver_granted)
Compliant: True
✓ Matches expected: WAIVER ACCEPTED
```

**What to record in your notes**: the **reason string** for each decision (`explicitly_allowed`, `explicitly_denied`, `waiver_granted`; `not_allowed_default_deny` fires for anything on neither list — try `exec:tools:formatter`), and the waiver rejection reasons. These strings are audit evidence — being able to predict them means you understand the gate. Note that `valid-waiver-004` is *compliant* and *still drift*: the waiver is a sanctioned exception, not a change to the declaration.

---

## Step 4 — Run the GitHub Actions Validator (CI Simulation)

```bash
python3 student/validate_aibom.py --scenario compliant-001; echo "exit code: $?"
python3 student/validate_aibom.py --scenario drifted-002; echo "exit code: $?"
python3 student/validate_aibom.py --self-test; echo "exit code: $?"
```

**What this does**: Runs the standalone validator that CI would invoke. Given one observed runtime capability set (here taken from a fixture scenario; in a pipeline you would pass `--runtime observed.json`), it exits **0 if compliant, 1 if not, 2 on error**. `--self-test` (also the default with no arguments) instead checks that every fixture scenario behaves as its `expected` label says.

**Expected output**:

```
compliant-001: COMPLIANT (evaluated at 2025-01-14T12:00:00+00:00)
exit code: 0
DENY: exec:tools:scanner (explicitly_denied)
drift: undeclared capabilities ['exec:tools:scanner']
drifted-002: NON-COMPLIANT (evaluated at 2025-01-14T12:00:00+00:00)
exit code: 1
self-test: 4/4 scenarios behave as their expected label
exit code: 0
```

**Why this step exists**: This is the bridge from teaching demo to practice — in a real pipeline, the non-zero exit on `drifted-002` is what blocks the deployment. Try `--scenario valid-waiver-004 --now now`: judged against today's clock the 2025 waiver has lapsed, and the same runtime is now non-compliant (exit 1).

---

## Step 5 — Generate the Results File

```bash
python3 student/generate_results.py
```

**What this does**: Re-runs all scenarios through the gate and writes `results/drift_results.json` in the standardized result schema.

**Expected output** (printed and saved; `commit` is your git short SHA or `local`, `environment` is your Python/OS; `result` is computed from the scenarios, not hard-coded):

```json
{
  "demo": "demo-02-supply-chain-aibom",
  "experiment": "drift_detection",
  "seed": 42,
  "commit": "local",
  "environment": "Python 3.11.15, Linux",
  "command": "make demo DEMO=02",
  "result": "pass",
  "notes": "Synthetic teaching fixture; evaluated at fixture evaluation_time 2025-01-14T12:00:00Z",
  "scenarios": [
    {"scenario": "compliant-001", "expected": "pass", "compliant": true, "drift_detected": false, "waiver_accepted": null, "matches_expected": true},
    {"scenario": "drifted-002", "expected": "block", "compliant": false, "drift_detected": true, "waiver_accepted": null, "matches_expected": true},
    {"scenario": "invalid-waiver-003", "expected": "reject_waiver", "compliant": false, "drift_detected": true, "waiver_accepted": false, "matches_expected": true},
    {"scenario": "valid-waiver-004", "expected": "accept_waiver", "compliant": true, "drift_detected": true, "waiver_accepted": true, "matches_expected": true}
  ]
}
```

✅ **Checkpoint**: every scenario has `"matches_expected": true` and `"result": "pass"`.

---

## Step 6 — Waiver Expiry Experiment (Recommended)

```bash
python3 - << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, "student")
from policy_gate import PolicyGate, Waiver

gate = PolicyGate(Path("fixtures/aibom.json"))   # evaluation_time pinned at 2025-01-14T12:00Z
for label, issued, expires in [("expired",  "2025-01-13T09:00:00Z", "2025-01-14T09:00:00Z"),
                               ("in force", "2025-01-14T09:00:00Z", "2025-01-15T09:00:00Z"),
                               ("too long", "2025-01-14T09:00:00Z", "2025-01-21T09:00:00Z")]:
    w = Waiver("exec:tools:scanner", "audit scan", True, expires, issued, "security-lead@example.com")
    r = gate.evaluate_system(["exec:tools:scanner"], w)
    print(f"{label:9} -> compliant={r['compliant']}  {r['waiver']['reasons']}")
EOF
```

**What this does**: Evaluates the same capability three times with waivers differing *only* in their timestamps.

**Expected output**:

```
expired   -> compliant=False  ['expired at 2025-01-14T09:00:00Z']
in force  -> compliant=True  []
too long  -> compliant=False  ['duration exceeds max_duration_hours=24']
```

**Lesson**: a waiver is a *lease*, and the lease length is policy (`max_duration_hours`), not the requester's choice. Record in your notes what happens silently the day an unmonitored waiver expires — then run `python3 student/validate_aibom.py --scenario valid-waiver-004 --now now` to watch it happen.

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
| Tests passed | | `17 passed` |
| Gate verdicts | | 4 × ✓ "Matches expected" (Step 3) |
| CI exit codes | | `0`, `1`, `0` (Step 4) |
| Result file | | `results/drift_results.json` |

**Reproducibility check**: `rm -rf results/` and re-run Steps 3–5. The JSON must be byte-identical: the fixture pins `evaluation_time`, so the clock does not leak into the result (only `commit` and `environment` differ between machines).

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
| Standard | Extend per-tool matching to host lists (`net:http:a.internal,b.internal`) | Generalise `expand_capability`; add a mixed-case test |
| Extension | Reject waivers with weak justifications (< 20 chars or "TODO"/"test") | Extend `Waiver.validate`; add fixtures |
| Extension | Normalise resource paths so `read:files:/workspace/../etc/passwd` no longer matches `read:files:/workspace/*` | `posixpath.normpath` on the scope part before matching; add a traversal test |

After any exercise: re-run Step 2 (tests) and Step 3 (gate) and record what changed.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: pytest` | Deps not installed | Repo root: `make setup` |
| `FileNotFoundError: fixtures/aibom.json` | Wrong directory | `cd demo-02-supply-chain-aibom` |
| `valid-waiver-004` shows `compliant=False` | `evaluation_time` removed from the fixture (real clock is past the 2025 waiver), or fixture edited | Restore with `git checkout -- fixtures/` |
| Tests fail after your edits | Exercise changes broke invariants | `git checkout -- student/ tests/ fixtures/` to reset |
| Exit code 2 from validator | Exception in validator | Read the traceback; usually a fixture JSON typo |

---

## Safety Reminder

⚠️ **Teaching demonstration only.** Synthetic package names; no real dependencies, registries, or credentials; local validation only. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
