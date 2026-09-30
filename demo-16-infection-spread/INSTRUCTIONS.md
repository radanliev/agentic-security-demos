# Demo 16: Infection Spread — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_spread.py` |
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

**Expected**: `5 passed` (determinism, uncontained 6/6, chain containment 2/6,
chain R0, results parity).

## Step 2 — Run the Spread

```bash
python3 student/run_spread.py
```

**Expected**:

```text
p 0.9  seed 16
topo   r0    infected  contained
chain  1.50  6/6       2/6
star   1.50  6/6       -
mesh   2.70  6/6       -
tree   1.50  6/6       -
lesson: uncontained spread reaches 6/6 everywhere; blocking 4 chain edges holds the chain at 2/6.
```

This also writes `results/spread.json`.

## Step 3 — Break It (Exercise)

Remove one edge from `chain_blocked_edges` in `fixtures/graphs.json` (keep 3 of
4) and re-run both commands. Record: how many nodes does the chain infect now?
Why does a single unblocked bridge undo containment on a chain?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| R0 (chain) | ___ |
| Uncontained / Chain contained | ___ / ___ |
| Commit | Git SHA or `local` |
