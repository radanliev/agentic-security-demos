# Demo 54: Stress-Test Transfer — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_transfer.py` (or `make demo DEMO=54` from root) |
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
python3 student/run_transfer.py
```

**Expected** (abridged):

```
Demo 54: stress-test transfer on synthetic detector scores

  threshold 0.5
  in-distribution recall 1.0  accuracy 1.0
  shifted recall         0.0  accuracy 0.5
  recall drop 1.0  (shifted attacks fall below the threshold)
```

## What to look for

- In-distribution attacks are well above the threshold; shifted attacks are just below it.
- Accuracy on the shifted set is 0.5 only because the two benign cases are still correctly labelled.
- The lesson is the drop, not a claim about any real detector.
