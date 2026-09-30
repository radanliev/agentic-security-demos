# Demo 41: Ten Invariants — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_inv.py` (or `make demo DEMO=41` from root) |
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

**Expected**: `5 passed` (determinism, 7 hold / 3 violated, violated names
pinned, results parity, stdlib-only).

## Step 2 — Run the Checklist

```bash
python3 student/run_inv.py
```

**Expected**:

```text
invariants 10  holding 7  violated 3
verdict      name
hold         action-gated
hold         artifact-bom
hold         authority-bound
hold         eval-pinned
hold         human-approval
hold         scan-bound
hold         typed-commitments
VIOLATED     memory-gated
VIOLATED     provenance-travels
VIOLATED     reconstructable
```

This also writes `results/invariants.json`.

## Step 3 — Break It (Exercise)

Flip `inv06` (memory-gated) `holds` to `true` in `fixtures/checks.json` and
re-run both commands. Record: which tests fail, and why? What would count as
accepted evidence for reinstating that invariant under the synthesis rule?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Holding / Violated | ___ / ___ |
| Violated names | ___ |
| Commit | Git SHA or `local` |
