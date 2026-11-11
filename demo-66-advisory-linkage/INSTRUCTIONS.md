# Demo 66: Advisory Linkage — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_linkage.py` (or `make demo DEMO=66` from root) |
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

**Expected**: all tests passed.

## Step 2 — Run the Demonstration

```bash
python3 student/run_linkage.py
```

This writes `results/linkage.json`.

## Step 3 — Break It (Exercise)

Change one labelled row in `fixtures/advisories.json` and re-run both
commands. Record which printed line moved and why the toy verdict changed.

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | ___ passed / ___ failed |
| Rows written | ___ |
| Commit | Git SHA or `local` |
