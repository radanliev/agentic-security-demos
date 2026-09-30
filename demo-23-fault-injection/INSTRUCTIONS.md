# Demo 23: Agent Pipeline Fault Injection — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_faults.py` (or `make demo DEMO=23` from root) |
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

**Expected**: `5 passed` (determinism, no-retry 2/6 graceful, retry-2 5/6
graceful, spot checks, results parity).

## Step 2 — Run the Scorecard

```bash
python3 student/run_faults.py
```

**Expected**:

```text
fault-injection scorecard (seed 23): 6 faults
mode       graceful  cascade  silent-wrong  cost-blowup
no-retry   2/6        2/6        1/6             1/6
retry-2    5/6        1/6        0/6             0/6
lesson: retries lift graceful from 2/6 to 5/6; the permanent fault still cascades.
```

This also writes `results/faults.json`.

## Step 3 — Break It (Exercise)

Change `RETRY_BUDGET` in `student/faults.py` from 2 to 1 and re-run both
commands. Record: does `outcome(f, 1)` use the retry table or the no-retry
table? What does that say about off-by-one budget checks in real retry code?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| No-retry graceful / Retry-2 graceful | ___ / ___ |
| Fault that still cascades | ___ |
| Commit | Git SHA or `local` |
