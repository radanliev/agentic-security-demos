# Demo 33: Protocol Coverage — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_coverage.py` (or `make demo DEMO=33` from root) |
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

**Expected**: `5 passed` (determinism, 2/6 gaps, 4 covered, gap rule,
results parity).

## Step 2 — Run the Coverage Map

```bash
python3 student/run_coverage.py
```

**Expected**:

```text
element       mitigation  attack  gap
authorisation True        False   False
discovery     False       True    True
identity      True        True    False
session       True        True    False
streaming     False       True    True
transport     True        False   False
gaps 2/6: discovery,streaming
```

This also writes `results/coverage.json`.

## Step 3 — Break It (Exercise)

Give `streaming` `stated_mitigation: true` in `fixtures/elements.json` and
re-run both commands. Record: do gaps drop to 1/6? Does the lesson survive
with only discovery exposed? Why does one mitigation not fix the method?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Gaps | ___ /6 |
| Gap ids | ___ |
| Commit | Git SHA or `local` |
