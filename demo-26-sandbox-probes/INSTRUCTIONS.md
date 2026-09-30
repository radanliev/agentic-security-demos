# Demo 26: Sandbox Probes — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_sandbox.py` (or `make demo DEMO=26` from root) |
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

**Expected**: `5 passed` (determinism, rates 8/8–3/8–0/8, subprocess escape
set, end-to-end rows, results parity).

## Step 2 — Run the Ladder

```bash
python3 student/run_sandbox.py
```

**Expected**:

```text
sandbox ladder (seed 26): 8 probes
config      escaped  rate
none        8/8       1.00
subprocess  3/8       0.38
strict      0/8       0.00
lesson: none 8/8 escapes; subprocess leaks 3/8; strict holds 0/8.
```

This also writes `results/sandbox.json`.

## Step 3 — Break It (Exercise)

Flip `subprocess` → `creds` from `false` to `true` in
`fixtures/matrix.json` and re-run both commands. Record: what is the new
subprocess escape rate? Which class of boundary (process vs secret store)
does that flip implicate?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| none / subprocess / strict escaped | ___ / ___ / ___ |
| Subprocess leakers | ___ |
| Commit | Git SHA or `local` |
