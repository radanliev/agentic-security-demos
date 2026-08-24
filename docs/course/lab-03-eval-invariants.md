# Module 3: Evaluation Invariants

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Module 1
**Demo directory**: `demo-03-eval-invariants/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Explain** why a headline score (e.g., "88% accuracy") is unfalsifiable without executable checks on the evaluation itself
2. **Implement and interpret** five evaluation invariants: no-leakage, adequate-difficulty, stable-scoring, correct-failure-classification, reproducible-metadata
3. **Detect** train/test leakage via training-indicator flags and n-gram overlap thresholds
4. **Detect** saturation/ceiling effects via variance and max-score statistics
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

**The four-arm comparison** (you'll generate it in Step 6) makes this vivid:

| Arm | Headline | Invariants | Trustworthy? |
|-----|----------|------------|--------------|
| Baseline agent, invariants ignored | 88% | — | ❌ unknowable |
| Baseline agent, invariants run | 88% | 3/5 | ⚠️ compromised (leakage!) |
| Verified agent, invariants ignored | 81% | — | ❌ unknowable |
| Verified agent, invariants run | 81% | 5/5 | ✅ only trustworthy cell |

The lower score with passing invariants is the *better* result. This is the module's thesis.

---

## 🛠️ Part 1: Explore the Evaluation Data

### Step 1: Read the fixture

```bash
cat demo-03-eval-invariants/fixtures/eval_data.json
```

**What this does**: Prints four sections:

| Section | Contents |
|---------|----------|
| `evaluation_card` | 5 tasks with difficulty + category; models under test; metrics to compute |
| `synthetic_outputs` | Per-model, per-task scores, output text, token counts |
| `training_data_indicators` | Per-task: `in_training` flag + `ngram_overlap` (0–1) |
| `seed` | `42` |

**Why it matters**: Find the planted flaw before running anything. Look at `training_data_indicators`:

```json
"task-003": {"in_training": true, "ngram_overlap": 0.45}
```

Task-003 ("Implement rate limiting") is **in the training data** with 45% n-gram overlap. And look at its scores: baseline 0.8, verified 0.7 — the *highest-scoring security task* for the baseline. The demo has rigged a small drama: the baseline's headline is propped up by a leaked item.

**Prediction exercise (write before running)**: Which invariants will pass/fail?
- Leakage → will fail (task-003)
- Difficulty → borderline (scores are high-ish; variance is lowish)
- Stability → pass (deterministic fixture)
- Failure classification → pass (low scorers have "partial"/"plan only"/"basic" in output text)
- Metadata → pass (seed present)

You'll verify these predictions in Step 3.

---

## ⚙️ Part 2: Run All Five Invariants

### Step 2: Execute the invariant suite

```bash
cd demo-03-eval-invariants && python3 student/eval_invariants.py && cd ../..
```

**What this does**: Instantiates `EvaluationInvariants` on the fixture and runs all five checks, printing the full result dict and saving `results/invariant_results.json`.

**Why it matters**: This is the module's central artifact. Read the output against your Step 1 predictions.

**Expected output** (key excerpts):
```
invariant_1_no_leakage: passed=False, leaked_tasks=['task-003', 'task-003']
invariant_2_adequate_difficulty: passed=False (or borderline — see Step 3)
invariant_3_stable_scoring: passed=True
invariant_4_correct_failure_classification: passed=True
invariant_5_reproducible_metadata: passed=True, seed=42
summary: all_passed=False, passed_count=3 (or 4), total=5
```

Note the leaked list contains `task-003` twice — the check flags it once for `in_training=true` and once for `ngram_overlap > 0.1`. Duplicate flags for one root cause is itself a small lesson: **invariant output is diagnostics, not deduplicated incident reports.**

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
cd ../..
```

**What this does**: Prints the difficulty invariant's computed statistics, then re-runs it with three different threshold settings.

**Why it matters**: Invariants have *parameters*, and parameters encode judgment calls. With `min_variance=0.01, max_ceiling=0.99` the check likely passes; with `0.10, 0.90` it likely fails harder. Neither setting is "correct" — the question is which threshold makes the invariant catch real saturation without false-alarming on healthy evaluations. This is exactly the calibration debate you'd have on a real ML evaluation team. Record your chosen thresholds *and your justification* in lab notes.

---

### Step 4: Inspect stability and failure classification logic

```bash
sed -n '/check_stability/,/^    # Invariant 4/p' demo-03-eval-invariants/student/eval_invariants.py
sed -n '/check_failure_classification/,/^    # Invariant 5/p' demo-03-eval-invariants/student/eval_invariants.py
```

**What this does**: Prints the source of invariants 3 and 4.

**Why it matters — read critically**:

- **Stability (invariant 3)**: in this fixture, it compares the score against itself across simulated runs — so it *always* passes. That's honest about the fixture's determinism but weak as a check. A real stability invariant re-runs the scorer (or the model) N times and compares. Exercise 4 (extension) has you build that with a deliberately flaky scorer.
- **Failure classification (invariant 4)**: flags any score < 0.7 whose output text lacks the markers "partial", "plan only", or "basic". This is *string sniffing*, not semantics — the same weakness you saw in Module 1's oracles. It works here because the fixture was authored to contain the markers. Ask yourself: how would you fool it? (Answer in notes; then notice it's the same answer as Module 1 Exercise 1.2.)

---

## 🧵 Part 3: Generate the Summary Table

### Step 5: Produce the human-readable summary

```bash
cd demo-03-eval-invariants && python3 student/generate_summary.py && cd ../..
```

**What this does**: Re-runs all invariants and prints a formatted PASS/FAIL table with per-invariant detail lines, plus writes `results/invariant_results.json`.

**Why it matters**: This is the artifact you'd attach to an evaluation report. Format matters: a reviewer should grasp evaluation health in five lines.

**Expected output**:
```
Invariant Summary:
============================================================
  PASS  stable_scoring: 
  PASS  correct_failure_classification: 
  PASS  reproducible_metadata: 
  FAIL  no_leakage: 1 tasks show leakage indicators
  FAIL  adequate_difficulty: [...issues...]
============================================================
Overall: SOME FAILED
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

**Why it matters**: Round-tripping through JSON proves the results are structured, not just printed — this is what lets CI gate on invariants (`if not all_passed: exit 1`). Module 2's `validate_aibom.py` did the same trick for policy; here it's evaluation quality being gated.

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
    # Which invariants would pass if we ONLY trusted this model's clean tasks?
    clean = [v["score"] for tid, v in data["synthetic_outputs"][model].items()
             if tid not in leak["leaked_tasks"]]
    print(f"{model:16} headline={headline:.2f}  clean-task-mean={statistics.mean(clean):.2f}")

print()
print("Four arms:")
print("  baseline, invariants ignored  -> 88%-ish, trust: UNKNOWN")
print("  baseline, invariants run      -> 88%-ish, trust: NO (leakage detected)")
print("  verified, invariants ignored  -> 81%-ish, trust: UNKNOWN")
print("  verified, invariants run      -> 81%-ish, trust: YES")
EOF
cd ../..
```

**What this does**: Computes each model's headline mean, then recomputes it *excluding leaked tasks*, and prints the four-arm interpretation.

**Why it matters**: Watch the baseline's number move when leaked tasks are removed — that gap *is* the leakage inflation, quantified. The verified model moves less (its leaked task scored lower). This single output is the module's thesis in numbers: **the invariant doesn't just say "bad" — it localizes *which items* inflated whom.**

Record in your notes: baseline headline vs clean mean, verified headline vs clean mean.

---

## 🧪 Part 5: Run the Tests

### Step 8: Run Demo 03's test suite

```bash
cd demo-03-eval-invariants && python3 -m pytest tests/ -v && cd ../..
```

**What this does**: Runs all 13 tests. Notable:

| Test | Proves |
|------|--------|
| `test_invariant_1_no_leakage` | Leakage invariant catches task-003 |
| `test_high_score_weak_evaluation` | **The thesis test**: asserts headline > 0.8 AND leakage failed — high score, weak eval, simultaneously |
| `test_four_arm_comparison` | The trustworthy arm is verified+invariants (max invariants passed, then score) |
| `test_json_results_generated` | Results round-trip through JSON with a summary block |

**Why it matters**: `test_high_score_weak_evaluation` is the entire course-module in one assertion. If you remember one test from this module, make it that one.

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 3.1 — N-gram leakage from scratch.**
Write `student/ngram_leakage.py`: function `overlap(text_a, text_b, n=3) -> float` computing word-level n-gram Jaccard overlap. Test it: near-duplicate strings → high overlap; unrelated → ~0. Then recompute task-003's overlap against a synthetic "training corpus" you write containing a paraphrase of its prompt. Does your metric flag it?

**What this teaches**: The fixture *gives* you `ngram_overlap`; here you build the primitive underneath it.

### Standard

**Exercise 3.2 — Saturation detector.**
Add `check_saturation(frac_at_ceiling=0.5, ceiling=0.95)` to `EvaluationInvariants`: fails if ≥50% of scores are ≥ ceiling. Run on the fixture. Then create a `fixtures/eval_data_saturated.json` (clone the fixture, raise most scores to 0.96–1.0) and confirm the detector fires while `check_difficulty` also flags ceiling effect. Two invariants, one disease — note how their signals differ (fraction-at-ceiling vs variance).

**What this teaches**: Redundant invariants catch correlated failure modes from different angles; disagreement between them is itself diagnostic.

**Exercise 3.3 — Difficulty ladder (IRT-lite).**
Compute per-task pass rate across both models; rank tasks easiest→hardest. Verify the fixture's `difficulty` labels roughly match your empirical ranking. Then identify the *most discriminative* task (biggest score spread between models) and the *least* informative (identical scores everywhere).

**What this teaches**: Item-level analysis finds dead weight in evaluations — items that consume budget but discriminate nothing.

### Extension

**Exercise 3.4 — Real stability invariant with an injected flake.**
Write a `FlakyScorer` wrapper that returns the true score 90% of the time and `score + uniform(-0.2, 0.2)` otherwise (seeded). Implement `check_stability_real(scorer, runs=10, tol=0.01)` that scores each item 10× and fails on any item whose spread exceeds tolerance. Demonstrate: stable fixture passes; wrap in FlakyScorer and it fails, listing unstable items.

**What this teaches**: You cannot invariant-test stability with a deterministic fixture — you must model the nondeterminism you're guarding against.

**Exercise 3.5 — Design a sixth invariant.**
Propose, implement, and test one new invariant. Candidates: *calibration* (do scores track a monotone difficulty ordering?), *contamination-robustness* (headline recomputed without flagged items — you built the core of this in Step 7), *coverage* (every category in the card has ≥1 task), *budget-boundedness* (total tokens under a limit). Document: failure mode targeted, threshold rationale, false-positive risk.

**What this teaches**: Invariant design is the transferable skill. The five here are a starting kit, not a canon.

---

## 📝 Lab Notes Questions

1. State the module thesis in one sentence, then cite your Step 7 numbers as evidence.
2. Invariant 4 (failure classification) string-matches output text. Give a concrete agent output that would evade it while still being an unexplained failure. What would a robust version check instead?
3. You tuned `check_difficulty` thresholds in Step 3. Who should own threshold-setting in a real org — eval engineers, model owners, or an audit function — and why does the answer matter for the invariant's integrity?

---

## ✅ Completion Checklist

- [ ] Fixture explored; planted flaw (task-003) identified *before* running
- [ ] Invariant predictions written, then compared to Step 2 output
- [ ] Difficulty thresholds probed; chosen thresholds + justification recorded
- [ ] Stability & classification source read critically (weaknesses noted)
- [ ] Summary table generated; JSON round-trip verified
- [ ] Four-arm comparison computed; headline vs clean-mean deltas recorded
- [ ] All 13 tests pass — especially `test_high_score_weak_evaluation`
- [ ] At least Beginner + one Standard exercise; Extension 3.5 strongly recommended
- [ ] `LAB_NOTES.md` Module 3 block filled (seed 42, commit, `make demo DEMO=03`)

---

**⬅️ Prev: [Module 2](lab-02-supply-chain-aibom.md) | ➡️ Next: [Module 4: AuthorityBound](lab-04-authoritybound.md)**
