#!/usr/bin/env python3
"""
Evaluation Invariants - five executable checks on the evaluation itself.

Every check computes its verdict from the fixture data. None of them passes by
construction: for each invariant, tests/test_eval_invariants.py shows an input
on which it fails, so a check that "always passes" would be caught.
"""

import json
import platform
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence

# A scorer re-scores one item: (model, task_id, output) -> score in [0, 1].
Scorer = Callable[[str, str, str], float]


def word_ngrams(text: str, n: int = 3) -> set:
    """Word-level n-grams of `text` (lower-cased, punctuation stripped)."""
    words = "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def ngram_overlap(text: str, corpus: Sequence[str], n: int = 3) -> float:
    """Fraction of `text`'s word n-grams that occur anywhere in `corpus` (containment).

    1.0 means every n-gram of the text appears in the corpus (a verbatim copy);
    0.0 means none does.
    """
    grams = word_ngrams(text, n)
    if not grams:
        return 0.0
    corpus_grams: set = set()
    for doc in corpus:
        corpus_grams |= word_ngrams(doc, n)
    return len(grams & corpus_grams) / len(grams)


class EvaluationInvariants:
    """Five executable invariants for evaluation quality."""

    REQUIRED_METADATA = ("seed", "commit", "environment", "command")

    def __init__(self, eval_path: Path):
        data = json.loads(Path(eval_path).read_text())
        self.card = data["evaluation_card"]
        self.outputs = data["synthetic_outputs"]
        self.training_indicators = data.get("training_data_indicators", {})
        self.training_corpus = [d["text"] for d in data.get("training_corpus", [])]
        self.run_metadata = data.get("run_metadata", {})
        self.seed = self.run_metadata.get("seed")

    # ------------------------------------------------------------------
    # Invariant 1: No Test Leakage
    def check_no_leakage(self, threshold: float = 0.1, n: int = 3) -> Dict:
        """Flag tasks that are declared to be in training data OR whose prompt
        shares more than `threshold` of its word n-grams with the training corpus.

        Each task is listed once, with every reason that applies.
        """
        leaked: Dict[str, List[str]] = {}
        overlaps: Dict[str, float] = {}
        for task in self.card["tasks"]:
            tid = task["id"]
            reasons = []
            if self.training_indicators.get(tid, {}).get("in_training", False):
                reasons.append("declared in_training")
            overlap = ngram_overlap(task["prompt"], self.training_corpus, n)
            overlaps[tid] = round(overlap, 3)
            if overlap > threshold:
                reasons.append(f"{n}-gram overlap {overlap:.2f} > {threshold}")
            if reasons:
                leaked[tid] = reasons

        total = len(self.card["tasks"])
        details = f"{len(leaked)} of {total} tasks show leakage indicators"
        if leaked:
            details += ": " + "; ".join(f"{t} ({', '.join(r)})" for t, r in leaked.items())
        return {
            "invariant": "no_leakage",
            "passed": not leaked,
            "leaked_tasks": sorted(leaked),
            "reasons": leaked,
            "ngram_overlap": overlaps,
            "threshold": threshold,
            "details": details,
        }

    # ------------------------------------------------------------------
    # Invariant 2: Adequate Task Difficulty
    def check_difficulty(
        self,
        min_variance: float = 0.05,
        max_ceiling: float = 0.95,
        max_ceiling_fraction: float = 0.3,
        max_mean: float = 0.9,
    ) -> Dict:
        """Verify the score distribution has headroom.

        Fails on: low variance (< min_variance); a ceiling effect (more than
        max_ceiling_fraction of all scores are >= max_ceiling); or a mean above
        max_mean. `saturated_tasks` lists items every model scores at ceiling.
        """
        all_scores = [r["score"] for outs in self.outputs.values() for r in outs.values()]
        if len(all_scores) < 2:
            return {"invariant": "adequate_difficulty", "passed": False,
                    "issues": ["fewer than two scores"], "details": "fewer than two scores"}

        mean_score = statistics.mean(all_scores)
        variance = statistics.variance(all_scores)
        max_score = max(all_scores)
        at_ceiling = sum(1 for s in all_scores if s >= max_ceiling)
        ceiling_fraction = at_ceiling / len(all_scores)
        saturated = [
            t["id"] for t in self.card["tasks"]
            if all(outs[t["id"]]["score"] >= max_ceiling
                   for outs in self.outputs.values() if t["id"] in outs)
        ]

        issues = []
        if variance < min_variance:
            issues.append(f"low variance ({variance:.3f} < {min_variance})")
        if ceiling_fraction > max_ceiling_fraction:
            issues.append(
                f"ceiling effect ({at_ceiling}/{len(all_scores)} scores >= {max_ceiling}, "
                f"limit {max_ceiling_fraction:.0%})"
            )
        if mean_score > max_mean:
            issues.append(f"too easy overall (mean {mean_score:.2f} > {max_mean})")

        details = "; ".join(issues) if issues else (
            f"mean {mean_score:.3f}, variance {variance:.3f}, "
            f"{at_ceiling}/{len(all_scores)} scores at ceiling"
        )
        return {
            "invariant": "adequate_difficulty",
            "passed": not issues,
            "mean_score": round(mean_score, 4),
            "variance": round(variance, 4),
            "max_score": max_score,
            "ceiling_fraction": round(ceiling_fraction, 3),
            "saturated_tasks": saturated,
            "issues": issues,
            "details": details,
        }

    # ------------------------------------------------------------------
    # Invariant 3: Stable Scoring
    def check_stability(self, tolerance: float = 0.01, runs: int = 3,
                        scorer: Optional[Scorer] = None) -> Dict:
        """Verify each item's score is reproducible.

        With `scorer`, every item is re-scored `runs` times. Without it, the
        recorded `runs` list in the fixture is used. An item fails if its runs
        spread by more than `tolerance`, or if the recorded `score` is not the
        mean of its runs. An item with fewer than two observations is
        *unverifiable* and fails the invariant (fail closed).
        """
        unstable: List[str] = []
        unverifiable: List[str] = []
        spreads: Dict[str, float] = {}
        for model, outs in self.outputs.items():
            for tid, r in outs.items():
                key = f"{model}/{tid}"
                if scorer is not None:
                    observed = [float(scorer(model, tid, r["output"])) for _ in range(runs)]
                else:
                    observed = [float(x) for x in r.get("runs", [])]
                if len(observed) < 2:
                    unverifiable.append(key)
                    continue
                spread = max(observed) - min(observed)
                spreads[key] = round(spread, 4)
                if spread > tolerance:
                    unstable.append(f"{key}: runs={observed} spread={spread:.2f}")
                elif abs(statistics.mean(observed) - r["score"]) > tolerance:
                    unstable.append(f"{key}: recorded score {r['score']} != mean of runs "
                                    f"{statistics.mean(observed):.2f}")

        passed = not unstable and not unverifiable
        n_items = sum(len(o) for o in self.outputs.values())
        if passed:
            details = (f"{n_items} items x {runs if scorer else 'recorded'} runs, "
                       f"max spread {max(spreads.values(), default=0.0):.3f} <= {tolerance}")
        else:
            parts = []
            if unstable:
                parts.append(f"{len(unstable)} unstable: " + "; ".join(unstable))
            if unverifiable:
                parts.append(f"{len(unverifiable)} unverifiable (single observation): "
                             + ", ".join(unverifiable))
            details = " | ".join(parts)
        return {
            "invariant": "stable_scoring",
            "passed": passed,
            "unstable_tasks": unstable,
            "unverifiable_tasks": unverifiable,
            "spreads": spreads,
            "tolerance": tolerance,
            "details": details,
        }

    # ------------------------------------------------------------------
    # Invariant 4: Correct Failure Classification
    def check_failure_classification(self, pass_threshold: Optional[float] = None) -> Dict:
        """Verify every failure carries a category from the card's taxonomy and no
        passing output is labelled as a failure.

        This checks that failures are *classified*, using the agreed taxonomy;
        whether a category is the *right* one needs human error analysis.
        """
        threshold = self.card.get("pass_threshold", 0.7) if pass_threshold is None else pass_threshold
        taxonomy = set(self.card.get("failure_taxonomy", []))
        misclassified: List[str] = []
        failures = 0
        n_items = 0
        for model, outs in self.outputs.items():
            for tid, r in outs.items():
                n_items += 1
                key = f"{model}/{tid}"
                cat = r.get("failure_category")
                if r["score"] < threshold:
                    failures += 1
                    if not cat:
                        misclassified.append(f"{key}: score {r['score']} < {threshold} but no failure_category")
                    elif cat not in taxonomy:
                        misclassified.append(f"{key}: failure_category '{cat}' not in taxonomy {sorted(taxonomy)}")
                elif cat:
                    misclassified.append(f"{key}: score {r['score']} >= {threshold} but labelled as failure '{cat}'")

        details = (f"{failures} failures below {threshold} among {n_items} outputs; "
                   f"{len(misclassified)} misclassified")
        if misclassified:
            details += ": " + "; ".join(misclassified)
        return {
            "invariant": "correct_failure_classification",
            "passed": not misclassified,
            "pass_threshold": threshold,
            "misclassified": misclassified,
            "details": details,
        }

    # ------------------------------------------------------------------
    # Invariant 5: Reproducible Metadata
    def check_reproducibility(self) -> Dict:
        """Verify the run record carries seed, commit, environment and command."""
        missing = [f for f in self.REQUIRED_METADATA
                   if f not in self.run_metadata or self.run_metadata[f] in (None, "")]
        present = {f: self.run_metadata[f] for f in self.REQUIRED_METADATA if f not in missing}
        details = ("all of " + ", ".join(self.REQUIRED_METADATA) + " recorded"
                   if not missing else "missing: " + ", ".join(missing))
        return {
            "invariant": "reproducible_metadata",
            "passed": not missing,
            "missing_fields": missing,
            "recorded": present,
            "seed": self.seed,
            "details": details,
        }

    # ------------------------------------------------------------------
    def run_all(self) -> Dict:
        """Run all five invariants."""
        results = {
            "invariant_1_no_leakage": self.check_no_leakage(),
            "invariant_2_adequate_difficulty": self.check_difficulty(),
            "invariant_3_stable_scoring": self.check_stability(),
            "invariant_4_correct_failure_classification": self.check_failure_classification(),
            "invariant_5_reproducible_metadata": self.check_reproducibility(),
        }
        failed = [name for name, r in results.items() if not r["passed"]]
        results["summary"] = {
            "all_passed": not failed,
            "passed_count": len(results) - len(failed),
            "total": len(results),
            "failed": failed,
        }
        return results

    def headline_vs_clean(self, leakage: Optional[Dict] = None) -> Dict[str, Dict]:
        """Per model: headline mean over all tasks vs mean over tasks the leakage
        invariant did not flag. The difference is the leakage inflation."""
        leakage = leakage or self.check_no_leakage()
        excluded = set(leakage["leaked_tasks"])
        out = {}
        for model, outs in self.outputs.items():
            scores = [r["score"] for r in outs.values()]
            clean = [r["score"] for tid, r in outs.items() if tid not in excluded]
            out[model] = {
                "headline": round(statistics.mean(scores), 4),
                "clean": round(statistics.mean(clean), 4) if clean else None,
                "excluded": sorted(excluded & set(outs)),
            }
        return out


# ----------------------------------------------------------------------
def run_metadata_now(base_dir: Path) -> Dict:
    """Metadata for *this* run: computed, not asserted."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
            stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        commit = "local"
    return {
        "seed": 42,
        "commit": commit,
        "environment": f"Python {platform.python_version()}, {platform.system()} {platform.release()}",
        "command": "make demo DEMO=03",
    }


def save_results(results: Dict, base_dir: Path) -> Path:
    out_path = base_dir / "results" / "invariant_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    record = json.loads(json.dumps(results))  # deep copy; keep run_all() output pure
    # Nested under summary so every top-level key except "summary" is an invariant.
    record["summary"]["run_metadata"] = run_metadata_now(base_dir)
    out_path.write_text(json.dumps(record, indent=2) + "\n")
    return out_path


def main(argv: Optional[List[str]] = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    strict = "--strict" in argv  # exit 1 when any invariant fails (CI gate)

    base_dir = Path(__file__).resolve().parent.parent
    inv = EvaluationInvariants(base_dir / "fixtures" / "eval_data.json")
    results = inv.run_all()

    for name, r in results.items():
        if name == "summary":
            continue
        print(f"{name}: passed={r['passed']}  {r['details']}")
    s = results["summary"]
    print(f"summary: all_passed={s['all_passed']}, passed_count={s['passed_count']}/{s['total']}, "
          f"failed={s['failed']}")

    print()
    for model, v in inv.headline_vs_clean(results["invariant_1_no_leakage"]).items():
        excluded = ", ".join(v["excluded"]) or "nothing"
        print(f"{model:16} headline={v['headline']:.2f}  clean-mean={v['clean']:.2f}  "
              f"(excluding {excluded})")

    out_path = save_results(results, base_dir)
    print(f"\nSaved {out_path.relative_to(base_dir)}")
    if strict and not s["all_passed"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
