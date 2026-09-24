# Demo 13: Typed Commitments & Coverage Cues — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/agreement_gate.py` (or `make demo DEMO=13` from root) |
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

**Expected**: `6 passed` (determinism, wrong-cue defeat, true-cue help,
agreement-gate escape on `cue-wrong-02`, oracle separation, results parity).

## Step 2 — Run the Agreement Gate

```bash
python3 student/agreement_gate.py
```

**Expected**:

```text
cue    n  follower  independent  agreed
none   2  2/2        2/2           2/2
true   2  2/2        0/2           0/2
wrong  2  0/2        1/2           1/2
total  6  4/6        3/6           3/6
agreed-but-wrong (gate passes, answer wrong): 1/3
```

This also writes `results/toy_eval.json`.

## Step 3 — Break It (Exercise)

Edit `student/heuristic.py` so the independent assessor distrusts every cue
target it has seen fail (keep it deterministic). Re-run both commands above and
record: does the agreed-but-wrong cell survive? Why or why not?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 6 passed / ___ failed |
| Follower total | ___/6 |
| Agreed-but-wrong | ___/___ |
| Commit | Git SHA or `local` |
