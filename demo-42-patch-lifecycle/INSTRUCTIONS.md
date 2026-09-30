# Demo 42: Patch Lifecycle — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_cycle.py` (or `make demo DEMO=42` from root) |
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

**Expected**: `5 passed` (determinism, median 37.5 days, 2/8 pin-blocked,
results parity, stdlib-only).

## Step 2 — Run the Lifecycle Summary

```bash
python3 student/run_cycle.py
```

**Expected**:

```text
vulns 8  lags [5, 12, 20, 30, 45, 60, 90, 180]
median adopt lag 37.5 days
blocked by pin 2/8: vuln04, vuln07.
```

This also writes `results/lifecycle.json`.

## Step 3 — Break It (Exercise)

Change `vuln08`'s `adopt_lag_days` from 180 to 40 in `fixtures/vulns.json`
and re-run both commands. Record: how far does the median move? Why is the
median (not the mean) the lifecycle statistic worth reporting here?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Median adopt lag | ___ |
| Blocked by pin | ___ |
| Commit | Git SHA or `local` |
