# Demo 29: Provenance Graphs — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_prov.py` (or `make demo DEMO=29` from root) |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~10 min** | |

**Safety**: 100% offline, standard library only. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

```bash
python3 --version          # must be 3.11 or newer
```

**Expected**: `Python 3.11.x` (or higher).

## Step 1 — Run the Tests

From this directory:

```bash
python3 -m pytest tests/ -v
```

**Expected**: `6 passed` (determinism, attributable 5/6, unattributable a5,
chain verifies, tamper detected, results parity).

## Step 2 — Run the Reconstruction

```bash
python3 student/run_prov.py
```

**Expected**:

```text
id   cause  attributable
a1   -      yes
a2   a1     yes
a3   a2     yes
a4   a3     yes
a5   -      no
a6   a4     yes
attributable 5/6  unattributable a5
chain verified True  tamper-detected True
```

This also writes `results/provenance.json`.

## Step 3 — Break It (Exercise)

Change the `authority` of `a3` in `fixtures/actions.json` from `tool` to
`operator` and re-run both commands. Record: does attribution change? Does
the chain still verify against the old hashes? Why does editing a record
break verification even though attribution is unchanged?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 6 passed / ___ failed |
| Attributable | ___ /6 |
| Chain verified / Tamper detected | ___ / ___ |
| Commit | Git SHA or `local` |
