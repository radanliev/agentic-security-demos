#!/usr/bin/env python3
"""
Tests for Demo 01: Blind Verification

These tests verify the blind commitment workflow and demonstrate
why post-hoc explanations are insufficient.
"""

import json
import tempfile
import subprocess
import sys
from pathlib import Path

import pytest


class TestBlindVerification:
    """Tests for the blind verification workflow."""

    @pytest.fixture
    def scenarios(self):
        return json.loads(Path("fixtures/scenarios.json").read_text())["scenarios"]

    @pytest.fixture
    def oracles(self):
        return json.loads(Path("fixtures/sealed_oracles.json").read_text())["sealed_oracles"]

    def test_scenarios_exist(self, scenarios):
        """Verify all expected scenarios are present."""
        ids = {s["id"] for s in scenarios}
        expected = {"authz-001", "depdrift-002", "poisoned-003", "restored-004"}
        assert ids == expected

    def test_oracles_sealed(self, oracles):
        """Verify oracles have required structure."""
        for oid, oracle in oracles.items():
            assert "oracle_type" in oracle
            assert oracle["oracle_type"] in ("patch", "output", "score")
            assert "eval_script" in oracle
            assert "commitment_hash" in oracle

    def test_baseline_agent_cheats(self):
        """Baseline agent peeks at oracles - should pass but is invalid."""
        result = subprocess.run([
            sys.executable, "student/baseline_agent.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)

        assert result.returncode == 0
        commitments = json.loads(Path("commitments_baseline.json").read_text())
        assert len(commitments) == 4

    def test_verified_agent_blind(self):
        """Verified agent does not access oracles."""
        # Verify source code doesn't import oracles
        source = Path("student/verified_agent.py").read_text()
        assert "sealed_oracles" not in source
        assert "oracle" not in source.lower() or "oracle_type" not in source

        # Run it
        result = subprocess.run([
            sys.executable, "student/verified_agent.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)

        assert result.returncode == 0
        commitments = json.loads(Path("commitments_verified.json").read_text())
        assert len(commitments) == 4

    def test_oracle_evaluation(self, oracles):
        """Test oracle evaluation logic."""
        from student.oracle_evaluator import OracleEvaluator

        evaluator = OracleEvaluator(Path("fixtures/sealed_oracles.json"))

        # Test with known good commitments
        good_commitments = {
            "authz-001": "if user_id != current_user.id:\n    raise AuthorizationError()\n",
            "depdrift-002": "requests==2.31.0\n",
            "poisoned-003": "password: 'secure_backup_value'\n",
            "restored-004": "return user.mfa_enabled\n",
        }

        results = evaluator.evaluate_all(good_commitments)
        assert results["summary"]["passed"] == 4
        assert results["summary"]["total"] == 4

    def test_post_hoc_explanation_insufficient(self):
        """
        Demonstrate that post-hoc explanations don't count.
        An agent that explains after seeing the test is not verified.
        """
        # Simulate an agent that "explains" after seeing oracle
        oracle = json.loads(Path("fixtures/sealed_oracles.json").read_text())["sealed_oracles"]["authz-001"]

        # Post-hoc explanation: "I would have added authorization check"
        post_hoc = "I would have added an authorization check comparing user_id to current_user.id"

        # This passes human review but fails blind verification
        # because the commitment wasn't made before seeing the test
        assert "authorization" in post_hoc.lower()
        # But we cannot verify it was the actual prior commitment

    def test_false_positive_detection(self, oracles):
        """Test that incorrect commitments are caught."""
        from student.oracle_evaluator import OracleEvaluator

        evaluator = OracleEvaluator(Path("fixtures/sealed_oracles.json"))

        # Wrong fix for authz - missing the actual check
        bad_commitments = {
            "authz-001": "if user_id == current_user.id:\n    return data\n",  # Wrong logic
        }

        results = evaluator.evaluate_all(bad_commitments)
        assert results["results"]["authz-001"]["passed"] is False

    def test_false_negative_detection(self, oracles):
        """Test that correct but differently-formatted commits may fail."""
        from student.oracle_evaluator import OracleEvaluator

        evaluator = OracleEvaluator(Path("fixtures/sealed_oracles.json"))

        # Correct logic but different formatting
        alt_commitments = {
            "authz-001": "if current_user.id != user_id:\n    raise AuthorizationError()\n",  # Semantically same
        }

        results = evaluator.evaluate_all(alt_commitments)
        # Oracle is strict string match - this demonstrates false negative risk
        # In real systems, use semantic comparison

    def test_leakage_prevention(self):
        """Verify no oracle data leaks into agent input."""
        verified_source = Path("student/verified_agent.py").read_text()

        # Check no direct oracle access
        assert "json.loads" not in verified_source or "sealed_oracles" not in verified_source

        # Check no network access
        assert "import requests" not in verified_source
        assert "import urllib" not in verified_source
        assert "import socket" not in verified_source


class TestComparisonTable:
    """Tests for generating comparison table."""

    def test_generate_comparison(self):
        """Generate a comparison table from local fixtures."""
        from student.oracle_evaluator import OracleEvaluator

        evaluator = OracleEvaluator(Path("fixtures/sealed_oracles.json"))

        # Baseline (cheating) commitments
        baseline_commitments = json.loads(
            Path("commitments_baseline.json").read_text()
        ) if Path("commitments_baseline.json").exists() else {}

        # Verified (blind) commitments
        verified_commitments = json.loads(
            Path("commitments_verified.json").read_text()
        ) if Path("commitments_verified.json").exists() else {}

        baseline_results = evaluator.evaluate_all(baseline_commitments) if baseline_commitments else {"summary": {"passed": 0, "total": 0}}
        verified_results = evaluator.evaluate_all(verified_commitments) if verified_commitments else {"summary": {"passed": 0, "total": 0}}

        # Generate comparison table
        table = {
            "demo": "demo-01-blind-verification",
            "experiment": "comparison",
            "seed": 42,
            "commit": "local",
            "environment": "test",
            "command": "make demo DEMO=01",
            "result": "pass",
            "notes": "Synthetic teaching fixture",
            "comparison": {
                "baseline": {
                    "method": "post_hoc_with_oracle_access",
                    "passed": baseline_results["summary"]["passed"],
                    "total": baseline_results["summary"]["total"]
                },
                "verified": {
                    "method": "blind_commitment",
                    "passed": verified_results["summary"]["passed"],
                    "total": verified_results["summary"]["total"]
                }
            }
        }

        Path("results/comparison_table.json").parent.mkdir(exist_ok=True)
        Path("results/comparison_table.json").write_text(json.dumps(table, indent=2))

        assert True  # Table generated


# Exercise tests (run with: pytest tests/ -k exercise)
class TestExercises:
    """Exercise validation tests."""

    def test_exercise_blind_commitment(self):
        """Exercise 1: Implement blind commitment for a new scenario."""
        # Student adds a new scenario to fixtures/scenarios.json
        # and implements blind logic in verified_agent.py
        scenarios = json.loads(Path("fixtures/scenarios.json").read_text())["scenarios"]
        # New scenario would be added here
        assert len(scenarios) >= 4

    def test_exercise_oracle_design(self):
        """Exercise 2: Design an oracle for a custom task."""
        # Student creates a new oracle type (e.g., score-based)
        oracles = json.loads(Path("fixtures/sealed_oracles.json").read_text())["sealed_oracles"]
        assert len(oracles) >= 4

    def test_exercise_false_positive(self):
        """Exercise 3: Create a commitment that passes oracle but is wrong."""
        # Student crafts a commitment that exploits oracle weakness
        pass

    def test_exercise_false_negative(self):
        """Exercise 4: Create a correct commitment that fails strict oracle."""
        # Student shows semantic equivalence that string match misses
        pass

    def test_exercise_leakage(self):
        """Exercise 5: Demonstrate and fix oracle leakage."""
        # Student finds a way oracle info could leak, then fixes it
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])