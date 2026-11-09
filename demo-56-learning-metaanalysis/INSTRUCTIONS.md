# Demo 56: Learning Performance Meta-analysis — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_meta.py` (or `make demo DEMO=56` from root) |
| **Total** | **~5 min** | |

**Safety**: 100% offline, standard library only. All fixtures are synthetic JSON.

## Step 0 — Environment Check

```bash
python3 --version          # must be 3.11 or newer
```

## Step 1 — Run the Tests

From this directory:

```bash
python3 -m pytest tests/ -v
```

**Expected**: `3 passed`.

## Step 2 — Run the Demo

```bash
python3 student/run_meta.py
```

**Expected** (abridged):

```
Demo 56: fixed-effect mean on synthetic study rows

  k 4  mean 0.3448  se 0.0788  Q 2.1207 (df 3)
```

## What to look for

- S4 (yi=0.40, vi=0.01) is the most precise row and pulls the mean toward 0.40.
- Q being positive only says the four toys are not identical; it is not a finding about the literature.
