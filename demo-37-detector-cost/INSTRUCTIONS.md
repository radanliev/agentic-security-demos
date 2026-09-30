# Demo 37: Detector Cost — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_cost.py` (or `make demo DEMO=37` from root) |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~10 min** | |

**Safety**: 100% offline, standard library only. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

```bash
python3 --version          # must be 3.11 or newer
```

**Expected**: `Python 3.11.x` (or higher).

## Step 1 — Run the Tests

From this directory:

```bash
python3 -m pytest tests/ -v
```

**Expected**: `6 passed` (determinism, strict 4/4 + 2 FPs, lenient 2/4 + 0 FPs,
cost 20 vs 50 with strict winning, results parity, stdlib-only).

## Step 2 — Run the Cost Comparison

```bash
python3 student/run_cost.py
```

**Expected**:

```text
fp_cost 10  fn_cost 25
detector  tp   fp   fn   cost
strict    4/4  2/6  0/4  20
lenient   2/4  0/6  2/4  50
winner: strict (cost 20 < 50).
```

This also writes `results/detector_cost.json`.

## Step 3 — Break It (Exercise)

Change `fn_cost` in `fixtures/inputs.json` from 25 to 5 and re-run both
commands. Record: does the winner flip to lenient? What does that tell you
about tuning with costs instead of accuracy?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 6 passed / ___ failed |
| Strict cost / Lenient cost | ___ / ___ |
| Winner | ___ |
| Commit | Git SHA or `local` |
