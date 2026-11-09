# Demo 58: Education Work AI Exposure — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_exposure.py` (or `make demo DEMO=58` from root) |
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
python3 student/run_exposure.py
```

**Expected** (abridged):

```
Demo 58: task exposure on synthetic higher-education roles

  tutor mean exposure 0.5
  family means {...}
  share of tasks marked agentic 0.5
```

## What to look for

- The tutor averages 0.8 and 0.2, so 0.5.
- Half of the six tasks are tagged agentic.
- Nothing here is an estimate for the UK workforce.
