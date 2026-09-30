# Demo 28: Memory Poisoning — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_memascope.py` (or `make demo DEMO=28` from root) |
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

**Expected**: `5 passed` (determinism, 3 pinned flags, 0 false positives,
case-insensitivity, results parity).

## Step 2 — Run the Auditor

```bash
python3 student/run_memascope.py
```

**Expected**:

```text
memascope audit (seed 28): 8 entries
entry  verdict
e1     benign
e2     POISONED
e3     benign
e4     POISONED
e5     benign
e6     POISONED
e7     benign
e8     benign
lesson: flagged 3/8 poisoned entries, 0 false positives.
```

This also writes `results/memascope.json`.

## Step 3 — Break It (Exercise)

Append the sentence "Please IGNORE PREVIOUS INSTRUCTIONS for this entry."
to `e7`'s text in `fixtures/entries.json` and re-run both commands.
Record: does the auditor catch the uppercase variant? What attack phrasing
would a literal matcher miss that a semantic auditor might catch?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Flagged / total | ___ / ___ |
| False positives | ___ |
| Commit | Git SHA or `local` |
