# Demo 20: Agent Web Census — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_web.py` |
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

**Expected**: `5 passed` (determinism, adoption 4/10, injections low-pop,
helper definitions, results parity).

## Step 2 — Run the Census

```bash
python3 student/run_web.py
```

**Expected**:

```text
sites 10  adopting 4/10  exposed 2/10
id   popularity  adopted  exposed
s01  high       True     False
s02  high       True     False
s03  medium     True     False
s04  low        True     True
s05  low        False    True
s06  high       False    False
s07  medium     False    False
s08  medium     False    False
s09  low        False    False
s10  low        False    False
lesson: adoption 4/10; injections 2/10, both on low-popularity sites.
```

This also writes `results/web_census.json`.

## Step 3 — Break It (Exercise)

Give site `s06` in `fixtures/sites.json` `"llms_txt": true` and re-run both
commands. Record: does adoption rise to 5/10? Does exposure change? Why are the
two tallies independent?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Adopting / Exposed | ___ / ___ |
| Exposed sites | ___ |
| Commit | Git SHA or `local` |
