# Demo 52: LLM Simulation Validation — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_sim.py` (or `make demo DEMO=52` from root) |
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
python3 student/run_sim.py
```

**Expected** (abridged):

```
Demo 52: verifying toy cohort simulators against held-out and renamed modules

  honest held-out pass MAE     0.0625
  memorizer held-out pass MAE  0.25
  honest rename probe source   same-module (transfers AAA to ZZZ)
  memorizer rename probe       unknown-name (fails to transfer)
```

## What to look for

- The honest predictor uses the same-module row when it exists and the train mean otherwise.
- The memorizer recites train names only, so unseen CCC and renamed ZZZ fail.
- A low training error would not have revealed that failure: the rename probe is the check.
