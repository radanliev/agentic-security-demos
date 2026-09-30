# Demo 43: Terms Coding — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_terms.py` (or `make demo DEMO=43` from root) |
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

**Expected**: `5 passed` (determinism, disclaim 5/8, monitoring 4/8 with
consent 3/8, results parity, stdlib-only).

## Step 2 — Run the Terms Coding

```bash
python3 student/run_terms.py
```

**Expected**:

```text
platforms 8
clause                   count
disclaims_autonomy       5/8
requires_monitoring      4/8
consent_for_delegation   3/8
```

This also writes `results/terms.json`.

## Step 3 — Break It (Exercise)

Flip `plat6`'s `consent_for_delegation` to `true` in
`fixtures/platforms.json` and re-run both commands. Record: which tally
moves, and which tests fail? What would a fourth clause (e.g. incident
disclosure) add to the accountability gradient?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Disclaim / Monitoring / Consent | ___ / ___ / ___ |
| Commit | Git SHA or `local` |
