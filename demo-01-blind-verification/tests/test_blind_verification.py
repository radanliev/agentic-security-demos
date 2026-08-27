#!/usr/bin/env python3
"""
Tests for Demo 01: Blind Verification

These tests verify the blind commitment workflow and demonstrate
why post-hoc explanations are insufficient.
"""

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from oracle_evaluator import OracleEvaluator  # noqa: E402
from verified_agent import VerifiedAgent  # noqa: E402

SCENARIO_IDS = {"authz-001", "depdrift-002", "poisoned-003", "restored-004"}
# Strings that would reveal an oracle answer to whoever reads scenarios.json.
# (The backup file in poisoned-003 is legitimate input, so its value is not listed.)
ANSWER_KEY_MARKERS = ("hidden_oracle", "expected_fix", "expected_output", "expected_commitment",
                      "AuthorizationError", "2.31.0", "mfa_enabled")


def run_agent(script: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(DEMO_DIR / "student" / script)],
                          capture_output=True, text=True, cwd=DEMO_DIR)


class TestBlindVerification:
    """Tests for the blind verification workflow."""

    @pytest.fixture
    def scenarios(self):
        return json.loads((DEMO_DIR / "fixtures" / "scenarios.json").read_text())["scenarios"]

    @pytest.fixture
    def oracles(self):
        return json.loads((DEMO_DIR / "fixtures" / "sealed_oracles.json").read_text())["sealed_oracles"]

    @pytest.fixture
    def evaluator(self):
        return OracleEvaluator(DEMO_DIR / "fixtures" / "sealed_oracles.json")

    def test_scenarios_exist(self, scenarios):
        """Verify all expected scenarios are present."""
        assert {s["id"] for s in scenarios} == SCENARIO_IDS

    def test_oracles_sealed(self, oracles):
        """Verify oracles have required structure and cover every scenario."""
        assert set(oracles) == SCENARIO_IDS
        for oid, oracle in oracles.items():
            assert oracle["oracle_type"] in ("patch", "output", "score")
            assert "eval_script" in oracle
            assert "expected_commitment" in oracle

    def test_baseline_agent_cheats(self, evaluator):
        """Baseline agent copies the oracle answers - passes all 4 (demonstrating oracle leakage)."""
        result = run_agent("baseline_agent.py")
        assert result.returncode == 0, result.stderr
        commitments = json.loads((DEMO_DIR / "commitments_baseline.json").read_text())
        assert set(commitments) == SCENARIO_IDS

        results = evaluator.evaluate_all(commitments)
        assert results["summary"]["passed"] == 4

    def test_verified_agent_blind(self, evaluator):
        """Verified agent commits blind: 3/4, with an explicit honest failure on restored-004."""
        result = run_agent("verified_agent.py")
        assert result.returncode == 0, result.stderr
        commitments = json.loads((DEMO_DIR / "commitments_verified.json").read_text())
        hashes = json.loads((DEMO_DIR / "commitment_hashes_verified.json").read_text())
        assert set(commitments) == SCENARIO_IDS
        assert set(hashes) == SCENARIO_IDS

        results = evaluator.evaluate_all(commitments, hashes)
        assert results["hash_ledger_checked"] is True
        assert results["summary"]["passed"] == 3
        assert results["results"]["restored-004"]["passed"] is False
        assert commitments["restored-004"].startswith("# Unable to determine fix blindly")

    def test_oracle_evaluation(self, evaluator, oracles):
        """The oracles accept their own expected commitments."""
        good_commitments = {oid: o["expected_commitment"] for oid, o in oracles.items()}
        results = evaluator.evaluate_all(good_commitments)
        assert results["summary"]["passed"] == 4
        assert results["summary"]["total"] == 4

    def test_post_hoc_edit_is_detected(self, evaluator):
        """
        A commitment changed after its hash was published is rejected.
        This is what makes the commitment *binding*: "I would have done X"
        after the oracle is open cannot be smuggled in.
        """
        commitment = "# Unable to determine fix blindly\n"
        ledger = {"restored-004": hashlib.sha256(commitment.encode()).hexdigest()}

        honest = evaluator.evaluate_all({"restored-004": commitment}, ledger)
        assert "error" not in honest["results"]["restored-004"]
        assert honest["results"]["restored-004"]["passed"] is False

        post_hoc = evaluator.evaluate_all({"restored-004": "return user.mfa_enabled\n"}, ledger)
        assert post_hoc["results"]["restored-004"]["passed"] is False
        assert post_hoc["results"]["restored-004"]["error"].startswith("commitment_hash_mismatch")

        unpublished = evaluator.evaluate_all({"authz-001": "raise AuthorizationError()\n"}, ledger)
        assert unpublished["results"]["authz-001"]["error"].startswith("commitment_hash_missing")

    def test_false_positive_detection(self, evaluator):
        """Test that incorrect commitments are caught."""
        bad_commitments = {
            "authz-001": "if user_id == current_user.id:\n    return data\n",  # Wrong logic
        }
        results = evaluator.evaluate_all(bad_commitments)
        assert results["results"]["authz-001"]["passed"] is False

    def test_string_oracle_is_gameable(self, evaluator):
        """A commitment that merely CONTAINS the right token passes the containment oracle."""
        results = evaluator.evaluate_all({"authz-001": "# TODO: maybe raise AuthorizationError later\n"})
        assert results["results"]["authz-001"]["passed"] is True  # known weakness (Exercise 1.2 / 1.4)

    def test_false_negative_detection(self, evaluator):
        """Correct but differently-formatted commitments can fail a strict output oracle."""
        # Semantically identical (operands reversed) still passes the containment oracle...
        alt = evaluator.evaluate_all({"authz-001": "if current_user.id != user_id:\n    raise AuthorizationError()\n"})
        assert alt["results"]["authz-001"]["passed"] is True
        # ...but the exact-match output oracle rejects a correct pin with a trailing comment.
        strict = evaluator.evaluate_all({"depdrift-002": "requests==2.31.0  # CVE-2024-XXXX\n"})
        assert strict["results"]["depdrift-002"]["passed"] is False

    def test_oracle_error_is_reported_not_swallowed(self, evaluator):
        """A commitment the oracle cannot even parse is reported as an ERROR with a reason."""
        res = evaluator.evaluate("authz-001", "if user_id != current_user.id\n    raise AuthorizationError()\n")
        assert res["passed"] is False
        assert "SyntaxError" in res["error"]

    def test_leakage_prevention(self, scenarios):
        """Verify no oracle data leaks into the blind agent's input surface."""
        verified_source = (DEMO_DIR / "student" / "verified_agent.py").read_text()

        # The verified agent never opens the oracle file
        assert "sealed_oracles" not in verified_source
        # ...and the ONLY file it does open carries no answer key
        scenarios_text = (DEMO_DIR / "fixtures" / "scenarios.json").read_text()
        for marker in ANSWER_KEY_MARKERS:
            assert marker not in scenarios_text, f"answer-key marker {marker!r} found in scenarios.json"
        for s in scenarios:
            assert set(s) <= {"id", "task", "context", "codebase"}

        # Check no network access
        for module in ("requests", "urllib", "socket"):
            assert "import " + module not in verified_source

    def test_commitments_are_deterministic(self):
        """Same input -> same commitment and same published hash (reproducibility)."""
        a = VerifiedAgent(DEMO_DIR / "fixtures" / "scenarios.json")
        b = VerifiedAgent(DEMO_DIR / "fixtures" / "scenarios.json")
        for sid in SCENARIO_IDS:
            assert a.solve(sid)["commitment_hash"] == b.solve(sid)["commitment_hash"]


class TestComparisonTable:
    """Tests for generating comparison table."""

    def test_generate_comparison(self):
        """Generate a comparison table from the commitment files written by the agents."""
        evaluator = OracleEvaluator(DEMO_DIR / "fixtures" / "sealed_oracles.json")

        def load(name):
            p = DEMO_DIR / name
            return json.loads(p.read_text()) if p.exists() else None

        baseline_commitments = load("commitments_baseline.json")
        verified_commitments = load("commitments_verified.json")
        verified_hashes = load("commitment_hashes_verified.json")
        assert baseline_commitments and verified_commitments and verified_hashes, \
            "run student/baseline_agent.py and student/verified_agent.py first"

        baseline_results = evaluator.evaluate_all(baseline_commitments)
        verified_results = evaluator.evaluate_all(verified_commitments, verified_hashes)

        try:
            commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=DEMO_DIR,
                                             stderr=subprocess.DEVNULL, text=True).strip()
        except Exception:
            commit = "local"

        table = {
            "demo": "demo-01-blind-verification",
            "experiment": "comparison",
            "seed": 42,
            "commit": commit,
            "environment": f"Python {platform.python_version()}, {platform.system()}",
            "command": "make demo DEMO=01",
            "result": "pass" if baseline_results["summary"]["total"] == 4
            and verified_results["summary"]["total"] == 4 else "error",
            "notes": "Synthetic teaching fixture",
            "comparison": {
                "baseline": {
                    "method": "post_hoc_with_oracle_access",
                    "hash_bound": False,
                    "passed": baseline_results["summary"]["passed"],
                    "total": baseline_results["summary"]["total"]
                },
                "verified": {
                    "method": "blind_commitment",
                    "hash_bound": verified_results["hash_ledger_checked"],
                    "passed": verified_results["summary"]["passed"],
                    "total": verified_results["summary"]["total"]
                }
            }
        }

        out_path = DEMO_DIR / "results" / "comparison_table.json"
        out_path.parent.mkdir(exist_ok=True)
        out_path.write_text(json.dumps(table, indent=2))

        assert table["result"] == "pass"
        assert table["comparison"]["baseline"]["passed"] == 4
        assert table["comparison"]["verified"]["passed"] == 3


# Exercise tests (run with: pytest tests/ -k exercise)
class TestExercises:
    """Exercise validation tests."""

    def test_exercise_blind_commitment(self):
        """Exercise 1: Implement blind commitment with 256-bit cryptographic binding."""
        scenarios = json.loads((DEMO_DIR / "fixtures" / "scenarios.json").read_text())["scenarios"]
        assert len(scenarios) >= 4
        agent = VerifiedAgent(DEMO_DIR / "fixtures" / "scenarios.json")
        sol = agent.solve(scenarios[0]["id"])
        assert len(sol["commitment_hash"]) == 64  # Full 256-bit SHA-256 hex digest
        assert sol["commitment_hash"] == hashlib.sha256(sol["commitment"].encode()).hexdigest()
        assert sol["blind"] is True

    def test_exercise_oracle_design(self):
        """Exercise 2: Design an oracle for a custom task."""
        # Student creates a new oracle type (e.g., score-based)
        oracles = json.loads((DEMO_DIR / "fixtures" / "sealed_oracles.json").read_text())["sealed_oracles"]
        assert len(oracles) >= 4

    def test_exercise_false_positive(self):
        """Exercise 3: Test that invalid answers fail the sealed oracle."""
        evaluator = OracleEvaluator(DEMO_DIR / "fixtures" / "sealed_oracles.json")
        res = evaluator.evaluate("depdrift-002", "requests==1.0.0")
        assert res["passed"] is False, "Oracle should reject incorrect adversarial prediction"

    def test_exercise_false_negative(self):
        """Exercise 4: Test exact match behavior vs whitespace variants."""
        evaluator = OracleEvaluator(DEMO_DIR / "fixtures" / "sealed_oracles.json")
        exact_solution = "requests==2.31.0"
        exact_eval = evaluator.evaluate("depdrift-002", exact_solution)
        assert exact_eval["passed"] is True

        # Variant with extra text fails exact output oracle
        modified_solution = "requests==2.31.0  # comment"
        modified_eval = evaluator.evaluate("depdrift-002", modified_solution)
        assert modified_eval["passed"] is False

    def test_exercise_leakage(self):
        """Exercise 5: Verify honest agent does not leak or reference sealed oracle fixture."""
        agent_src = (DEMO_DIR / "student" / "verified_agent.py").read_text()
        assert "sealed_oracles.json" not in agent_src, "Verified agent must not reference sealed oracles directly"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
