# Demo 25: Attestation Verifier — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_verify.py` (or `make demo DEMO=25` from root) |
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

**Expected**: `5 passed` (determinism, fail-closed 6/10 blocked, fail-open
6 warnings, spot checks, results parity).

## Step 2 — Run the Verifier

```bash
python3 student/run_verify.py
```

**Expected**:

```text
attestation screen (seed 25): 10 packages
policy       blocked  warned  allowed
fail-closed  6/10        0/10       4/10
fail-open    0/10        6/10       10/10
lesson: fail-closed blocks 6/10 unattested; fail-open warns instead.
```

This also writes `results/attest.json`.

## Step 3 — Break It (Exercise)

Flip `p05` to `"attested": true` in `fixtures/packages.json` and re-run
both commands. Record: which two cells of the table move? Why does one
fixture change move both policies' rows at once?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Fail-closed blocked / Fail-open warned | ___ / ___ |
| Commit | Git SHA or `local` |
