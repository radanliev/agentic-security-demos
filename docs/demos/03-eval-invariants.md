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

`make demo DEMO=03` runs `student/eval_invariants.py` (one line per invariant, then each model's headline with the leaked task excluded) and then `student/generate_summary.py`:

```
invariant_1_no_leakage: passed=False  1 of 5 tasks show leakage indicators: task-003 (declared in_training, 3-gram overlap 1.00 > 0.1)
invariant_2_adequate_difficulty: passed=False  low variance (0.032 < 0.05); ceiling effect (4/10 scores >= 0.95, limit 30%)
invariant_3_stable_scoring: passed=True  10 items x recorded runs, max spread 0.000 <= 0.01
invariant_4_correct_failure_classification: passed=True  2 failures below 0.7 among 10 outputs; 0 misclassified
invariant_5_reproducible_metadata: passed=True  all of seed, commit, environment, command recorded
summary: all_passed=False, passed_count=3/5, failed=['invariant_1_no_leakage', 'invariant_2_adequate_difficulty']

baseline-agent   headline=0.88  clean-mean=0.85  (excluding task-003)
verified-agent   headline=0.81  clean-mean=0.84  (excluding task-003)

Saved results/invariant_results.json

Generating summary table...
Invariant Summary:
============================================================
  FAIL  no_leakage: 1 of 5 tasks show leakage indicators: task-003 (declared in_training, 3-gram overlap 1.00 > 0.1)
  FAIL  adequate_difficulty: low variance (0.032 < 0.05); ceiling effect (4/10 scores >= 0.95, limit 30%)
  PASS  stable_scoring: 10 items x recorded runs, max spread 0.000 <= 0.01
  PASS  correct_failure_classification: 2 failures below 0.7 among 10 outputs; 0 misclassified
  PASS  reproducible_metadata: all of seed, commit, environment, command recorded
============================================================
Overall: SOME FAILED (3/5 passed)

Headline vs clean-task mean (leaked tasks excluded):
  baseline-agent   0.88 -> 0.85  (-0.03)
  verified-agent   0.81 -> 0.84  (+0.03)
```

`python3 student/eval_invariants.py --strict` exits 1 when any invariant fails — the CI gate.

## Invariant Details

### 1. No Leakage
Computes the word 3-gram containment of each task prompt in the fixture's `training_corpus` and also reads the dataset's declared `in_training` flag. Each task is listed once, with every reason that applies (from `student/eval_invariants.py`, trimmed):

```python
def check_no_leakage(self, threshold: float = 0.1, n: int = 3) -> Dict:
    leaked: Dict[str, List[str]] = {}
    for task in self.card["tasks"]:
        tid = task["id"]
        reasons = []
        if self.training_indicators.get(tid, {}).get("in_training", False):
            reasons.append("declared in_training")
        overlap = ngram_overlap(task["prompt"], self.training_corpus, n)
        if overlap > threshold:
            reasons.append(f"{n}-gram overlap {overlap:.2f} > {threshold}")
        if reasons:
            leaked[tid] = reasons
    ...
    return {"invariant": "no_leakage", "passed": not leaked,
            "leaked_tasks": sorted(leaked), "reasons": leaked, ...}
```

On the fixture, task-003's prompt is planted verbatim in `corpus-001` (overlap 1.00) and is also declared in training: one task, two independent signals.

### 2. Adequate Difficulty
Verifies the score distribution has headroom.

```python
def check_difficulty(self, min_variance=0.05, max_ceiling=0.95,
                     max_ceiling_fraction=0.3, max_mean=0.9):
    # Fails on: sample variance < min_variance; more than max_ceiling_fraction
    # of all scores >= max_ceiling; mean > max_mean.
    # saturated_tasks lists items every model scores at ceiling (task-001 here).
```

### 3. Stable Scoring
Spread (max minus min) of each item's recorded scoring `runs` must be within `tolerance` (0.01), and the recorded `score` must be the mean of its runs. An item with fewer than two observations is unverifiable and fails the invariant. Pass a `scorer` callable to re-score every item `runs` times instead of reading the fixture.

### 4. Correct Failure Classification
Every output below the card's `pass_threshold` (0.7) must carry a `failure_category` from the card's `failure_taxonomy`; a passing output must not carry one. This checks that failures are classified with the agreed vocabulary, not that the category is the right one.

### 5. Reproducible Metadata
`seed`, `commit`, `environment`, `command` must all be present and non-empty in `run_metadata`; a gap is reported as `missing: seed` rather than raised.

## Four-Arm Comparison

Invariants are properties of the evaluation (its items, its scorer, its records), not of a model, so a failed invariant taints every model's headline on that evaluation. What the demo computes (`headline_vs_clean()`):

| Arm | Headline Score | Invariants run? | What the number means |
|-----|----------------|-----------------|-----------------------|
| Baseline, invariants ignored | 0.88 | no | unqualified |
| Baseline, invariants run | 0.88 → **0.85** on clean items | 3/5 pass; leakage localized to `task-003` | inflated: the leaked item is a perfect 1.0 for the baseline |
| Verified, invariants ignored | 0.81 | no | unqualified |
| Verified, invariants run | 0.81 → **0.84** on clean items | 3/5 pass | not inflated: it scored *below* its average on the leaked item |

The 0.07 headline gap between the agents shrinks to 0.01 once the leaked task is excluded.

**Key insight**: High score + failed invariants = weak evaluation — and the invariant localizes which item inflated whom

## Exercises

### Beginner
1. **Leakage metric** — Extend the demo's `ngram_overlap` (containment) to Jaccard similarity and compare them on the fixture; on a 9-gram prompt one shared trigram is already 0.11 > 0.10

### Standard
2. **Saturation detection** — Detect ceiling effects per task, using `saturated_tasks`
3. **Item response** — Basic difficulty analysis (IRT-lite)

### Extension
4. **Custom invariant** — Design a 6th invariant (e.g., calibration)
5. **Four-arm extension** — Add more arms (different models, prompts)

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/eval_data.json` | Synthetic tasks, outputs (with recorded `runs` and `failure_category`), training indicators, `training_corpus`, `run_metadata` |
| `student/eval_invariants.py` | Five invariant implementations plus `headline_vs_clean()` |
| `student/generate_summary.py` | Summary table generator |
| `tests/test_eval_invariants.py` | 25 tests: every invariant passes on the fixture and fails on a mutated copy |

## Key Insight

> **A high headline score with failed invariants = a weak evaluation**

This is the core teaching point: invariants expose evaluation weaknesses that headline scores hide.

---

*Next: [Demo 04: Authority Bound](../demos/04-authoritybound.md)*