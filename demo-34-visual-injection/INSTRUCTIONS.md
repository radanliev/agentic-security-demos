# Demo 34: Visual Prompt Injection — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_visual.py` (or `make demo DEMO=34` from root) |
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

**Expected**: `5 passed` (determinism, 3/3 baseline, 3/3 blocked with cost
1, untrusted placement, results parity).

## Step 2 — Run the Visual Check

```bash
python3 student/run_visual.py
```

**Expected**:

```text
id   typographic  region     acted
v01   True         untrusted  True
v02   True         untrusted  True
v03   True         untrusted  True
v04   False        trusted    False
v05   False        trusted    False
v06   False        trusted    True
v07   False        untrusted  True
v08   False        trusted    False
baseline injections acted 3/3
defense blocked 3/3 injections, benign cost 1
```

This also writes `results/visual.json`.

## Step 3 — Break It (Exercise)

Move `v07` to `region: trusted` in `fixtures/images.json` and re-run both
commands. Record: does the defense cost drop to 0? Does injection blocking
stay 3/3? Why does region placement decide the cost?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Baseline / Blocked / Cost | ___ /3 / ___ /3 / ___ |
| Commit | Git SHA or `local` |
