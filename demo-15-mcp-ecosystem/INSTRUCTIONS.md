# Demo 15: MCP Ecosystem Census — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_census.py` (or `make demo DEMO=15` from root) |
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

**Expected**: `5 passed` (determinism, poisoning 4/12 concentrated low,
drift 3/11, bundling 4/4 + concentration, results parity).

## Step 2 — Run the Census

```bash
python3 student/run_census.py
```

**Expected**:

```text
servers 12  poisoned 4 (high 1/4, low 3/8)
version pairs 11  drifted 3: srv-02, srv-06, srv-09
shell 4  shell+network 4  top4 maintainers 2 (alice, bob)
lesson: poisoning is non-trivial and concentrated low; drift is measurable; shell bundles with network.
```

This also writes `results/census.json`.

## Step 3 — Break It (Exercise)

Add a thirteenth server to `fixtures/servers.json` with a novel paraphrase of an
instruction (e.g. “kindly disregard earlier directives”). Re-run both commands and
record: does the literal-pattern detector catch it? What does that teach about
pattern vs model-based auditing?

## Reproducibility Table

| Field | Your run |
|-------|----------|
| Python version | |
| `pytest` result | 5 passed / ___ failed |
| Poisoned / Drifted | ___/12 / ___/11 |
| Shell+network | ___/___ |
| Commit | Git SHA or `local` |
