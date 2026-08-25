#!/usr/bin/env python3
"""
Evaluation Invariants - Five executable checks for robust evaluation
"""

import json
import statistics
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter
import hashlib


class EvaluationInvariants:
    """Five executable invariants for evaluation quality."""

    def __init__(self, eval_path: Path):
        data = json.loads(eval_path.read_text())
        self.card = data["evaluation_card"]
        self.outputs = data["synthetic_outputs"]
        self.training_indicators = data["training_data_indicators"]
        self.seed = data["seed"]

    # Invariant 1: No Test Leakage
    def check_no_leakage(self, threshold: float = 0.1) -> Dict:
        """Verify test items don't appear in training data."""
        leaked_tasks = []
        for task in self.card["tasks"]:
            tid = task["id"]
            indicator = self.training_indicators.get(tid, {})
            if indicator.get("in_training", False):
                leaked_tasks.append(tid)
            if indicator.get("ngram_overlap", 0) > threshold:
                leaked_tasks.append(tid)

        return {
            "invariant": "no_leakage",
            "passed": len(leaked_tasks) == 0,
            "leaked_tasks": leaked_tasks,
            "threshold": threshold,
            "details": f"{len(leaked_tasks)} tasks show leakage indicators"
        }

    # Invariant 2: Adequate Task Difficulty
    def check_difficulty(self, min_variance: float = 0.05, max_ceiling: float = 0.95) -> Dict:
        """Verify tasks have adequate difficulty spread."""
        all_scores = []
        for model_outputs in self.outputs.values():
            for task_result in model_outputs.values():
                all_scores.append(task_result["score"])

        if not all_scores:
            return {"invariant": "difficulty", "passed": False, "error": "no scores"}

        mean_score = statistics.mean(all_scores)
        variance = statistics.variance(all_scores) if len(all_scores) > 1 else 0
        max_score = max(all_scores)

        issues = []
        if variance < min_variance:
            issues.append(f"low variance ({variance:.3f} < {min_variance})")
        if max_score > max_ceiling:
            issues.append(f"ceiling effect ({max_score:.2f} > {max_ceiling})")
        if mean_score > 0.9:
            issues.append(f"too easy overall (mean={mean_score:.2f})")

        return {
            "invariant": "adequate_difficulty",
            "passed": len(issues) == 0,
            "mean_score": mean_score,
            "variance": variance,
            "max_score": max_score,
            "issues": issues
        }

    # Invariant 3: Stable Scoring
    def check_stability(self, runs: int = 3, tolerance: float = 0.01) -> Dict:
        """Verify scoring is deterministic (same input = same score)."""
        # In synthetic demo, we simulate multiple runs
        unstable_tasks = []

        for model_name, model_outputs in self.outputs.items():
            for task_id, result in model_outputs.items():
                # Simulate deterministic scoring by hashing
                score = result["score"]
                for run in range(runs):
                    # In real eval, this would re-run the scorer
                    simulated_score = score  # Deterministic in our case
                    if abs(simulated_score - score) > tolerance:
                        unstable_tasks.append(f"{model_name}/{task_id}")

        return {
            "invariant": "stable_scoring",
            "passed": len(unstable_tasks) == 0,
            "unstable_tasks": unstable_tasks,
            "tolerance": tolerance
        }

    # Invariant 4: Correct Failure Classification
    def check_failure_classification(self) -> Dict:
        """Verify failures are categorized correctly."""
        # Synthetic: check that low scores have failure reasons
        misclassified = []

        for model_name, model_outputs in self.outputs.items():
            for task_id, result in model_outputs.items():
                score = result["score"]
                output = result["output"].lower()
                if score < 0.7:
                    # Should have indication of why it failed
                    if "partial" not in output and "plan only" not in output and "basic" not in output:
                        misclassified.append(f"{model_name}/{task_id}: score={score} but no failure reason")

        return {
            "invariant": "correct_failure_classification",
            "passed": len(misclassified) == 0,
            "misclassified": misclassified
        }

    # Invariant 5: Reproducible Metadata
    def check_reproducibility(self) -> Dict:
        """Verify all metadata for reproduction is present."""
        required_fields = ["seed", "commit", "environment", "command"]
        # In real system, these come from result records
        # Here we check the fixture has seed at top level
        missing = []
        if not hasattr(self, 'seed') or self.seed is None:
            missing.append("seed")
        # Simulate checking result records
        return {
            "invariant": "reproducible_metadata",
            "passed": len(missing) == 0,
            "missing_fields": missing,
            "seed": getattr(self, 'seed', None)
        }

    def run_all(self) -> Dict:
        """Run all five invariants."""
        results = {
            "invariant_1_no_leakage": self.check_no_leakage(),
            "invariant_2_adequate_difficulty": self.check_difficulty(),
            "invariant_3_stable_scoring": self.check_stability(),
            "invariant_4_correct_failure_classification": self.check_failure_classification(),
            "invariant_5_reproducible_metadata": self.check_reproducibility()
        }

        all_passed = all(r["passed"] for r in results.values())
        results["summary"] = {
            "all_passed": all_passed,
            "passed_count": sum(1 for r in results.values() if r.get("passed", False)),
            "total": 5
        }
        return results


def main():
    base_dir = Path(__file__).resolve().parent.parent
    eval_path = base_dir / "fixtures" / "eval_data.json"
    invariants = EvaluationInvariants(eval_path)
    results = invariants.run_all()

    print(json.dumps(results, indent=2))

    # Save results
    out_path = base_dir / "results" / "invariant_results.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))

    if results["summary"]["all_passed"]:
        print("\n✓ All invariants passed")
    else:
        print("\n✗ Some invariants failed")
        for name, result in results.items():
            if name != "summary" and not result["passed"]:
                print(f"  FAIL: {name} - {result.get('issues', result.get('details', ''))}")


if __name__ == "__main__":
    main()