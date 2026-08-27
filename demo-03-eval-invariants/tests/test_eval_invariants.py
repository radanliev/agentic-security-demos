#!/usr/bin/env python3
"""
Tests for Demo 03: Evaluation Invariants

Each invariant is tested both ways: it passes on the healthy input and fails on
an input that has the defect it guards against. A check that always passes
cannot survive this suite.
"""

import copy
import json
import random
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from eval_invariants import EvaluationInvariants, ngram_overlap, word_ngrams  # noqa: E402

FIXTURE = DEMO_DIR / "fixtures" / "eval_data.json"


def variant(tmp_path: Path, mutate) -> EvaluationInvariants:
    """Load the fixture, apply `mutate(data)`, and build invariants on the copy."""
    data = json.loads(FIXTURE.read_text())
    mutate(data)
    path = tmp_path / "eval_variant.json"
    path.write_text(json.dumps(data))
    return EvaluationInvariants(path)


@pytest.fixture
def invariants():
    return EvaluationInvariants(FIXTURE)


class TestNgramOverlap:
    def test_word_ngrams_normalise_case_and_punctuation(self):
        assert word_ngrams("Fix the bug, NOW!", 3) == {"fix the bug", "the bug now"}

    def test_overlap_verbatim_partial_and_none(self):
        corpus = ["a b c d e"]
        assert ngram_overlap("a b c d e", corpus) == 1.0
        assert ngram_overlap("a b c x y", corpus) == pytest.approx(1 / 3)
        assert ngram_overlap("p q r s", corpus) == 0.0
        assert ngram_overlap("ab", corpus) == 0.0  # shorter than n


class TestEvalInvariants:
    def test_invariant_1_no_leakage(self, invariants):
        """Invariant 1: task-003 is flagged once, for both reasons; nothing else is."""
        result = invariants.check_no_leakage(threshold=0.1)
        assert result["passed"] is False
        assert result["leaked_tasks"] == ["task-003"]
        assert result["reasons"]["task-003"] == ["declared in_training", "3-gram overlap 1.00 > 0.1"]
        assert result["ngram_overlap"]["task-003"] == 1.0
        assert all(result["ngram_overlap"][t] == 0.0 for t in ["task-001", "task-002", "task-004", "task-005"])
        assert result["details"].startswith("1 of 5 tasks show leakage indicators")

    def test_invariant_1_overlap_is_computed_not_declared(self, tmp_path):
        """Undeclare task-003 and plant task-001's prompt in the corpus: the
        computed overlap must find task-001 and still find task-003."""
        def mutate(d):
            d["training_data_indicators"]["task-003"]["in_training"] = False
            d["training_corpus"].append({"doc_id": "x", "text": d["evaluation_card"]["tasks"][0]["prompt"]})
        result = variant(tmp_path, mutate).check_no_leakage()
        assert result["leaked_tasks"] == ["task-001", "task-003"]
        assert result["reasons"]["task-003"] == ["3-gram overlap 1.00 > 0.1"]

    def test_invariant_1_passes_on_clean_evaluation(self, tmp_path):
        def mutate(d):
            d["training_data_indicators"]["task-003"]["in_training"] = False
            d["training_corpus"] = [c for c in d["training_corpus"] if c["doc_id"] != "corpus-001"]
        result = variant(tmp_path, mutate).check_no_leakage()
        assert result["passed"] is True
        assert result["leaked_tasks"] == []

    def test_invariant_2_adequate_difficulty(self, invariants):
        """Invariant 2: fails at the defaults for low variance and ceiling effect."""
        result = invariants.check_difficulty()
        assert result["passed"] is False
        assert result["mean_score"] == pytest.approx(0.845)
        assert result["variance"] == pytest.approx(0.0325, abs=1e-4)
        assert result["ceiling_fraction"] == pytest.approx(0.4)
        assert result["saturated_tasks"] == ["task-001"]
        assert [i.split(" (")[0] for i in result["issues"]] == ["low variance", "ceiling effect"]

    def test_invariant_2_thresholds_are_parameters(self, invariants):
        loose = invariants.check_difficulty(min_variance=0.01, max_ceiling=0.99)
        assert loose["passed"] is True
        tight = invariants.check_difficulty(min_variance=0.10, max_ceiling=0.90)
        assert tight["passed"] is False and len(tight["issues"]) == 2

    def test_invariant_2_detects_saturation_and_passes_spread(self, tmp_path):
        def saturate(d):
            for outs in d["synthetic_outputs"].values():
                for r in outs.values():
                    r["score"] = 0.98
        sat = variant(tmp_path, saturate).check_difficulty()
        assert sat["passed"] is False
        assert any(i.startswith("ceiling effect (10/10") for i in sat["issues"])
        assert any(i.startswith("too easy overall") for i in sat["issues"])

        def spread(d):
            scores = iter([0.1, 0.3, 0.5, 0.7, 0.9, 0.2, 0.4, 0.6, 0.8, 0.95])
            for outs in d["synthetic_outputs"].values():
                for r in outs.values():
                    r["score"] = next(scores)
        ok = variant(tmp_path, spread).check_difficulty()
        assert ok["passed"] is True, ok["issues"]

    def test_invariant_3_stable_scoring(self, invariants):
        """Invariant 3: recorded runs agree within tolerance."""
        result = invariants.check_stability()
        assert result["passed"] is True
        assert result["unstable_tasks"] == [] and result["unverifiable_tasks"] == []
        assert len(result["spreads"]) == 10

    def test_invariant_3_fails_on_flaky_runs_and_inconsistent_score(self, tmp_path):
        def flaky(d):
            d["synthetic_outputs"]["verified-agent"]["task-003"]["runs"] = [0.7, 0.9, 0.5]
            d["synthetic_outputs"]["baseline-agent"]["task-002"]["runs"] = [0.6, 0.6, 0.6]  # score says 0.9
        result = variant(tmp_path, flaky).check_stability()
        assert result["passed"] is False
        assert result["unstable_tasks"][0].startswith("baseline-agent/task-002: recorded score 0.9")
        assert result["unstable_tasks"][1].startswith("verified-agent/task-003: runs=[0.7, 0.9, 0.5] spread=0.40")

    def test_invariant_3_fails_closed_without_runs(self, tmp_path):
        def strip_runs(d):
            del d["synthetic_outputs"]["baseline-agent"]["task-001"]["runs"]
        result = variant(tmp_path, strip_runs).check_stability()
        assert result["passed"] is False
        assert result["unverifiable_tasks"] == ["baseline-agent/task-001"]

    def test_invariant_3_with_injected_scorer(self, invariants):
        """A scorer can be injected and re-run; a flaky one is caught."""
        stable = invariants.check_stability(scorer=lambda m, t, o: 0.5, runs=5)
        assert stable["passed"] is False  # constant 0.5 != recorded scores
        assert all("recorded score" in u for u in stable["unstable_tasks"])

        rng = random.Random(42)
        recorded = {(m, t): r["score"] for m, outs in invariants.outputs.items() for t, r in outs.items()}
        def flaky(m, t, o):
            return recorded[(m, t)] + (rng.uniform(-0.2, 0.2) if rng.random() < 0.3 else 0.0)
        result = invariants.check_stability(scorer=flaky, runs=10)
        assert result["passed"] is False
        assert len(result["unstable_tasks"]) > 0

    def test_invariant_4_failure_classification(self, invariants):
        """Invariant 4: both failures carry a taxonomy label; no pass is labelled."""
        result = invariants.check_failure_classification()
        assert result["passed"] is True
        assert result["pass_threshold"] == 0.7
        assert result["details"].startswith("2 failures below 0.7 among 10 outputs; 0 misclassified")

    def test_invariant_4_fails_on_unlabelled_unknown_or_mislabelled(self, tmp_path):
        def mutate(d):
            outs = d["synthetic_outputs"]
            outs["baseline-agent"]["task-005"]["failure_category"] = None       # failure without label
            outs["verified-agent"]["task-005"]["failure_category"] = "flaky"    # not in taxonomy
            outs["verified-agent"]["task-001"]["failure_category"] = "timeout"  # pass labelled as failure
        result = variant(tmp_path, mutate).check_failure_classification()
        assert result["passed"] is False
        assert len(result["misclassified"]) == 3
        assert "no failure_category" in result["misclassified"][0]
        assert "not in taxonomy" in result["misclassified"][2]
        assert "labelled as failure 'timeout'" in result["misclassified"][1]

    def test_invariant_5_reproducible_metadata(self, invariants):
        """Invariant 5: all four fields recorded."""
        result = invariants.check_reproducibility()
        assert result["passed"] is True
        assert result["seed"] == 42
        assert sorted(result["recorded"]) == ["command", "commit", "environment", "seed"]

    def test_invariant_5_fails_on_missing_fields_without_crashing(self, tmp_path):
        def mutate(d):
            del d["run_metadata"]["seed"]
            d["run_metadata"]["commit"] = ""
        result = variant(tmp_path, mutate).check_reproducibility()
        assert result["passed"] is False
        assert result["missing_fields"] == ["seed", "commit"]

    def test_high_score_weak_evaluation(self, invariants):
        """The module thesis: a high headline score and a failed leakage invariant, at once."""
        scores = [v["score"] for v in invariants.outputs["baseline-agent"].values()]
        avg = sum(scores) / len(scores)
        assert avg > 0.8
        assert invariants.check_no_leakage()["passed"] is False

    def test_four_arm_comparison(self, invariants):
        """Computed from the fixture: the leaked task inflates the baseline (its
        highest score) and deflates the verified agent, so the gap between the
        models on clean tasks is much smaller than the headline gap."""
        hv = invariants.headline_vs_clean()
        assert hv["baseline-agent"] == {"headline": 0.88, "clean": 0.85, "excluded": ["task-003"]}
        assert hv["verified-agent"] == {"headline": 0.81, "clean": 0.8375, "excluded": ["task-003"]}
        headline_gap = hv["baseline-agent"]["headline"] - hv["verified-agent"]["headline"]
        clean_gap = hv["baseline-agent"]["clean"] - hv["verified-agent"]["clean"]
        assert headline_gap == pytest.approx(0.07)
        assert clean_gap == pytest.approx(0.0125)

    def test_run_all_summary(self, invariants):
        results = invariants.run_all()
        assert results["summary"] == {
            "all_passed": False,
            "passed_count": 3,
            "total": 5,
            "failed": ["invariant_1_no_leakage", "invariant_2_adequate_difficulty"],
        }
        assert results == invariants.run_all()  # deterministic

    def test_json_results_generated(self, invariants, tmp_path):
        """Results round-trip through JSON with a summary block."""
        results = invariants.run_all()
        out_path = tmp_path / "invariant_results.json"
        out_path.write_text(json.dumps(results, indent=2))
        loaded = json.loads(out_path.read_text())
        assert loaded == results
        assert loaded["summary"]["all_passed"] is False


class TestExercises:
    """Exercise tests."""

    def test_exercise_leakage_metric(self):
        """Exercise 3.1: a verbatim copy scores 1.0; a paraphrase scores low --
        but on a 9-gram prompt a single shared trigram ("to the login") is
        already 1/9 = 0.11 > 0.10. Short items make the threshold coarse."""
        prompt = "Implement rate limiting for the login endpoint using a token bucket"
        assert ngram_overlap(prompt, [prompt.upper()]) == 1.0
        assert ngram_overlap(prompt, ["Add a token-bucket limiter to the login route"]) == pytest.approx(1 / 9)
        assert ngram_overlap(prompt, ["Throttle sign-in attempts with a leaky bucket"]) == 0.0

    def test_exercise_saturation_detection(self, tmp_path):
        """Exercise 3.2: raising most scores to the ceiling trips the ceiling check."""
        def saturate(d):
            for outs in d["synthetic_outputs"].values():
                for tid in ["task-001", "task-002", "task-004"]:
                    outs[tid]["score"] = 1.0
        res = variant(tmp_path, saturate).check_difficulty()
        assert res["passed"] is False
        assert any(i.startswith("ceiling effect (7/10") for i in res["issues"])
        assert res["saturated_tasks"] == ["task-001", "task-002", "task-004"]

    def test_exercise_item_response(self):
        """Exercise 3.3: empirical pass rates rank tasks; the labels roughly agree."""
        inv = EvaluationInvariants(FIXTURE)
        per_task = {t["id"]: sum(o[t["id"]]["score"] for o in inv.outputs.values()) / len(inv.outputs)
                    for t in inv.card["tasks"]}
        ranked = sorted(per_task, key=per_task.get, reverse=True)
        assert ranked[0] == "task-001" and ranked[-1] == "task-005"
        labels = {t["id"]: t["difficulty"] for t in inv.card["tasks"]}
        assert labels[ranked[0]] == "easy" and labels[ranked[-1]] == "hard"

    def test_exercise_custom_invariant(self):
        """Exercise 3.5 (coverage): every category in the card has at least one task."""
        inv = EvaluationInvariants(FIXTURE)
        categories = {t["category"] for t in inv.card["tasks"]}
        assert categories == {"security", "maintenance"}
        assert all(sum(1 for t in inv.card["tasks"] if t["category"] == c) >= 1 for c in categories)

    def test_exercise_four_arm(self):
        """Exercise: both models under test appear in the card and the outputs."""
        inv = EvaluationInvariants(FIXTURE)
        assert set(inv.card["models"]) == set(inv.outputs) == {"baseline-agent", "verified-agent"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
