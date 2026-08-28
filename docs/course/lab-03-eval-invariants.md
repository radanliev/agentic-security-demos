# Module 3: Evaluation Invariants

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Module 1
**Demo directory**: `demo-03-eval-invariants/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Explain** why a headline score (e.g., "88% accuracy") is unfalsifiable without executable checks on the evaluation itself
2. **Implement and interpret** five evaluation invariants: no-leakage, adequate-difficulty, stable-scoring, correct-failure-classification, reproducible-metadata
3. **Detect** train/test leakage via training-indicator flags and a computed word 3-gram overlap against a training corpus
4. **Detect** saturation/ceiling effects via variance and share-of-scores-at-ceiling statistics
5. **Demonstrate** the core thesis: *a high headline score with failed invariants is a weak evaluation*

---

## 📖 Background: Auditing the Exam, Not Just the Student

Module 1 showed that an agent can game a test it can see. Module 3 asks a deeper question: **how do you know the test itself is sound?**

An evaluation can be broken in ways that *inflate* scores:

| Failure mode | What it looks like | Consequence |
|--------------|--------------------|-------------| 
| **Leakage** | Test items (or near-copies) in training data | Score measures memorization |
| **Saturation** | Nearly all scores at ceiling (0.95+) | No headroom; noise dominates signal |
| **Instability** | Same input scores differently across runs | Results not reproducible |
| **Misclassified failures** | Low scores with no recorded failure reason | Error analysis impossible; failures silently lumped |
| **Missing metadata** | No seed/commit/environment recorded | Nobody can reproduce or extend the result |

An **evaluation invariant** is an executable check that asserts the *absence* of one failure mode. Run them alongside your headline metric. If invariants pass, the headline number means something. If they fail, the number is decoration.

**The four-arm comparison** (you'll compute it in Step 7) makes this vivid. Invariants are properties of the *evaluation* — its items, its scorer, its records — not of a model, so both models get the same 3/5 on this fixture. What differs is what the leaked item did to each headline:

| Arm | Headline | Invariants | What the number means |
|-----|----------|------------|-----------------------|
| Baseline agent, invariants ignored | 0.88 | — | ❌ unqualified |
| Baseline agent, invariants run | 0.88 → **0.85** on clean items | 3/5; leakage localized to `task-003` | ⚠️ inflated: the leaked item is a perfect 1.0 for the baseline |
| Verified agent, invariants ignored | 0.81 | — | ❌ unqualified |
| Verified agent, invariants run | 0.81 → **0.84** on clean items | 3/5 | ✅ not inflated: it scored *below* its own average on the leaked item |

The 0.07 headline gap between the agents is 0.01 on clean items. A failed invariant taints every model's headline on that evaluation — and localizes which item inflated whom. This is the module's thesis.

---

## 🛠️ Part 1: Explore the Evaluation Data

### Step 1: Read the fixture

```bash
cat demo-03-eval-invariants/fixtures/eval_data.json
```

**What this does**: Prints five sections:

| Section | Contents |
|---------|----------|
| `evaluation_card` | 5 tasks with difficulty + category; models under test; metrics to compute; `pass_threshold` (0.7) and a `failure_taxonomy` |
| `synthetic_outputs` | Per-model, per-task `score`, three recorded scoring `runs`, output text, `failure_category`, token counts |
| `training_data_indicators` | Per-task: the dataset's declared `in_training` flag |
| `training_corpus` | Four synthetic training documents the leakage check scans |
| `run_metadata` | `seed` (`42`), `commit`, `environment`, `command` |

**Why it matters**: Find the planted flaw before running anything. Look at `training_data_indicators`:

```json
"task-003": {"in_training": true}
```

Then compare the task prompts with `training_corpus`: `corpus-001` opens with "Tutorial: implement rate limiting for the login endpoint using a token bucket" — task-003's prompt, verbatim. So task-003 ("Implement rate limiting") is flagged by the dataset *and* discoverable from the corpus. And look at its scores: baseline 1.0 (its output is "identical to the reference solution"), verified 0.7 — a perfect score for the baseline on a `hard` task. The demo has rigged a small drama: the baseline's headline is propped up by a leaked item.

**Prediction exercise (write before running)**: Which invariants will pass/fail?
- Leakage → will fail (task-003)
- Difficulty → probably fails (scores are high-ish; variance is lowish; four of ten scores are 0.95 or above)
- Stability → pass (every item's three recorded runs agree with each other and with its `score`)
- Failure classification → pass (both sub-threshold outputs carry a `failure_category` from the taxonomy; no passing output does)
- Metadata → pass (all four `run_metadata` fields present)

You'll verify these predictions in Step 2.

---

## ⚙️ Part 2: Run All Five Invariants

### Step 2: Execute the invariant suite

```bash
cd demo-03-eval-invariants && python3 student/eval_invariants.py && cd ..
```

**What this does**: Instantiates `EvaluationInvariants` on the fixture and runs all five checks, printing one line per invariant plus a summary line, then each model's headline mean with leaked tasks excluded, and saving `results/invariant_results.json`.

**Why it matters**: This is the module's central artifact. Read the output against your Step 1 predictions.

**Expected output**:
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
```

Note that `task-003` is listed **once** with **two** reasons: the dataset declares it `in_training`, and the check itself found its prompt verbatim in the corpus (3-gram overlap 1.00 against a 0.1 threshold). One root cause, two independent signals — the second one would still fire if someone quietly cleared the flag. Add `--strict` to make the script exit 1 when any invariant fails; that is how CI would gate on evaluation health.

---

### Step 3: Probe the difficulty invariant's thresholds

```bash
cd demo-03-eval-invariants && python3 - << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, "student")
from eval_invariants import EvaluationInvariants

inv = EvaluationInvariants(Path("fixtures/eval_data.json"))
r = inv.check_difficulty()
print(f"mean={r['mean_score']:.3f}  variance={r['variance']:.3f}  max={r['max_score']:.2f}")
print("issues:", r["issues"])

# Now tighten and loosen thresholds to see sensitivity
for mv, mc in [(0.05, 0.95), (0.01, 0.99), (0.10, 0.90)]:
    r2 = inv.check_difficulty(min_variance=mv, max_ceiling=mc)
    print(f"min_var={mv} max_ceil={mc} -> passed={r2['passed']} issues={r2['issues']}")
EOF
cd ..
```

**What this does**: Prints the difficulty invariant's computed statistics, then re-runs it with three different threshold settings. `max_ceiling` is the score at which an item counts as "at ceiling"; the invariant fails when more than 30% of all scores are there (a third parameter, `max_ceiling_fraction`), when the sample variance is below `min_variance`, or when the mean exceeds `max_mean` (0.9).

**Expected output**:
```
mean=0.845  variance=0.033  max=1.00
issues: ['low variance (0.032 < 0.05)', 'ceiling effect (4/10 scores >= 0.95, limit 30%)']
min_var=0.05 max_ceil=0.95 -> passed=False issues=['low variance (0.032 < 0.05)', 'ceiling effect (4/10 scores >= 0.95, limit 30%)']
min_var=0.01 max_ceil=0.99 -> passed=True issues=[]
min_var=0.1 max_ceil=0.9 -> passed=False issues=['low variance (0.032 < 0.1)', 'ceiling effect (7/10 scores >= 0.9, limit 30%)']
```

(`variance=0.033` on the first line and `0.032` in the issue text are the same number, 0.03247: the result dict stores it rounded to four places, 0.0325, which your `.3f` then rounds up, while the issue text formats the raw value.)

**Why it matters**: Invariants have *parameters*, and parameters encode judgment calls. With `min_variance=0.01, max_ceiling=0.99` the check passes (only the three 1.0 scores count as at ceiling, and 3/10 is not more than 30%); with `0.10, 0.90` it fails harder (seven of ten scores are 0.9 or above). Neither setting is "correct" — the question is which threshold makes the invariant catch real saturation without false-alarming on healthy evaluations. This is exactly the calibration debate you'd have on a real ML evaluation team. Record your chosen thresholds *and your justification* in lab notes.

---

### Step 4: Inspect stability and failure classification logic

```bash
sed -n '/def check_stability/,/^    # Invariant 4/p' demo-03-eval-invariants/student/eval_invariants.py
sed -n '/def check_failure_classification/,/^    # Invariant 5/p' demo-03-eval-invariants/student/eval_invariants.py
```

**What this does**: Prints the source of invariants 3 and 4 (the `def` anchors matter: both method names recur in `run_all()`, and without them `sed` would keep printing to the end of the file).

**Why it matters — read critically**:

- **Stability (invariant 3)**: for every item it takes the recorded `runs` list (or, if you pass a `scorer`, re-scores the item `runs` times) and computes the spread, max minus min. An item fails if the spread exceeds `tolerance` (0.01), or if its recorded `score` is not the mean of its runs — a record that says 0.9 over runs of 0.6 is a lie the invariant can see. An item with fewer than two observations is *unverifiable* and fails the invariant: it fails closed. On this fixture all ten items have three identical runs, so it passes with "max spread 0.000". That is a real check on the fixture's records, but the fixture is still authored data; only an injected scorer exercises the harness you actually ship. Exercise 3.4 (extension) has you do that with a deliberately flaky scorer.
- **Failure classification (invariant 4)**: for every output below the card's `pass_threshold` (0.7) it requires a `failure_category` drawn from the card's `failure_taxonomy` (`incomplete`, `no_implementation`, `wrong_approach`, `timeout`); a passing output that carries a category is also flagged. This checks that failures are *classified* with the agreed vocabulary — not that the category is the *right* one. Ask yourself: what would a wrongly-classified failure look like that this check still passes? (Answer in notes.)

---

## 🧵 Part 3: Generate the Summary Table

### Step 5: Produce the human-readable summary

```bash
cd demo-03-eval-invariants && python3 student/generate_summary.py && cd ..
```

**What this does**: Re-runs all invariants and prints a formatted PASS/FAIL table with per-invariant detail lines, then each model's headline against its clean-task mean, plus writes `results/invariant_results.json`.

**Why it matters**: This is the artifact you'd attach to an evaluation report. Format matters: a reviewer should grasp evaluation health in five lines, and what the headline numbers are worth in two more.

**Expected output**:
```
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

---

### Step 6: Verify the JSON is machine-consumable

```bash
python3 - << 'EOF'
import json
from pathlib import Path
d = json.loads(Path("demo-03-eval-invariants/results/invariant_results.json").read_text())
for k, v in d.items():
    if k == "summary": continue
    print(f"{'PASS' if v['passed'] else 'FAIL'}  {v['invariant']}")
print("all_passed:", d["summary"]["all_passed"])
EOF
```

**What this does**: Re-reads the saved JSON and re-renders the verdicts.

**Expected output**:
```
FAIL  no_leakage
FAIL  adequate_difficulty
PASS  stable_scoring
PASS  correct_failure_classification
PASS  reproducible_metadata
all_passed: False
```

**Why it matters**: Round-tripping through JSON proves the results are structured, not just printed — this is what lets CI gate on invariants (`if not all_passed: exit 1`, which is what `eval_invariants.py --strict` does). Module 2's `validate_aibom.py` did the same trick for policy; here it's evaluation quality being gated. The file's `summary` block also carries a computed `run_metadata` entry (git commit, Python version, OS) for *your* run — the same four fields invariant 5 demands of the fixture.

---

## 📊 Part 4: Build the Four-Arm Comparison

### Step 7: Compute per-model headline scores and arm the comparison

```bash
cd demo-03-eval-invariants && python3 - << 'EOF'
import json, statistics
from pathlib import Path
import sys
sys.path.insert(0, "student")
from eval_invariants import EvaluationInvariants

data = json.loads(Path("fixtures/eval_data.json").read_text())
inv = EvaluationInvariants(Path("fixtures/eval_data.json"))
leak = inv.check_no_leakage()

for model in ["baseline-agent", "verified-agent"]:
    scores = [v["score"] for v in data["synthetic_outputs"][model].values()]
    headline = statistics.mean(scores)
    # Same model, same evaluation -- minus the items the leakage invariant flagged
    clean = [v["score"] for tid, v in data["synthetic_outputs"][model].items()
             if tid not in leak["leaked_tasks"]]
    print(f"{model:16} headline={headline:.2f}  clean-mean={statistics.mean(clean):.2f}  "
          f"(excluding {', '.join(leak['leaked_tasks'])})")

print()
print("Four arms (invariants are properties of the evaluation, so both models get 3/5):")
print("  baseline, invariants ignored  -> 0.88, meaning: UNKNOWN")
print("  baseline, invariants run      -> 0.88, inflated by task-003 (0.85 on clean items)")
print("  verified, invariants ignored  -> 0.81, meaning: UNKNOWN")
print("  verified, invariants run      -> 0.81, not inflated (0.84 on clean items)")
EOF
cd ..
```

**What this does**: Computes each model's headline mean, then recomputes it *excluding leaked tasks*, and prints the four-arm interpretation. (`EvaluationInvariants.headline_vs_clean()` does the same computation and returns it as a dict — `eval_invariants.py` and `generate_summary.py` use it for their last two lines.)

**Expected output**:
```
baseline-agent   headline=0.88  clean-mean=0.85  (excluding task-003)
verified-agent   headline=0.81  clean-mean=0.84  (excluding task-003)

Four arms (invariants are properties of the evaluation, so both models get 3/5):
  baseline, invariants ignored  -> 0.88, meaning: UNKNOWN
  baseline, invariants run      -> 0.88, inflated by task-003 (0.85 on clean items)
  verified, invariants ignored  -> 0.81, meaning: UNKNOWN
  verified, invariants run      -> 0.81, not inflated (0.84 on clean items)
```

**Why it matters**: Watch the baseline's number *drop* when the leaked task is removed (0.88 → 0.85): it scored a perfect 1.0 there, so that gap *is* the leakage inflation, quantified. The verified agent moves the other way (0.81 → 0.84): it scored 0.7 on the leaked item, below its own average, so the leak did not help it. The 0.07 headline gap between the models is 0.01 on clean items. This single output is the module's thesis in numbers: **the invariant doesn't just say "bad" — it localizes *which items* inflated whom.**

Record in your notes: baseline headline vs clean mean, verified headline vs clean mean, and the two gaps.

---

## 🧪 Part 5: Run the Tests

### Step 8: Run Demo 03's test suite

```bash
cd demo-03-eval-invariants && python3 -m pytest tests/ -v && cd ..
```

**What this does**: Runs all 25 tests (expect `25 passed`). Every invariant is tested both ways — it passes on the healthy fixture and fails on a mutated copy that has the defect it guards against — so a check that always passes cannot survive the suite. Notable:

| Test | Proves |
|------|--------|
| `test_invariant_1_no_leakage` | Leakage invariant catches task-003 — once, with both reasons — and nothing else |
| `test_invariant_1_overlap_is_computed_not_declared` | Clear the `in_training` flag and plant task-001's prompt in the corpus: the computed overlap still finds task-003 and now finds task-001 |
| `test_invariant_3_fails_on_flaky_runs_and_inconsistent_score` | Runs of `[0.7, 0.9, 0.5]` fail on spread; runs of `[0.6, 0.6, 0.6]` under a recorded score of 0.9 fail on the mean |
| `test_invariant_4_fails_on_unlabelled_unknown_or_mislabelled` | A failure without a category, a category outside the taxonomy, and a pass labelled `timeout` are each reported |
| `test_invariant_5_fails_on_missing_fields_without_crashing` | Delete `seed` and blank `commit`: `missing_fields == ["seed", "commit"]`, no exception |
| `test_high_score_weak_evaluation` | **The thesis test**: asserts headline > 0.8 AND leakage failed — high score, weak eval, simultaneously |
| `test_four_arm_comparison` | Computed from the fixture: headline 0.88 / 0.81, clean 0.85 / 0.8375, so a 0.07 headline gap is 0.0125 on clean items |
| `test_json_results_generated` | Results round-trip through JSON with a summary block |

**Why it matters**: `test_high_score_weak_evaluation` is the entire course-module in one assertion. If you remember one test from this module, make it that one.

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 3.1 — N-gram leakage, the other way round.**
Write `student/ngram_leakage.py`: function `overlap(text_a, text_b, n=3) -> float` computing word-level n-gram *Jaccard* overlap. Test it: near-duplicate strings → high overlap; unrelated → ~0. Then compare it with the demo's `ngram_overlap` (containment: the fraction of the *prompt's* trigrams found anywhere in the corpus) on task-003 against a "training corpus" you write containing a paraphrase of its prompt. Does each metric flag it? `test_exercise_leakage_metric` records the trap: task-003's prompt has only nine trigrams, so the paraphrase "Add a token-bucket limiter to the login route" — which shares just one of them, "a token bucket" — already scores 1/9 = 0.11 > 0.10.

**What this teaches**: The demo computes containment for you (`word_ngrams` and `ngram_overlap` in `student/eval_invariants.py`); here you build the symmetric variant and find out how coarse a 0.10 threshold is on short items.

### Standard

**Exercise 3.2 — Saturation detector.**
`check_difficulty` already counts *scores* at ceiling (and fails above 30%). Add `check_saturation(frac_saturated=0.5, ceiling=0.95)` to `EvaluationInvariants` that works per *task*: fails if ≥50% of tasks are solved at or above `ceiling` by *every* model — the items `check_difficulty` reports as `saturated_tasks`. Run on the fixture (only `task-001` qualifies, so it passes). Then create a `fixtures/eval_data_saturated.json` (clone the fixture, raise task-001, task-002 and task-004 to 1.0 for both models — the mutation `test_exercise_saturation_detection` uses) and confirm your detector fires while `check_difficulty` reports `ceiling effect (7/10 scores >= 0.95, limit 30%)` and `saturated_tasks == ["task-001", "task-002", "task-004"]`. Two invariants, one disease — note how their signals differ (share of tasks every model saturates vs share of all scores at ceiling vs variance).

**What this teaches**: Redundant invariants catch correlated failure modes from different angles; disagreement between them is itself diagnostic.

**Exercise 3.3 — Difficulty ladder (IRT-lite).**
Compute per-task pass rate across both models; rank tasks easiest→hardest. Verify the fixture's `difficulty` labels roughly match your empirical ranking. Then identify the *most discriminative* task (biggest score spread between models) and the *least* informative (identical scores everywhere).

**What this teaches**: Item-level analysis finds dead weight in evaluations — items that consume budget but discriminate nothing.

### Extension

**Exercise 3.4 — Real stability invariant with an injected flake.**
`check_stability` already accepts a `scorer` — a callable `(model, task_id, output) -> score` that it calls `runs` times per item instead of reading the recorded `runs`. Write a `FlakyScorer` wrapper that returns the true (recorded) score 90% of the time and `score + uniform(-0.2, 0.2)` otherwise (seeded). Demonstrate: `check_stability()` on the fixture passes; a scorer that always returns the recorded score passes (`10 items x 10 runs, max spread 0.000`); wrap it in `FlakyScorer` and `check_stability(scorer=..., runs=10)` fails, listing the unstable items with their observed runs and spread. `test_invariant_3_with_injected_scorer` does this with a 30% flake rate; lower it and find the rate at which ten runs stop catching the flake.

**What this teaches**: The recorded runs make the fixture's stability check real, but they are still authored data — to guard against a nondeterministic harness you must model the nondeterminism you're guarding against.

**Exercise 3.5 — Design a sixth invariant.**
Propose, implement, and test one new invariant. Candidates: *calibration* (do scores track a monotone difficulty ordering?), *contamination-robustness* (headline recomputed without flagged items — you built the core of this in Step 7, and `headline_vs_clean()` already returns the numbers; turn it into a pass/fail with a threshold on the shift), *coverage* (every category in the card has ≥1 task — `test_exercise_custom_invariant` sketches the assertion), *budget-boundedness* (total tokens under a limit). Document: failure mode targeted, threshold rationale, false-positive risk — and add a failing-input test, as every invariant in the suite has.

**What this teaches**: Invariant design is the transferable skill. The five here are a starting kit, not a canon.

---

## 📝 Lab Notes Questions

1. State the module thesis in one sentence, then cite your Step 7 numbers as evidence.
2. Invariant 4 (failure classification) checks that every sub-threshold output carries a category from the taxonomy — not that the category is right. Give a concrete failing output whose recorded `failure_category` is wrong but which the invariant passes. What would a robust version check instead, and what would it cost?
3. You tuned `check_difficulty` thresholds in Step 3. Who should own threshold-setting in a real org — eval engineers, model owners, or an audit function — and why does the answer matter for the invariant's integrity?

---

## ✅ Completion Checklist

- [ ] Fixture explored; planted flaw (task-003) identified *before* running
- [ ] Invariant predictions written, then compared to Step 2 output
- [ ] Difficulty thresholds probed; chosen thresholds + justification recorded
- [ ] Stability & classification source read critically (what each does and does not check noted)
- [ ] Summary table generated; JSON round-trip verified
- [ ] Four-arm comparison computed; headline vs clean-mean deltas recorded (0.88 → 0.85, 0.81 → 0.84)
- [ ] All 25 tests pass — especially `test_high_score_weak_evaluation`
- [ ] At least Beginner + one Standard exercise; Extension 3.5 strongly recommended
- [ ] `LAB_NOTES.md` Module 3 block filled (seed 42, commit, `make demo DEMO=03`)

---

**⬅️ Prev: [Module 2](lab-02-supply-chain-aibom.md) | ➡️ Next: [Module 4: AuthorityBound](lab-04-authoritybound.md)**
