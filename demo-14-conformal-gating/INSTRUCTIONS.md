# Demo 14: Conformal Action Gating — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_gate.py` (or `make demo DEMO=14` from root) |
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

**Expected**: `6 passed` (determinism, calibration 0.20, same-corpus holds,
shifted fails, oracle separation, results parity).

## Step 2 — Run the Gate

```bash
python3 student/run_gate.py
```

**Expected**:

```text
alpha 0.3  calibrated threshold 0.2
gate        set      exec  risk   benign-blocked
conformal  same     1/4    0.00  1/2
conformal  shifted  2/4    1.00  1/1
fixed-0.5  same     2/4    0.00  0/2
fixed-0.5  shifted  3/4    0.67  0/1
lesson: same-corpus holds (risk 0.00 <= 0.30); shifted fails (risk 1.00).
```

This also writes `results/gating_eval.json`.

## Step 3 — Break It (Exercise)

Change `alpha` in `fixtures/episodes.json` from 0.30 to 0.10 and re-run both
commands. Record: does the calibrated threshold move? Does the shifted failure
survive? Why does a tighter budget not fix shift?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 6 passed / ___ failed |
| Calibrated threshold | ___ |
| Same risk / Shifted risk | ___ / ___ |
| Commit | Git SHA or `local` |
