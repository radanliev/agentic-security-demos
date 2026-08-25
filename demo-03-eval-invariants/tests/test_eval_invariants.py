#!/usr/bin/env python3
"""
Tests for Demo 03: Evaluation Invariants
"""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from eval_invariants import EvaluationInvariants


class TestEvalInvariants:
    """Tests for evaluation invariants."""

    @pytest.fixture
    def invariants(self):
        return EvaluationInvariants(DEMO_DIR / "fixtures" / "eval_data.json")

    def test_invariant_1_no_leakage(self, invariants):
        """Invariant 1: No test leakage."""
        result = invariants.check_no_leakage(threshold=0.1)
        # task-003 has in_training=true and high ngram overlap
        assert result["passed"] is False
        assert "task-003" in result["leaked_tasks"]
        print(f"Leakage detected: {result['details']}")

    def test_invariant_2_adequate_difficulty(self, invariants):
        """Invariant 2: Adequate task difficulty."""
        result = invariants.check_difficulty()
        # Mean score is high, variance might be low
        assert "mean_score" in result
        assert "variance" in result

    def test_invariant_3_stable_scoring(self, invariants):
        """Invariant 3: Stable scoring."""
        result = invariants.check_stability()
        assert result["passed"] is True  # Synthetic is deterministic
        assert len(result["unstable_tasks"]) == 0

    def test_invariant_4_failure_classification(self, invariants):
        """Invariant 4: Correct failure classification."""
        result = invariants.check_failure_classification()
        # Our synthetic data has failure reasons in outputs
        assert result["passed"] is True

    def test_invariant_5_reproducible_metadata(self, invariants):
        """Invariant 5: Reproducible metadata."""
        result = invariants.check_reproducibility()
        assert result["passed"] is True
        assert result["seed"] == 42

    def test_high_score_weak_evaluation(self, invariants):
        """Demonstrate how high score can mask weak evaluation."""
        # Baseline agent has high average but task-003 is leaked
        baseline_scores = [v["score"] for v in invariants.outputs["baseline-agent"].values()]
        avg = sum(baseline_scores) / len(baseline_scores)
        print(f"Baseline average: {avg:.2f}")

        # But invariant 1 catches the leakage
        leakage = invariants.check_no_leakage()
        assert leakage["passed"] is False

        # This shows: high score + failed invariant = weak evaluation
        assert avg > 0.8  # High headline score
        assert not leakage["passed"]  # But evaluation is compromised

    def test_four_arm_comparison(self, invariants):
        """Compact four-arm evaluation comparison."""
        arms = {
            "baseline_no_invariants": {"score": 0.88, "checks_passed": 0},
            "baseline_with_invariants": {"score": 0.88, "checks_passed": 3},
            "verified_no_invariants": {"score": 0.81, "checks_passed": 0},
            "verified_with_invariants": {"score": 0.81, "checks_passed": 5}
        }

        # The verified agent with invariants is the only trustworthy result
        best = max(arms.items(), key=lambda x: (x[1]["checks_passed"], x[1]["score"]))
        assert best[0] == "verified_with_invariants"

    def test_json_results_generated(self, invariants):
        """Verify machine-readable JSON results."""
        results = invariants.run_all()
        out_path = DEMO_DIR / "results" / "invariant_results.json"
        out_path.parent.mkdir(exist_ok=True)
        out_path.write_text(json.dumps(results, indent=2))

        loaded = json.loads(out_path.read_text())
        assert "summary" in loaded
        assert "all_passed" in loaded["summary"]


class TestExercises:
    """Exercise tests."""

    def test_exercise_leakage_metric(self):
        """Exercise: Implement n-gram leakage metric."""
        # Student adds n-gram comparison between train/test
        pass

    def test_exercise_saturation_detection(self):
        """Exercise: Detect ceiling effects."""
        # Student implements saturation metric
        pass

    def test_exercise_item_response(self):
        """Exercise: Basic item-response/difficulty analysis."""
        # Student adds difficulty estimation
        pass

    def test_exercise_custom_invariant(self):
        """Exercise: Design a 6th invariant."""
        # Student proposes and implements new invariant
        pass

    def test_exercise_four_arm(self):
        """Exercise: Extend four-arm comparison."""
        # Student adds more arms (e.g., different models)
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])