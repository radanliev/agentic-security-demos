# Demo 03: Evaluation Invariants — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md). Full course lab: [../docs/course/lab-03-eval-invariants.md](../../docs/course/lab-03-eval-invariants.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the five invariants | 2 min | `python3 student/eval_invariants.py` |
| Generate summary table | 1 min | `python3 student/generate_summary.py` |
| Four-arm analysis | 5 min | inline script (Step 5) |
| **Total** | **~15 min** | |

**Safety**: 100% offline. Synthetic tasks and model outputs; no dataset downloads, no model API calls.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-03-eval-invariants
```

---

## Step 1 — Read the Fixture and Predict (Before Running)

```bash
cat fixtures/eval_data.json
```

**What this does**: Shows the evaluation card (5 tasks), synthetic outputs for two models, and — crucially — `training_data_indicators`.

**Find the planted flaw before running**: look at `training_data_indicators` for `task-003`. Write down:

1. Which task is leaked into training data? ______
2. Its n-gram overlap value: ______ (threshold for the leakage invariant is 0.10)
3. Prediction: which of the five invariants will PASS, which will FAIL?

| Invariant | My prediction (PASS/FAIL) |
|-----------|---------------------------|
| 1. no_leakage | |
| 2. adequate_difficulty | |
| 3. stable_scoring | |
| 4. correct_failure_classification | |
| 5. reproducible_metadata | |

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected**: `13 passed`. Pay attention to `test_invariant_1_no_leakage` (asserts task-003 is caught) and `test_high_score_weak_evaluation` (the module thesis as an assertion).

```
============================== 13 passed in 0.XXs ==============================
```

---

## Step 3 — Run All Five Invariants

```bash
python3 student/eval_invariants.py
```

**What this does**: Executes the five invariant checks against the fixture and saves `results/invariant_results.json`.

**Expected output** (key excerpts — compare with your Step 1 predictions):

```
invariant_1_no_leakage: passed=False, leaked_tasks=['task-003', 'task-003']
invariant_2_adequate_difficulty: passed=False (mean/variance issues listed)
invariant_3_stable_scoring: passed=True
invariant_4_correct_failure_classification: passed=True
invariant_5_reproducible_metadata: passed=True, seed=42
summary: all_passed=False
```

**Record**: which of your predictions were right? Note that `task-003` appears **twice** in the leaked list — flagged once for `in_training=true` and once for `ngram_overlap > 0.1`. One root cause, two flags.

---

## Step 4 — Generate the Human-Readable Summary

```bash
python3 student/generate_summary.py
```

**What this does**: Re-runs the invariants and prints a formatted PASS/FAIL table.

**Expected output**:

```
Invariant Summary:
============================================================
  PASS  stable_scoring:
  PASS  correct_failure_classification:
  PASS  reproducible_metadata:
  FAIL  no_leakage: 1 tasks show leakage indicators
  FAIL  adequate_difficulty: [...]
============================================================
Overall: SOME FAILED
```

**Why this matters**: this table is what you would attach to a real evaluation report — five lines that summarize evaluation health.

---

## Step 5 — Four-Arm Analysis (The Module Thesis in Numbers)

```bash
python3 - << 'EOF'
import json, statistics
from pathlib import Path
import sys
sys.path.insert(0, "student")
from eval_invariants import EvaluationInvariants

data = json.loads(Path("fixtures/eval_data.json").read_text())
inv = EvaluationInvariants(Path("fixtures/eval_data.json"))
leak = inv.check_no_leakage()

for model in ["baseline-agent", "verified-agent"]:
    scores = [v["score"] for v in data["synthetic_outputs"][model].values()]
    clean = [v["score"] for tid, v in data["synthetic_outputs"][model].items()
             if tid not in leak["leaked_tasks"]]
    print(f"{model:16} headline={statistics.mean(scores):.2f}  "
          f"clean-task-mean={statistics.mean(clean):.2f}")

print()
print("Four arms:")
print("  baseline, invariants ignored -> high score, trust: UNKNOWN")
print("  baseline, invariants run     -> high score, trust: NO (leakage)")
print("  verified, invariants ignored -> lower score, trust: UNKNOWN")
print("  verified, invariants run     -> lower score, trust: YES")
EOF
```

**What this does**: Computes each model's headline mean score, then recomputes it *excluding leaked tasks*.

**What to record**: the gap between headline and clean-task mean for the baseline — **that gap is the leakage inflation, quantified**.

**The thesis**: a high headline score with failed invariants is a weak evaluation. The lower score with passing invariants is the only trustworthy result.

---

## Step 6 — Threshold Sensitivity Experiment (Recommended)

```bash
python3 - << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, "student")
from eval_invariants import EvaluationInvariants

inv = EvaluationInvariants(Path("fixtures/eval_data.json"))
for mv, mc in [(0.05, 0.95), (0.01, 0.99), (0.10, 0.90)]:
    r = inv.check_difficulty(min_variance=mv, max_ceiling=mc)
    print(f"min_var={mv} max_ceil={mc} -> passed={r['passed']} issues={r['issues']}")
EOF
```

**What this does**: Re-runs the difficulty invariant with three threshold settings.

**Lesson**: invariants have parameters, and parameters encode judgment calls. Record which thresholds you would choose and why.

---

## Step 7 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2–5 |
| Tests passed | | `13 passed` |
| Invariants passed | | count from Step 3 summary (expected 3 of 5) |
| Leaked task(s) | | `task-003` |
| Result file | | `results/invariant_results.json` |

**Reproducibility check**: `rm -rf results/`, re-run Steps 3–4, and confirm the JSON is identical.

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=03`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Implement word-level n-gram overlap from scratch | Jaccard over 3-gram sets |
| Standard | Add a saturation detector (`check_saturation`) | Fail if ≥50% of scores ≥ 0.95 |
| Standard | Difficulty ladder: rank tasks by empirical pass rate | Compare with the fixture's `difficulty` labels |
| Extension | Real stability check with an injected flaky scorer | Wrap the scorer; score each item 10×; flag spread > 0.01 |
| Extension | Design a 6th invariant (calibration, coverage, budget…) | Document failure mode + threshold rationale |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `13 passed` fails after your edits | Exercise changes broke invariants | `git checkout -- student/ fixtures/` to reset |
| `FileNotFoundError: fixtures/eval_data.json` | Wrong directory | `cd demo-03-eval-invariants` |
| `invariant_5` fails with `missing seed` | Fixture edited; seed removed | `git checkout -- fixtures/` |
| JSON decode error | Fixture corrupted | `git checkout -- fixtures/eval_data.json` |

---

## Safety Reminder

⚠️ **Teaching demonstration only.** Synthetic tasks/outputs; no external datasets; no model API calls. Results are demonstrations, not research claims. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
