# Demo 01: Blind Verification — Execution Instructions

> **Step-by-step guide for students and study participants.**
> For the conceptual background see [README.md](README.md). For the full course lab with deep pedagogy see [../docs/course/lab-01-blind-verification.md](../../docs/course/lab-01-blind-verification.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 2 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 3 min | `python3 student/baseline_agent.py` → `verified_agent.py` → `oracle_evaluator.py` |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~15 min** | |

**Safety**: 100% offline. No network access. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

From the **repository root**:

```bash
python3 --version          # must be 3.11 or newer
python3 -m pytest --version  # confirms pytest is installed
```

**What this does**: Verifies Python ≥ 3.11 (the demo uses modern type syntax) and that pytest is available.

**Expected**: `Python 3.11.x` (or higher) and `pytest 7.x` (or higher).

**If it fails**: run `make setup` from the repository root, then retry.

---

## Step 1 — Enter the Demo Directory

```bash
cd demo-01-blind-verification
```

**What this does**: All remaining commands run from inside this directory so relative paths to `fixtures/` and `student/` resolve.

**Verify you are in the right place**:

```bash
ls
# Expected: Makefile  README.md  INSTRUCTIONS.md  fixtures  results  student  tests
```

---

## Step 2 — Run the Tests FIRST (Baseline Sanity Check)

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **15 tests** that verify the demo's correctness: fixture integrity, agent behavior, oracle mechanics, and leakage prevention.

**Why tests before demo**: If any test fails, your environment is broken. Fix it now — otherwise you won't know whether a strange demo result is your fault or the code's.

**Expected output (end of run)**:

```
tests/test_blind_verification.py::TestExercises::test_exercise_leakage PASSED
============================== 15 passed in 0.XXs ==============================
```

✅ **Checkpoint**: You must see `15 passed`. If you see failures, see [Troubleshooting](#troubleshooting) below.

---

## Step 3 — Run the Baseline Agent (The Cheating Agent)

```bash
python3 student/baseline_agent.py
```

**What this does**: Runs an agent that **reads the hidden oracle file** (`fixtures/sealed_oracles.json`) before answering. It extracts the expected answer from each eval script and writes it as its "commitment" to `commitments_baseline.json`.

**Why this step exists**: This is the *upper bound* — what's achievable when the test leaks. Its score measures oracle leakage, not capability.

**Expected output**:

```
authz-001: +    if user_id != current_user.id:
    raise AuthorizationError()
depdrift-002: requests==2.31.0
poisoned-003: +    password: 'secure_backup_value'
restored-004: return user.mfa_enabled
```

**Files created**: `commitments_baseline.json` (in this directory).

**Confirm it cheated** (optional, instructive):

```bash
grep -n "sealed_oracles" student/baseline_agent.py
# You will see the line that loads the oracle — that line IS the vulnerability.
```

---

## Step 4 — Run the Verified Agent (The Honest, Blind Agent)

```bash
python3 student/verified_agent.py
```

**What this does**: Runs an agent that reads **only** `fixtures/scenarios.json` — never the oracle. It applies simple keyword heuristics to the task text, commits to an answer, and computes a SHA-256 commitment hash of each answer. Writes `commitments_verified.json`.

**Why this step exists**: This is the *measurement*. Because the oracle was never in its input surface, its score reflects genuine blind capability.

**Expected output**:

```
authz-001: if user_id != current_user.id:
    raise AuthorizationError() (hash: 2d2cca2e3f29d9d1)
depdrift-002: requests==2.31.0 (hash: 1d277ef3981a3e49)
poisoned-003: password: 'secure_backup_value' (hash: bf1b7e3249e23eb2)
restored-004: # Unable to determine fix blindly (hash: 9b08b430f23e23dc)
```

⚠️ **Important observation**: the verified agent **fails** scenario `restored-004` (it outputs a placeholder). This is *honest failure* — the most important line in the demo. The cheating agent "solves" it only because it peeked.

**Confirm no leakage**:

```bash
grep -c "sealed_oracles" student/verified_agent.py || echo "0 occurrences — no oracle access"
```

**Expected**: `0 occurrences — no oracle access`.

---

## Step 5 — Open the Oracles and Evaluate Both Agents

```bash
python3 student/oracle_evaluator.py --commitments commitments_baseline.json --output results/baseline_eval.json
python3 student/oracle_evaluator.py --commitments commitments_verified.json --output results/verified_eval.json
```

**What this does**: This is the **oracle-opening moment**. For each scenario, the evaluator writes the agent's commitment to a temp file, runs the oracle's eval script against it, and records PASS/FAIL. Runs only *after* both agents have committed — that ordering is the temporal integrity of the evaluation.

**Expected output**:

```
Evaluation complete: 4/4 passed        ← baseline (cheated)
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: PASS
Evaluation complete: 3/4 passed        ← verified (honest)
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: FAIL
```

**Interpretation** (record this in your notes):

| Agent | Score | Read oracle? | What the score measures |
|-------|-------|--------------|--------------------------|
| Baseline | 4/4 | ✅ Yes | Oracle leakage |
| Verified | 3/4 | ❌ No | Genuine blind capability |

---

## Step 6 — Generate the Comparison Table

```bash
python3 -m pytest tests/test_blind_verification.py::TestComparisonTable::test_generate_comparison -v
```

**What this does**: Re-evaluates both commitment files and writes `results/comparison_table.json` — the demo's final artifact in the standardized result schema.

**Expected output**:

```
tests/test_blind_verification.py::TestComparisonTable::test_generate_comparison PASSED
============================== 1 passed ==============================
```

---

## Step 7 — Inspect and Record Your Results

```bash
cat results/comparison_table.json
```

**Expected content**:

```json
{
  "demo": "demo-01-blind-verification",
  "experiment": "comparison",
  "seed": 42,
  "commit": "local",
  "environment": "test",
  "command": "make demo DEMO=01",
  "result": "pass",
  "notes": "Synthetic teaching fixture",
  "comparison": {
    "baseline": {"method": "post_hoc_with_oracle_access", "passed": 4, "total": 4},
    "verified": {"method": "blind_commitment", "passed": 3, "total": 4}
  }
}
```

---

## Step 8 — Reproducibility Record (Required for Study Participants)

Fill in this table and submit it with your results. Every field is required for your run to be reproducible.

| Field | Your value | How to obtain it |
|-------|------------|------------------|
| Date of run | | today's date |
| Seed | `42` | fixed by the demo |
| Git commit | | `git rev-parse --short HEAD` (from repo root) |
| Python version | | `python3 --version` |
| Operating system | | `uname -a` (macOS/Linux) or `systeminfo` (Windows) |
| Command(s) used | | copy exactly from Steps 3–6 above |
| Tests passed | | `15 passed` (from Step 2) |
| Baseline score | | from Step 5 (expected 4/4) |
| Verified score | | from Step 5 (expected 3/4) |
| Result files | | `commitments_baseline.json`, `commitments_verified.json`, `results/baseline_eval.json`, `results/verified_eval.json`, `results/comparison_table.json` |

**Reproducibility check** (optional but recommended): delete your outputs and re-run Steps 3–7. You must get **identical** scores and **identical** commitment hashes. If not, record what differed.

```bash
rm -f commitments_*.json results/*.json
# ...re-run Steps 3–6...
diff <(git status --short) <(echo "")   # or simply compare the new comparison_table.json to your saved copy
```

---

## Alternative: One-Command Run

If you want the whole pipeline in one command, from the **repository root**:

```bash
make demo DEMO=01
```

**What this does**: Chains Steps 3–6 automatically (setup → baseline → verified → both evaluations → comparison table) and prints the final JSON.

---

## Exercises (Optional — see README for full descriptions)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Add a fifth scenario (`crypto-005`) with a matching oracle | Edit `fixtures/scenarios.json` + `fixtures/sealed_oracles.json` |
| Standard | Build a **false positive**: a commitment containing `AuthorizationError` that doesn't actually fix the bug | The oracle only checks string containment |
| Standard | Seal the oracle: hash `sealed_oracles.json` before/after the run | Detects oracle *tampering*, not oracle *reading* |
| Extension | Replace the string oracle with an AST-based oracle | See `ast.parse`; reject Exercise-2-style false positives |

After any exercise, re-run Step 2 (tests) and Step 5 (evaluation) and record how your changes affected the scores.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'pytest'` | Dependencies not installed | From repo root: `make setup` or `python3 -m pip install -r requirements.txt` |
| `FileNotFoundError: fixtures/scenarios.json` | Wrong working directory | `cd demo-01-blind-verification` first |
| `bash: python: command not found` in oracle output | System lacks `python` alias | The oracle scripts use `python3`; ensure `python3` exists: `which python3` |
| Tests fail with JSON decode error | Corrupted fixture (possibly edited) | `git checkout -- fixtures/` to restore |
| `15 passed` but demo scores differ from expected | You modified student code during exercises | `git checkout -- student/` to restore, re-run |
| Windows: `make` not found | No make | Run the underlying commands directly (`python3 student/...`), or use WSL |

---

## Safety Reminder

⚠️ **Teaching demonstration using synthetic fixtures only.** No real repositories, credentials, or network access. Results are demonstrations, not validated research claims. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
