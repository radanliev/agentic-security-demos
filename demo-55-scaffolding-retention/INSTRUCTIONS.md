# Demo 55: Scaffolding Retention Power — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_power.py` (or `make demo DEMO=55` from root) |
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
python3 student/run_power.py
```

**Expected** (abridged):

```
Demo 55: analytic power for a two-arm retention contrast (synthetic plan)

  n per arm 40  alpha 0.05  sd 1.0
  power against an immediate difference of 0.4 : 0.4322
  power against a residual difference of 0.15  : 0.1029
```

## What to look for

- The formula is a planning calculation, not an observed effect.
- Holding n fixed, a smaller residual difference has lower power.
- Increasing n raises power against the residual without inventing new data.
