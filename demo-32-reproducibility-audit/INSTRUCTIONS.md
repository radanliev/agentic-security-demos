# Demo 32: Reproducibility Audit — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_audit.py` (or `make demo DEMO=32` from root) |
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

**Expected**: `5 passed` (determinism, 6/10 code+data with 4/10 reproduce,
channel breakdown, invariant, results parity).

## Step 2 — Run the Audit

```bash
python3 student/run_audit.py
```

**Expected**:

```text
channel     n  reproduces
content     3  2
memory      2  1
multiagent  2  0
tool        3  1
code+data 6/10  reproduces 4/10
```

This also writes `results/sok_audit.json`.

## Step 3 — Break It (Exercise)

Flip `p05` to `code: true, data: true` (still `reproduces: false`) in
`fixtures/papers.json` and re-run both commands. Record: does the code+data
count move to 7/10? Does the reproduce count change? Why can sharing rise
while reproduction stays flat?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Code+data / Reproduces | ___ /10 / ___ /10 |
| Commit | Git SHA or `local` |
