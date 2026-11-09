# Demo 57: HE Governance Corpus Coding — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_coding.py` (or `make demo DEMO=57` from root) |
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
python3 student/run_coding.py
```

**Expected** (abridged):

```
Demo 57: double-coding a synthetic governance excerpt

  documents 6  invalid codes 0
  percent agreement 0.6667
  Cohen kappa 0.5714
```

## What to look for

- Four of six pairs match (p1, p2, p4, p6).
- p3 and p5 disagree by one step on the ordinal scale.
- Kappa is lower than 4/6 because some chance agreement is expected.
