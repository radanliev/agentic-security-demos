# Demo 45: Exact Nulls — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_nulls.py` (or `make demo DEMO=45` from root) |
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

**Expected**: `5 passed` (known tail, score ordering, transfer gap, design limit, results parity).

## Step 2 — Run the Null Check

```bash
python3 student/run_nulls.py
```

**Expected**:

```text
cases 8  alpha 0.01
transfer check: same recall 0.5 but p 1.84564e-05 vs 0.00155615; lift 5.0 vs 2.5 (not comparable).
design limit D=10 k=2 alpha=0.01: need pool >= 96
```

This also writes `results/nulls.json`.

## Step 3 — Break It (Exercise)

Change `case2`'s `tp` from `2` to `5` in `fixtures/cases.json` and re-run
both commands. Record: does case2 flip to significant? Why does the same
recall 0.50 in case5 vs case6 give p-values ~84x apart — and what does that
say about comparing lifts across corpora?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Significant cases at 0.01 | ___ |
| Transfer p-values | A ___ vs B ___ |
| Commit | Git SHA or `local` |
