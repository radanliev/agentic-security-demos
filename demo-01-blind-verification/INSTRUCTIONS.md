# Demo 01: Blind Verification — Execution Instructions

> **Step-by-step guide for students and study participants.**
> For the conceptual background see [README.md](README.md). For the full course lab with deep pedagogy see [../docs/course/lab-01-blind-verification.md](../docs/course/lab-01-blind-verification.md).

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
# Expected: INSTRUCTIONS.md  Makefile  README.md  commitments_baseline.json  commitments_verified.json  fixtures  student  tests
# (results/ is git-ignored; it is created by `make setup` or by the first evaluation run)
```

---

## Step 2 — Run the Tests FIRST (Baseline Sanity Check)

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **18 tests** that verify the demo's correctness: fixture integrity, agent behavior (baseline 4/4, verified 3/4 with `restored-004` failing honestly), oracle mechanics (false positives, false negatives, oracle errors reported), commitment binding (a post-hoc edit is rejected), and leakage prevention (the blind agent's only input file contains no answer key).

**Why tests before demo**: If any test fails, your environment is broken. Fix it now — otherwise you won't know whether a strange demo result is your fault or the code's.

**Expected output (end of run)**:

```
tests/test_blind_verification.py::TestExercises::test_exercise_leakage PASSED
============================== 18 passed in 0.XXs ==============================
```

✅ **Checkpoint**: You must see `18 passed`. If you see failures, see [Troubleshooting](#troubleshooting) below.

---

## Step 3 — Run the Baseline Agent (The Cheating Agent)

```bash
python3 student/baseline_agent.py
```

**What this does**: Runs an agent that **reads the hidden oracle file** (`fixtures/sealed_oracles.json`) before answering. It copies each oracle's `expected_commitment` and writes it as its "commitment" to `commitments_baseline.json`. It publishes no hash, so nothing binds it to what it wrote.

**Why this step exists**: This is the *upper bound* — what's achievable when the test leaks. Its score measures oracle leakage, not capability.

**Expected output**:

```
authz-001: if user_id != current_user.id:
    raise AuthorizationError()
depdrift-002: requests==2.31.0
poisoned-003: password: 'secure_backup_value'
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

**What this does**: Runs an agent that reads **only** `fixtures/scenarios.json` (task, ticket context, code snippet — no answer key) — never the oracle. It applies simple keyword heuristics to the ticket text, commits to an answer, computes the SHA-256 of each commitment and **publishes the hashes** to `commitment_hashes_verified.json` before any oracle is opened. Writes `commitments_verified.json`.

**Why this step exists**: This is the *measurement*. Because the oracle was never in its input surface, its score reflects genuine blind capability; because the hashes are published first, the commitments cannot be revised after the reveal.

**Expected output**:

```
authz-001: if user_id != current_user.id:
    raise AuthorizationError() (sha256: 2d2cca2e3f29d9d15c789539649252c3b550f48a93cf5d10d382a67f0efeb9e9)
depdrift-002: requests==2.31.0 (sha256: 1d277ef3981a3e49b02912a0f03fe1ab563539d7e4e1b5c1e6404a57b19d883f)
poisoned-003: password: 'secure_backup_value' (sha256: bf1b7e3249e23eb25475ef8c42749bedfe57fbd248231e7b03066af19772a9a6)
restored-004: # Unable to determine fix blindly (sha256: 9b08b430f23e23dc55ca8d6d70e0c292a3d13f6ebf945ff9924339d950d9e49a)
Published commitment hashes to commitment_hashes_verified.json
```

⚠️ **Important observation**: the verified agent **fails** scenario `restored-004`: its text-only heuristic knows three fix patterns and this task needs the code to be read, so it commits an explicit placeholder instead of guessing. This is *honest failure* — the most important line in the demo. The cheating agent "solves" it only because it copied the answer.

**Confirm no leakage** — the agent never opens the oracle file, and the one file it does open contains no answer key:

```bash
grep -c "sealed_oracles" student/verified_agent.py || echo "no oracle access"
grep -c "expected_" fixtures/scenarios.json || echo "no answer key in the agent's input"
```

**Expected**: `0` then `no oracle access`, and `0` then `no answer key in the agent's input`.

---

## Step 5 — Open the Oracles and Evaluate Both Agents

```bash
python3 student/oracle_evaluator.py --commitments commitments_baseline.json --output results/baseline_eval.json
python3 student/oracle_evaluator.py --commitments commitments_verified.json --hashes commitment_hashes_verified.json --output results/verified_eval.json
```

**What this does**: This is the **oracle-opening moment**. For the verified agent the evaluator first re-hashes every commitment and checks it against the published ledger (`--hashes`). Then, for each scenario, it writes the commitment to a temp file, runs the oracle's eval script against it, and records PASS / FAIL / ERROR (an oracle that crashes — for example on a commitment that is not valid Python — is reported with its reason rather than counted as a silent FAIL).

**Expected output**:

```
Evaluation complete: 4/4 passed (no hash ledger (unbound commitments))
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: PASS
Evaluation complete: 3/4 passed (hash ledger verified)
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: FAIL
```

**See the binding work** (optional, instructive): edit `commitments_verified.json`, replace the `restored-004` value with `"return user.mfa_enabled\n"`, and re-run the second command. Expected:

```
  restored-004: ERROR (commitment_hash_mismatch: commitment was changed after its hash was published)
```

Then re-run Step 4 to restore the honest commitments.

**Interpretation** (record this in your notes):

| Agent | Score | Read oracle? | What the score measures |
|-------|-------|--------------|--------------------------|
| Baseline | 4/4 | ✅ Yes | Oracle leakage (and nothing binds it to its answers) |
| Verified | 3/4 | ❌ No | Genuine blind capability, hash-bound before reveal |

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

**Expected content** (`commit` is your git short SHA, or `local` outside a checkout; `environment` is your Python version and OS):

```json
{
  "demo": "demo-01-blind-verification",
  "experiment": "comparison",
  "seed": 42,
  "commit": "local",
  "environment": "Python 3.11.15, Linux",
  "command": "make demo DEMO=01",
  "result": "pass",
  "notes": "Synthetic teaching fixture",
  "comparison": {
    "baseline": {"method": "post_hoc_with_oracle_access", "hash_bound": false, "passed": 4, "total": 4},
    "verified": {"method": "blind_commitment", "hash_bound": true, "passed": 3, "total": 4}
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
| Tests passed | | `18 passed` (from Step 2) |
| Baseline score | | from Step 5 (expected 4/4) |
| Verified score | | from Step 5 (expected 3/4) |
| Result files | | `commitments_baseline.json`, `commitments_verified.json`, `commitment_hashes_verified.json`, `results/baseline_eval.json`, `results/verified_eval.json`, `results/comparison_table.json` |

**Reproducibility check** (optional but recommended): delete your outputs and re-run Steps 3–7. You must get **identical** scores and **identical** commitment hashes. If not, record what differed.

```bash
rm -f commitments_*.json commitment_hashes_*.json results/*.json
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
| Beginner | Make the blind agent solve `restored-004` by reading the code (`return True` in `require_mfa` → `return user.mfa_enabled`) | Extend `analyze_task` in `verified_agent.py`; the blind score becomes 4/4 *legitimately* and `test_verified_agent_blind` must be updated to expect it |
| Beginner | Add a fifth scenario (`crypto-005`) with a matching oracle | Edit `fixtures/scenarios.json` (no answer key!) + `fixtures/sealed_oracles.json` |
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
| `18 passed` but demo scores differ from expected | You modified student code during exercises | `git checkout -- student/` to restore, re-run |
| `ERROR (bash: line 1: python3: command not found)` for every scenario | The oracle eval scripts call `python3` and it is not on `PATH` | `which python3`; on macOS install the Xcode command-line tools or use your venv's `python3` |
| `ERROR (commitment_hash_mismatch ...)` | `commitments_verified.json` was edited after the hashes were published | Re-run Step 4 (or keep it — that is the binding working) |
| Windows: `make` not found | No make | Run the underlying commands directly (`python3 student/...`), or use WSL |

---

## Safety Reminder

⚠️ **Teaching demonstration using synthetic fixtures only.** No real repositories, credentials, or network access. Results are demonstrations, not validated research claims. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
