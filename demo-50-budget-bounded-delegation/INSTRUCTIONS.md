# Demo 50: Budget-Bounded Delegation — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_budget.py` (or `make demo DEMO=50` from root) |
| **Total** | **~5 min** | |

**Safety**: 100% offline, standard library only. All plans are synthetic JSON.

## Step 0 — Environment Check

```bash
python3 --version          # must be 3.11 or newer
```

## Step 1 — Run the Tests

From this directory:

```bash
python3 -m pytest tests/ -v
```

**Expected**: `5 passed`.

## Step 2 — Replay the Delegation Plans

```bash
python3 student/run_budget.py
```

**Expected**:

```
Demo 50: budget-attenuated delegation (synthetic fixtures)

  B1  a node's own spend plus what it has delegated never exceeds its grant
  B2  delegation depth never exceeds the configured maximum
  B3  no node delegates to more children than the configured fan-out cap
  B4  every child's grant was within its parent's remaining budget when it was made
  B5  total spend across the tree never exceeds the root budget

within_budget: requested spend 9000, spent 9000 of root budget 10000, denials 0, invariants all hold
fanout_beyond_cap: requested spend 4500, spent 2700 of root budget 10000, denials 4, invariants all hold
    denied delegate reviewer_4 (1000): fan-out cap
    denied delegate reviewer_5 (1000): fan-out cap
    denied spend reviewer_4 (900): unknown node
    denied spend reviewer_5 (900): unknown node
chain_beyond_depth: requested spend 6500, spent 5000 of root budget 10000, denials 2, invariants all hold
    denied delegate agent_c (2000): depth cap
    denied spend agent_c (1500): unknown node
overspend_request: requested spend 4800, spent 4000 of root budget 5000, denials 2, invariants all hold
    denied spend reviewer_1 (800): exceeds remaining budget
    denied delegate reviewer_2 (4000): exceeds parent's remaining budget

Fixtures are placeholders that exercise the ledger; they are not results.
```

`results/delegation_budget.json` holds the same decisions.

## What to look for

- In every plan the ledger's own audit holds: a denial is the mechanism working,
  not a violation.
- `fanout_beyond_cap` and `chain_beyond_depth` are stopped by structure; the
  follow-on "unknown node" denials are the denied children trying to spend.
- `overspend_request` asks for more than the parent still holds and is refused
  rather than truncated (partial grants are opt-in).
