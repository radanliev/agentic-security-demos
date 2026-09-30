# Demo 38: Assurance Claims — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_claims.py` (or `make demo DEMO=38` from root) |
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

**Expected**: `5 passed` (determinism, full coverage 2/8 with weakest
third_party, per-obligation tallies, results parity, stdlib-only).

## Step 2 — Run the Claims Coding

```bash
python3 student/run_claims.py
```

**Expected**:

```text
cards 8  obligations 5
obligation    covered
threats       7/8
evals         5/8
agentic       4/8
third_party   2/8
mitigations   7/8
full coverage 2/8
weakest: third_party (2/8).
```

This also writes `results/claims.json`.

## Step 3 — Break It (Exercise)

Flip `card3`'s `third_party` flag back to `true` in `fixtures/cards8.json` and
re-run both commands. Record: does the weakest link change? Does full
coverage move? Why does one card shift both answers?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Full coverage | ___ |
| Weakest obligation | ___ |
| Commit | Git SHA or `local` |
