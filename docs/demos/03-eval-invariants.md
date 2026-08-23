# Demo 03: Evaluation Invariants

## Learning Objectives

- Design evaluations using executable invariants, not just headline scores
- Detect test leakage (train/test contamination)
- Measure task difficulty and saturation
- Verify scoring stability across runs
- Classify failure modes correctly
- Capture reproducible evaluation metadata

## Conceptual Explanation

Headline scores (e.g., "95% accuracy") are misleading without context. **Evaluation invariants** are executable checks that validate the evaluation itself.

### The Five Invariants

| # | Invariant | Protects Against |
|---|-----------|------------------|
| 1 | **No Leakage** | Train/test contamination |
| 2 | **Adequate Difficulty** | Trivially solvable tasks |
| 3 | **Stable Scoring** | Non-deterministic scoring |
| 4 | **Correct Failure Classification** | Mislabeling failure modes |
| 5 | **Reproducible Metadata** | Missing reproduction info |

## Safety Notice

⚠️ **Teaching demonstration only.**
- Synthetic tasks and model outputs
- No external dataset downloads
- No model API calls
- Results are demonstrations, not research claims

## Running the Demo

```bash
make demo DEMO=03
```

### Expected Output

```
Invariant Summary:
============================================================
PASS  no_leakage: 1 tasks show leakage indicators
FAIL  adequate_difficulty: low variance (0.023 < 0.05), ceiling effect (0.95 > 0.95)
PASS  stable_scoring:
PASS  correct_failure_classification:
PASS  reproducible_metadata: seed=42
============================================================
Overall: SOME FAILED
```

## Invariant Details

### 1. No Leakage
Checks if test items appear in training data (n-gram overlap, exact match).

```python
def check_no_leakage(self, threshold=0.1):
    leaked = []
    for task in self.tasks:
        if task.in_training or task.ngram_overlap > threshold:
            leaked.append(task.id)
    return {"passed": len(leaked) == 0, "leaked": leaked}
```

### 2. Adequate Difficulty
Verifies tasks have variance and no ceiling effect.

```python
def check_difficulty(self, min_variance=0.05, max_ceiling=0.95):
    # Checks: variance > threshold, max_score < ceiling, mean < 0.9
```

### 3. Stable Scoring
Same input → same score across runs.

### 4. Correct Failure Classification
Low scores must have failure reasons in output.

### 5. Reproducible Metadata
Seed, commit, environment, command all recorded.

## Four-Arm Comparison

| Arm | Headline Score | Invariants Passed | Trustworthy? |
|-----|----------------|-------------------|--------------|
| Baseline, no invariants | 88% | 0/5 | ❌ |
| Baseline, with invariants | 88% | 3/5 | ⚠️ |
| Verified, no invariants | 81% | 0/5 | ❌ |
| **Verified, with invariants** | **81%** | **5/5** | ✅ |

**Key insight**: High score + failed invariants = weak evaluation

## Exercises

### Beginner
1. **Leakage metric** — Implement n-gram comparison between train/test

### Standard
2. **Saturation detection** — Detect ceiling effects automatically
3. **Item response** — Basic difficulty analysis (IRT-lite)

### Extension
4. **Custom invariant** — Design a 6th invariant (e.g., calibration)
5. **Four-arm extension** — Add more arms (different models, prompts)

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/eval_data.json` | Synthetic tasks, outputs, training indicators |
| `student/eval_invariants.py` | Five invariant implementations |
| `student/generate_summary.py` | Summary table generator |
| `tests/test_eval_invariants.py` | 13 tests covering all invariants |

## Key Insight

> **A high headline score with failed invariants = a weak evaluation**

This is the core teaching point: invariants expose evaluation weaknesses that headline scores hide.

---

*Next: [Demo 04: Authority Bound](../demos/04-authoritybound.md)*