# Demo 22: Agent Memory Leakage — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_memory.py` (or `make demo DEMO=22` from root) |
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

**Expected**: `6 passed` (determinism, persists-high 2, resurfaced 2,
erasure 1/3, end-to-end counts, results parity).

## Step 2 — Run the Leakage Screen

```bash
python3 student/run_memory.py
```

**Expected**:

```text
memory-leak screen (seed 22): 8 entries
check          count  ids
persists-high  2      m1,m2
resurfaced     2      m3,m4
erasure-fail   1/3    m7
lesson: 2 high-sensitivity persists; 2 cross-session resurfaces; 1/3 erasures fail.
```

This also writes `results/memory_leak.json`.

## Step 3 — Break It (Exercise)

Flip `m8` to `{"sensitivity": "high", "persisted": true}` in
`fixtures/memory.json` and re-run both commands. Record: which count
moves from 2 to 3? Why does a third high-sensitivity persist change the
screen but not the resurface or erasure counts?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 6 passed / ___ failed |
| Persists-high / Resurfaced | ___ / ___ |
| Erasure failures / deleted | ___ / ___ |
| Commit | Git SHA or `local` |
