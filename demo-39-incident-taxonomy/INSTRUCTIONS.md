# Demo 39: Incident Taxonomy — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_tax.py` (or `make demo DEMO=39` from root) |
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

**Expected**: `5 passed` (determinism, top pattern prompt-injection 4/10,
7/10 supported controls, results parity, stdlib-only).

## Step 2 — Run the Tally

```bash
python3 student/run_tax.py
```

**Expected**:

```text
incidents 10  controls 10
pattern               count
data-exfiltration     2/10
privilege-escalation  1/10
prompt-injection      4/10
tool-misuse           3/10
top pattern: prompt-injection (4/10)
supported controls: 7/10.
```

This also writes `results/taxonomy.json`.

## Step 3 — Break It (Exercise)

Change `inc10`'s pattern to `tool-misuse` in `fixtures/incidents.json` and
re-run both commands. Record: is there now a tie for the top pattern? How
should practitioner guidance handle a tie — and why do counts alone not
settle it?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Top pattern | ___ |
| Supported controls | ___ |
| Commit | Git SHA or `local` |
