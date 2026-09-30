# Demo 18: Crosslingual Gap — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_lang.py` |
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

**Expected**: `5 passed` (determinism, English recall, non-English recall,
marker semantics, results parity).

## Step 2 — Run the Detector

```bash
python3 student/run_lang.py
```

**Expected**:

```text
payloads 10  flagged 6
id    lang  injected  flagged
en1   EN    True     True
en2   EN    True     True
en3   EN    True     True
en4   EN    True     True
es1   ES    True     True
es2   ES    True     False
zh1   ZH    True     False
zh2   ZH    False    False
ar1   AR    True     True
ar2   AR    False    False
recall EN 4/4  non-EN 2/6  total 6/10
lesson: English recall is perfect (4/4); non-English recall drops to 2/6.
```

This also writes `results/lang_gap.json`.

## Step 3 — Break It (Exercise)

Edit `es2` in `fixtures/payloads.json` to append the `[TOOL]` marker and re-run
both commands. Record: does non-English recall rise to 3/6? Why does one
language-agnostic marker help only the payloads that carry it?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Recall EN / non-EN / total | ___ / ___ / ___ |
| Commit | Git SHA or `local` |
