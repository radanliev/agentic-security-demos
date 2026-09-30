# Demo 30: Insecure Defaults — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_defaults.py` (or `make demo DEMO=30` from root) |
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

**Expected**: `5 passed` (determinism, 6/10 insecure, 3/10 pinned, rule
spot-check, results parity).

## Step 2 — Run the Checker

```bash
python3 student/run_defaults.py
```

**Expected**:

```text
id   insecure  reasons
s01  True      public-without-auth
s02  False     -
s03  True      privileged
s04  True      pinned-vuln
s05  True      privileged
s06  False     -
s07  True      public-without-auth,pinned-vuln
s08  False     -
s09  True      pinned-vuln
s10  False     -
insecure 6/10  pinned-vuln 3/10
```

This also writes `results/defaults.json`.

## Step 3 — Break It (Exercise)

Give `s02` `privileged: true` in `fixtures/stacks.json` and re-run both
commands. Record: does the insecure count move to 7/10? Which reason fires?
Why does one flag flip the whole verdict?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Insecure / Pinned | ___ /10 / ___ /10 |
| Commit | Git SHA or `local` |
