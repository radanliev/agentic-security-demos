# Demo 03: Evaluation Invariants — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md). Full course lab: [../docs/course/lab-03-eval-invariants.md](../docs/course/lab-03-eval-invariants.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the five invariants | 2 min | `python3 student/eval_invariants.py` |
| Generate summary table | 1 min | `python3 student/generate_summary.py` |
| Four-arm analysis | 5 min | inline script (Step 5) |
| **Total** | **~15 min** | |

**Safety**: 100% offline. Synthetic tasks and model outputs; no dataset downloads, no model API calls. Every number in the fixture is invented for teaching.

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

**What this does**: Shows the evaluation card (5 tasks, a `pass_threshold` and a `failure_taxonomy`), synthetic outputs for two models (each with a `score`, three recorded scoring `runs` and a `failure_category`), the dataset's declared `training_data_indicators`, a four-document `training_corpus`, and the `run_metadata` block.

**Find the planted flaw before running**: compare the task prompts with `training_corpus`. Write down:

1. Which task's prompt appears verbatim in the corpus? ______
2. Which task is declared `in_training: true`? ______ (the leakage invariant flags a task once, listing every reason that applies; the n-gram threshold is 0.10)
3. Look at that task's scores: baseline ______, verified ______. Which model does the leak help?
4. Prediction: which of the five invariants will PASS, which will FAIL?

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

**Expected**: `25 passed`. Every invariant is tested both ways — it passes on the healthy fixture and fails on a copy that has the defect (a planted overlap, flaky runs, an unlabelled failure, a missing commit). Pay attention to `test_invariant_1_no_leakage` (asserts task-003 is caught, once) and `test_four_arm_comparison` (the module thesis computed from the data).

```
============================== 25 passed in 0.XXs ==============================
```

---

## Step 3 — Run All Five Invariants

```bash
python3 student/eval_invariants.py
```

**What this does**: Executes the five invariant checks against the fixture, prints one line per invariant, recomputes each model's headline with leaked tasks excluded, and saves `results/invariant_results.json` (whose `summary.run_metadata` block records this run's commit, Python version and OS).

**Expected output** (compare with your Step 1 predictions):

```
invariant_1_no_leakage: passed=False  1 of 5 tasks show leakage indicators: task-003 (declared in_training, 3-gram overlap 1.00 > 0.1)
invariant_2_adequate_difficulty: passed=False  low variance (0.032 < 0.05); ceiling effect (4/10 scores >= 0.95, limit 30%)
invariant_3_stable_scoring: passed=True  10 items x recorded runs, max spread 0.000 <= 0.01
invariant_4_correct_failure_classification: passed=True  2 failures below 0.7 among 10 outputs; 0 misclassified
invariant_5_reproducible_metadata: passed=True  all of seed, commit, environment, command recorded
summary: all_passed=False, passed_count=3/5, failed=['invariant_1_no_leakage', 'invariant_2_adequate_difficulty']

baseline-agent   headline=0.88  clean-mean=0.85  (excluding task-003)
verified-agent   headline=0.81  clean-mean=0.84  (excluding task-003)
```

**Record**: which of your predictions were right? Note that `task-003` is listed **once** with **two** reasons: the dataset declares it in training, and the check itself found its prompt verbatim in the corpus (overlap 1.00). One root cause, two independent signals.

Add `--strict` to make the script exit 1 when any invariant fails — that is how CI would gate on evaluation health.

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
  FAIL  no_leakage: 1 of 5 tasks show leakage indicators: task-003 (declared in_training, 3-gram overlap 1.00 > 0.1)
  FAIL  adequate_difficulty: low variance (0.032 < 0.05); ceiling effect (4/10 scores >= 0.95, limit 30%)
  PASS  stable_scoring: 10 items x recorded runs, max spread 0.000 <= 0.01
  PASS  correct_failure_classification: 2 failures below 0.7 among 10 outputs; 0 misclassified
  PASS  reproducible_metadata: all of seed, commit, environment, command recorded
============================================================
Overall: SOME FAILED (3/5 passed)

Headline vs clean-task mean (leaked tasks excluded):
  baseline-agent   0.88 -> 0.85  (-0.03)
  verified-agent   0.81 -> 0.84  (+0.03)
```

**Why this matters**: this table is what you would attach to a real evaluation report — five lines that summarize evaluation health, and two that say what the headline numbers are worth.

---

## Step 5 — Four-Arm Analysis (The Module Thesis in Numbers)

```bash
python3 - << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, "student")
from eval_invariants import EvaluationInvariants

inv = EvaluationInvariants(Path("fixtures/eval_data.json"))
leak = inv.check_no_leakage()
for model, v in inv.headline_vs_clean(leak).items():
    print(f"{model:16} headline={v['headline']:.2f}  clean-mean={v['clean']:.2f}  "
          f"(excluding {', '.join(v['excluded'])})")

print()
print("Four arms:")
print("  baseline, invariants ignored -> 0.88, meaning: UNKNOWN")
print("  baseline, invariants run     -> 0.88, inflated by task-003 (0.85 on clean items)")
print("  verified, invariants ignored -> 0.81, meaning: UNKNOWN")
print("  verified, invariants run     -> 0.81, not inflated (0.84 on clean items)")
EOF
```

**What this does**: Computes each model's headline mean score, then recomputes it *excluding leaked tasks*.

**Expected output** (first two lines):

```
baseline-agent   headline=0.88  clean-mean=0.85  (excluding task-003)
verified-agent   headline=0.81  clean-mean=0.84  (excluding task-003)
```

**What to record**: the baseline scores 1.0 on the leaked task (its output is "identical to the reference solution") — dropping it lowers the baseline by 0.03. The verified agent scored 0.7 there, below its own average, so dropping it *raises* its mean. The headline gap between the models (0.07) shrinks to 0.01 on clean items. **That shrinkage is the leakage inflation, quantified.**

**The thesis**: invariants are properties of the evaluation, not of a model. A high headline score on an evaluation whose invariants fail is a weak result; the invariant tells you *which items* inflated *whom*.

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

**What this does**: Re-runs the difficulty invariant with three threshold settings (`max_ceiling` is the score at which an item counts as "at ceiling"; the invariant fails when more than 30% of scores are there).

**Expected output**:

```
min_var=0.05 max_ceil=0.95 -> passed=False issues=['low variance (0.032 < 0.05)', 'ceiling effect (4/10 scores >= 0.95, limit 30%)']
min_var=0.01 max_ceil=0.99 -> passed=True issues=[]
min_var=0.1 max_ceil=0.9 -> passed=False issues=['low variance (0.032 < 0.1)', 'ceiling effect (7/10 scores >= 0.9, limit 30%)']
```

**Lesson**: invariants have parameters, and parameters encode judgment calls. The same ten scores pass or fail depending on the thresholds. Record which thresholds you would choose and why.

---

## Step 7 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` (also written to `results/invariant_results.json` under `summary.run_metadata`) |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2–5 |
| Tests passed | | `25 passed` |
| Invariants passed | | count from Step 3 summary (expected 3 of 5) |
| Leaked task(s) | | `task-003` |
| Result file | | `results/invariant_results.json` |

**Reproducibility check**: `rm -rf results/`, re-run Steps 3–4, and confirm the JSON is identical apart from the `summary.run_metadata` block (which records the commit, Python version and OS of *your* run).

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=03`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Extend `ngram_overlap` to Jaccard similarity and compare it with containment on the fixture | On a 9-gram prompt a single shared trigram is already 0.11 > 0.10 — is the threshold right for short items? |
| Standard | Add a saturation detector (`check_saturation`) | Fail if ≥50% of *tasks* are in `saturated_tasks` |
| Standard | Difficulty ladder: rank tasks by empirical pass rate | Compare with the fixture's `difficulty` labels (see `test_exercise_item_response`) |
| Extension | Real stability check with an injected flaky scorer | `check_stability(scorer=FlakyScorer(...), runs=10)` — see `test_invariant_3_with_injected_scorer` |
| Extension | Design a 6th invariant (calibration, coverage, budget…) | Document failure mode + threshold rationale; add a failing-input test |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `25 passed` fails after your edits | Exercise changes broke invariants | `git checkout -- student/ fixtures/` to reset |
| `FileNotFoundError: fixtures/eval_data.json` | Wrong directory | `cd demo-03-eval-invariants` |
| `invariant_5` reports `missing: seed` | Fixture edited; `run_metadata.seed` removed | `git checkout -- fixtures/` |
| `invariant_3` reports `unverifiable` items | Fixture edited; an item lost its `runs` list | `git checkout -- fixtures/` |
| JSON decode error | Fixture corrupted | `git checkout -- fixtures/eval_data.json` |

---

## Safety Reminder

⚠️ **Teaching demonstration only.** Synthetic tasks/outputs; no external datasets; no model API calls. Results are demonstrations, not research claims. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
