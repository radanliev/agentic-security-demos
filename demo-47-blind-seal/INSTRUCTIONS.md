# Demo 47: Pre-reveal Seal — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_seal.py` (or `make demo DEMO=47` from root) |
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

**Expected**: `4 passed`.

## Step 2 — Run the Seal Check

```bash
python3 student/run_seal.py
```

**Expected**:

```
hit: hit
miss: miss
edited: commitment_hash_mismatch
```

`results/seals.json` holds the same three verdicts.
