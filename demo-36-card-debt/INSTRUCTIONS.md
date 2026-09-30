# Demo 36: Model Card Debt — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_cards.py` (or `make demo DEMO=36` from root) |
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

**Expected**: `5 passed` (determinism, 7/12 missing, popularity gap, helper,
results parity).

## Step 2 — Run the Card Audit

```bash
python3 student/run_cards.py
```

**Expected**:

```text
id   downloads  safety
c01   95000      True
c02   80000      True
c03   70000      False
c04   60000      True
c05   50000      False
c06   40000      False
c07   30000      True
c08   20000      False
c09   15000      False
c10   10000      True
c11   5000       False
c12   1000       False
missing safety 7/12
top-4 missing 1/4  bottom-8 missing 6/8
```

This also writes `results/cards.json`.

## Step 3 — Break It (Exercise)

Give `c03` `safety: true` in `fixtures/cards.json` and re-run both commands.
Record: does overall missing drop to 6/12? Does the top-4 gap vanish to 0/4?
Why does fixing one popular card hide the tail debt?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Missing / Top / Bottom | ___ /12 / ___ /4 / ___ /8 |
| Commit | Git SHA or `local` |
