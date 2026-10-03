# Demo 37: Detector Cost — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 2 min | `python3 --version` |
| Enter demo directory | 1 min | `cd demo-37-detector-cost` |
| Run tests FIRST | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_cost.py` |
| Hand-built experiment | 5 min | Edit `fixtures/inputs.json`, re-run |
| Inspect benchmark artefact | 2 min | `cat results/detector_cost.json` |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~15 min** | |

**Safety**: 100% offline, standard library only. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

From the **repository root**:

```bash
python3 --version          # must be 3.11 or newer
python3 -m pytest --version  # confirms pytest is installed
```

**What this does**: Verifies Python ≥ 3.11 (the demo uses modern type syntax) and that pytest is available.

**Expected**: `Python 3.11.x` (or higher) and `pytest 7.x` (or higher).

**If it fails**: run `make setup` from this directory, then retry.

---

## Step 1 — Enter the Demo Directory

```bash
cd demo-37-detector-cost
```

**What this does**: All remaining commands run from inside this directory so relative paths to `fixtures/` and `student/` resolve.

**Verify you are in the right place**:

```bash
ls
# Expected: CITATION.cff  INSTRUCTIONS.md  Makefile  README.md  fixtures  results  student  tests
```

---

## Step 2 — Run the Tests FIRST (Baseline Sanity Check)

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **21 tests** that verify the demo's correctness: fixture integrity (10 inputs, unique ids, 4 injected / 6 benign, costs 10/25, seed 37), detector behaviour (strict 4/4 with 2 false positives, lenient 2/4 with 0 false positives), cost pricing (strict-cost-20 vs lenient-cost-50 with strict winning), the cost-flip experiment, results parity and schema, determinism, and stdlib-only imports. This extends the original 6-passed checkpoint (determinism, strict numbers, lenient numbers, cost winner, results parity, stdlib-only) — every original check is still present.

**Why tests before demo**: If any test fails, your environment is broken. Fix it now — otherwise you won't know whether a strange demo result is your fault or the code's.

**Expected output (end of run)**:

```
tests/test_detector_cost.py::TestCostFlip::test_cost_flip_when_fn_cheap PASSED
====================== 21 passed in 0.XXs ======================
```

✅ **Checkpoint**: You must see `21 passed`. If you see failures, see [Troubleshooting](#troubleshooting) below.

---

## Step 3 — Run the Cost Comparison

```bash
python3 student/run_cost.py
```

**What this does**: Scores both toy detectors on the same 10 hand-built prompts (4 injected, 6 benign), prices false positives at 10 and false negatives at 25, declares the cheaper operating point, and writes `results/detector_cost.json`.

**Why this step exists**: This is the *measurement*. Both detectors see identical inputs, so the only difference is their operating point: strict catches everything but cries wolf twice; lenient never cries wolf but misses the two paraphrased injections. Pricing converts that trade-off into one number per detector.

**Expected output**:

```text
fp_cost 10  fn_cost 25
detector  tp   fp   fn   cost
strict    4/4  2/6  0/4  20
lenient   2/4  0/6  2/4  50
winner: strict (cost 20 < 50).
```

**Files created**: `results/detector_cost.json`.

**Interpretation** (record this in your notes):

| Detector | TP | FP | FN | Cost (FP=10, FN=25) | What the score measures |
|----------|----|----|----|----------------------|--------------------------|
| Strict | 4/4 | 2/6 | 0/4 | 2×10 + 0×25 = 20 | Recall at the price of wolf-cries |
| Lenient | 2/4 | 0/6 | 2/4 | 0×10 + 2×25 = 50 | Precision at the price of misses |

Lesson: under these asymmetric costs, the noisier detector is the cheaper one.

---

## Step 4 — Hand-Built Experiment (Break It)

Change `fn_cost` in `fixtures/inputs.json` from 25 to 5 and re-run both commands:

```bash
python3 student/run_cost.py
python3 -m pytest tests/ -v -k "not test_cost_pricing_picks_strict and not test_lenient_cost_arithmetic and not test_results_file_matches_memory"
```

**What this does**: Re-prices a missed injection at 5 instead of 25 while a false alarm still costs 10. Nothing about the detectors changes — only the costs.

**Why this step exists**: Operating-point decisions live in the cost model, not in the detector. The same two detectors, the same ten prompts, a different winner.

**Expected output**:

```text
fp_cost 10  fn_cost 5
detector  tp   fp   fn   cost
strict    4/4  2/6  0/4  20
lenient   2/4  0/6  2/4  10
winner: lenient (cost 10 < 20).
```

Strict still costs 20 (2×10 + 0×5); lenient drops to 10 (0×10 + 2×5) and wins. Record: the winner flipped from strict to lenient. That tells you detectors are tuned with costs, not accuracy — whoever sets the prices picks the winner.

Restore the fixture when finished:

```bash
git checkout -- fixtures/inputs.json
python3 student/run_cost.py
```

---

## Step 5 — Inspect the Benchmark Artefact

```bash
cat results/detector_cost.json
```

**What this does**: Shows the demo's final artefact in the standardized result schema: costs, per-detector tallies, winner, seed, and provenance note.

**Expected content** (`commit` is not stored here; provenance is the seed plus the note):

```json
{
  "demo": "demo-37-detector-cost",
  "experiment": "detector-cost",
  "seed": 37,
  "fp_cost": 10,
  "fn_cost": 25,
  "strict": {"tp": 4, "fp": 2, "fn": 0, "tn": 4, "cost": 20},
  "lenient": {"tp": 2, "fp": 0, "fn": 2, "tn": 6, "cost": 50},
  "winner": "strict",
  "notes": "Synthetic teaching fixture"
}
```

**Why this step exists**: This JSON is the *benchmark* other runs compare against. `test_results_file_matches_memory` and `test_results_schema` enforce its shape: fixed keys, seed 37, the teaching-fixture note. If you extend the fixture (see Exercises), this file is where the new numbers land.

---

## Step 6 — Reproducibility Record (Required for Study Participants)

Fill in this table and submit it with your results. Every field is required for your run to be reproducible.

| Field | Your value | How to obtain it |
|-------|------------|------------------|
| Date of run | | today's date |
| Seed | `37` | fixed by the demo |
| Git commit | | `git rev-parse --short HEAD` (from repo root) |
| Python version | | `python3 --version` |
| Operating system | | `uname -a` (macOS/Linux) or `systeminfo` (Windows) |
| Command(s) used | | copy exactly from Steps 3–5 above |
| Tests passed | | `21 passed` (from Step 2) |
| Strict cost | | from Step 3 (expected 20) |
| Lenient cost | | from Step 3 (expected 50) |
| Winner | | from Step 3 (expected strict) |
| Result files | | `results/detector_cost.json` |

**Reproducibility check** (optional but recommended): delete your outputs and re-run Steps 3–5. You must get **identical** costs and an **identical** results file. If not, record what differed.

```bash
rm -f results/detector_cost.json
python3 student/run_cost.py
cat results/detector_cost.json
# ...compare against your saved copy: costs 20 vs 50, winner strict...
```

---

## Alternative: One-Command Run

If you want the whole pipeline in one command, from **this directory**:

```bash
make demo
```

**What this does**: Chains setup and the cost comparison (Steps 3–5 automatically) and prints the final table plus the results path.

From the **repository root** (all demos):

```bash
make demo DEMO=37
```

---

## Exercises (Tiered)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Add an 11th prompt: a benign message containing "ignore" in a harmless context (e.g. "kindly ignore this reminder if already paid") and predict strict's new FP count before running | Strict flags any `ignor` substring, so FP rises to 3/7; update `test_fixture_balance_4_injected_6_benign` accordingly |
| Beginner | Add a fifth injected prompt carrying the exact phrase "ignore previous instructions" | Both detectors catch it: strict 5/5, lenient 3/5 — re-run Step 2 and record which tests break |
| Standard | Sweep `fn_cost` over 5, 10, 25, 50 in a shell loop and find the flip point where the winner changes | Strict costs 20 always; lenient costs 2×fn_cost — the flip is where 2×fn_cost crosses 20 |
| Standard | Build a **false positive the lenient detector catches**: impossible by construction — prove it, then relax the lenient phrase and show the FP count move | The exact-phrase rule cannot fire on benign text that avoids the phrase; any relaxation trades FPs for TPs |
| Extension | Replace the substring rules with a scored rule (e.g. count of suspicious tokens) and select the operating point at fixed FPR ≤ 1/6 | Mirrors the research protocol (`analysis/detector_protocol.md`): fix the false-positive rate, then read recall |
| Extension | Write a third detector (e.g. case-sensitive match) and extend the cost table plus `test_cost_pricing_picks_strict` | The winner logic (`<=` favours strict on ties) must be re-examined with three players |

After any exercise, re-run Step 2 (tests) and Step 3 (demo) and record how your changes affected the scores.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'pytest'` | Dependencies not installed | `make setup` or `python3 -m pip install pytest` |
| `FileNotFoundError: fixtures/inputs.json` | Wrong working directory | `cd demo-37-detector-cost` first |
| Tests fail with JSON decode error | Corrupted fixture (possibly edited in Step 4) | `git checkout -- fixtures/inputs.json` to restore, re-run |
| `21 passed` but demo costs differ from expected | You modified student code or fixture during exercises | `git checkout -- student/ fixtures/` to restore, re-run |
| Winner is lenient at default costs | `fn_cost` still 5 from the Step 4 experiment | Restore: `git checkout -- fixtures/inputs.json`, re-run Step 3 |
| `test_results_file_matches_memory` fails | Stale `results/detector_cost.json` from an edited fixture | Delete it and re-run `python3 student/run_cost.py` |
| Windows: `make` not found | No make | Run the underlying commands directly (`python3 student/...`), or use WSL |

---

## Safety Reminder

⚠️ **Teaching demonstration using synthetic fixtures only.** No real prompts, models, detectors, or credentials. No network access (standard library only). Results demonstrate a mechanism — operating-point selection under asymmetric costs — not validated research claims. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
