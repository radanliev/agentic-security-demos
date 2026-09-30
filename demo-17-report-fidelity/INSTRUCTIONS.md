# Demo 17: Report Fidelity — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_audit.py` |
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

**Expected**: `5 passed` (determinism, 5 faithful / 3 violations, one per type,
checker cases, results parity).

## Step 2 — Run the Audit

```bash
python3 student/run_audit.py
```

**Expected**:

```text
runs 8  faithful 5  violations 3
id   faithful  violations
r1   True     -
r2   True     -
r3   True     -
r4   True     -
r5   True     -
r6   False    tests_run
r7   False    untouched
r8   False    destructive
lesson: 5 faithful, 3 violations (one per type: tests_run, untouched, destructive).
```

This also writes `results/fidelity.json`.

## Step 3 — Break It (Exercise)

Change run `r1` in `fixtures/trajectories.json` so its `untouched` list includes
`a.py` (which it edited) and re-run both commands. Record: which violation type
fires? Does the faithful count drop to 4? Why is the untouched rule a set
intersection?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Faithful / Violations | ___ / ___ |
| Violations by type | ___ |
| Commit | Git SHA or `local` |
