# Demo 19: Lineage Risk — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_lineage.py` |
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

**Expected**: `5 passed` (determinism, 6/8 risky, origin split, inheritance
case, results parity).

## Step 2 — Run the Lineage

```bash
python3 student/run_lineage.py
```

**Expected**:

```text
models 8  risky 6/8
id   kind
A    safe
B    origin
a1   safe
a2   introduced
b1   inherited
b2   inherited
c1   inherited
c2   introduced
origin 1  introduced 2  inherited 3
lesson: 6/8 risky; clean-looking children inherit risk from flagged parents.
```

This also writes `results/lineage.json`.

## Step 3 — Break It (Exercise)

Flip model `B` in `fixtures/models.json` to `"pickle": false` and re-run both
commands. Record: which models flip from risky to safe? Why do b1, b2 change
but a2, c2 stay risky?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Risky / total | ___ / ___ |
| Origin / Introduced / Inherited | ___ / ___ / ___ |
| Commit | Git SHA or `local` |
