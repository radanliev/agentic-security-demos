# Demo 59: Provenance-labelled Foresight — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_delphi.py` (or `make demo DEMO=59` from root) |
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
python3 student/run_delphi.py
```

**Expected** (abridged):

```
Demo 59: Delphi summaries on synthetic panel ratings

  P1  median 6.0  IQR 1.5  consensus=True  briefing abc111
  P2  median 3.0  IQR 3.0  consensus=False  briefing abc111
```

## What to look for

- Both rows carry the same briefing hash, so they can be compared under one brief.
- Consensus here is an IQR rule, not a claim about expert agreement in the sector.
