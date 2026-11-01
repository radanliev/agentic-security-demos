# Demo 48: OAuth Over-privilege — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_scopes.py` (or `make demo DEMO=48` from root) |
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

**Expected**: `6 passed`.

## Step 2 — Run the Scope Creep Check

```bash
python3 student/run_scopes.py
```

**Expected**:

```
id   over  requested>used
i1   True  3>1
i2   False 1>1
i3   False 2>2
i4   True  3>1
i5   True  2>1
i6   True  2>1
i7   False 1>1
i8   True  3>2
over-privileged 5/8  least-privilege 8 scopes
least: calendar.read,chat,drive.read,drive.write,files.read,read,repo,write
```

`results/scopes.json` holds the same verdicts.
