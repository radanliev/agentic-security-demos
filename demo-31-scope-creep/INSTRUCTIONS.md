# Demo 31: Integration Scope Creep — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_scopes.py` (or `make demo DEMO=31` from root) |
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

**Expected**: `5 passed` (determinism, 5/8 over-privileged, least-privilege
union, strict-superset rule, results parity).

## Step 2 — Run the Scope Check

```bash
python3 student/run_scopes.py
```

**Expected**:

```text
id   over  requested>used
i1   True   3>1
i2   False  1>1
i3   False  2>2
i4   True   3>1
i5   True   2>1
i6   True   2>1
i7   False  1>1
i8   True   3>2
over-privileged 5/8  least-privilege 8 scopes
least: calendar.read,chat,drive.read,drive.write,files.read,read,repo,write
```

This also writes `results/scopes.json`.

## Step 3 — Break It (Exercise)

Add `admin` to the `used` list of `i1` in `fixtures/integrations.json` and
re-run both commands. Record: is `i1` still over-privileged? What happens to
the least-privilege union? Why does using more not fix the creep?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Over-privileged | ___ /8 |
| Least-privilege scopes | ___ |
| Commit | Git SHA or `local` |
