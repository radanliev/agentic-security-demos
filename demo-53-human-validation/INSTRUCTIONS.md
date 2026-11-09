# Demo 53: Human Validation of Agent Outputs — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_validate.py` (or `make demo DEMO=53` from root) |
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
python3 student/run_validate.py
```

**Expected** (abridged):

```
Demo 53: sampled validation of synthetic agent outputs

  items 8  planted 3
  sample a2,a4,a5,a8
  planted-in-sample 3/3  coverage 1.0
  sample error rate 0.75
```

## What to look for

- Three of eight items carry a planted error (a2, a5, a8).
- The declared sample includes all three, so coverage is 1.0 — a lucky sample, not a guarantee.
- The sample error rate is 3/4 = 0.75, which is not the population rate (3/8).
