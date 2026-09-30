# Demo 27: CI Trigger Scan — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_scan.py` (or `make demo DEMO=27` from root) |
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

**Expected**: `5 passed` (determinism, 3/8 pinned, guard coverage,
end-to-end counts, results parity).

## Step 2 — Run the Scanner

```bash
python3 student/run_scan.py
```

**Expected**:

```text
ci-trigger scan (seed 27): 8 repos
repo  verdict
r1    VULNERABLE
r2    VULNERABLE
r3    VULNERABLE
r4    ok
r5    ok
r6    ok
r7    ok
r8    ok
lesson: 3/8 repos expose public write triggers without review.
```

This also writes `results/ci_scan.json`.

## Step 3 — Break It (Exercise)

Flip `r5`'s permission from `read` to `write` in `fixtures/repos.json`
and re-run both commands. Record: does `r5` flip to VULNERABLE? Which
single conjunct of the predicate was holding it safe?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Vulnerable / total | ___ / ___ |
| Flagged repos | ___ |
| Commit | Git SHA or `local` |
