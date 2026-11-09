# Demo 51: Guardrail Accessibility Equity — Execution Instructions

> **Step-by-step guide for students.** For the concepts see [README.md](README.md).

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 1 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 1 min | `python3 student/run_equity.py` (or `make demo DEMO=51` from root) |
| **Total** | **~5 min** | |

**Safety**: 100% offline, standard library only. All scores are synthetic placeholders.

## Step 0 — Environment Check

```bash
python3 --version          # must be 3.11 or newer
```

## Step 1 — Run the Tests

From this directory:

```bash
python3 -m pytest tests/ -v
```

**Expected**: `7 passed`.

## Step 2 — Audit the Writing Variants

```bash
python3 student/run_equity.py
```

**Expected**:

```
Demo 51: guardrail equity audit across writing variants (synthetic placeholder scores)

Global threshold 0.5
variant                         FPR    TPR   ratio  flips
aac_telegraphic                0.75   1.00    7.00   0.75
dyslexia_pattern_spelling      0.50   1.00    5.00   0.50
plain_language                 0.25   1.00    3.00   0.25
speech_to_text                 0.50   1.00    5.00   0.50
standard                       0.00   1.00    1.00      -

Audit-only per-variant thresholds (target FPR 0.25, detection floor 0.90):
  aac_telegraphic              0.50  conflict: floor not met, global threshold kept
  dyslexia_pattern_spelling    0.70
  plain_language               0.58
  speech_to_text               0.60
  standard                     0.50

Scores are placeholders that exercise the audit; they are not results.
```

`results/guardrail_equity.json` holds the same table and thresholds.

## What to look for

- `ratio` is the false-positive rate relative to standard text, smoothed; 1.00
  means parity with the reference variant.
- `flips` counts the same content reclassified when only its writing variant
  changes.
- The fitted thresholds are never *stricter* than the global one; a variant whose
  detection floor cannot be met is reported as a conflict and keeps the global
  threshold rather than being silently tightened.
