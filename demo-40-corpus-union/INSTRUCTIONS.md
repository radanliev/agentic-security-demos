# Demo 40: Corpus Union — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_corpus.py` (or `make demo DEMO=40` from root) |
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

**Expected**: `6 passed` (determinism, 9 unique after dedupe, normalisation
folding, 7/9 releasable with r07+r08 blocked, results parity, stdlib-only).

## Step 2 — Run the Union

```bash
python3 student/run_corpus.py
```

**Expected**:

```text
records 12  unique 9
duplicates removed 3
releasable 7/9
blocked: r07, r08.
```

This also writes `results/corpus.json`.

## Step 3 — Break It (Exercise)

Change `r07`'s licence to `permissive` in `fixtures/records.json` and re-run
both commands. Record: does the releasable count move to 8/9? Why does the
licence gate — not the dedupe — own that change?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 6 passed / ___ failed |
| Unique / Releasable | ___ / ___ |
| Blocked ids | ___ |
| Commit | Git SHA or `local` |
