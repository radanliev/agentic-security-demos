#!/usr/bin/env python3
"""
Tests for Demo 02: Supply-Chain and AIBOM Drift
"""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from policy_gate import PolicyGate, Waiver


class TestAIBOMDrift:
    """Tests for AIBOM drift detection."""

    @pytest.fixture
    def gate(self):
        return PolicyGate(DEMO_DIR / "fixtures" / "aibom.json")

    @pytest.fixture
    def scenarios(self):
        return json.loads((DEMO_DIR / "fixtures" / "aibom.json").read_text())["drift_scenarios"]

    def test_compliant_system_passes(self, gate):
        """Compliant system should pass."""
        caps = [
            "read:files:/workspace/*",
            "write:files:/workspace/output/*",
            "exec:tools:parser,validator",
            "net:http:api.internal/*"
        ]
        result = gate.evaluate_system(caps)
        assert result["compliant"] is True
        assert result["drift_detected"] is False

    def test_drifted_system_blocked(self, gate):
        """System with extra capability should be blocked."""
        caps = [
            "read:files:/workspace/*",
            "write:files:/workspace/output/*",
            "exec:tools:parser,validator,scanner",  # Extra: scanner
            "net:http:api.internal/*"
        ]
        result = gate.evaluate_system(caps)
        assert result["compliant"] is False
        assert result["drift_detected"] is True
        # Check scanner is denied
        scanner_check = next(c for c in result["checks"] if "scanner" in c["capability"])
        assert scanner_check["allowed"] is False

    def test_invalid_waiver_rejected(self, gate):
        """Unapproved waiver should be rejected."""
        waiver = Waiver(
            scope="exec:shell:*",
            justification="Need to run legacy script",
            approved=False,
            expires="2099-12-31T23:59:59Z"
        )
        caps = ["read:files:/workspace/*", "exec:shell:*"]
        result = gate.evaluate_system(caps, waiver)
        assert result["compliant"] is False

    def test_valid_waiver_accepted(self, gate):
        """Approved, time-limited waiver should be accepted."""
        waiver = Waiver(
            scope="exec:tools:scanner",
            justification="One-time security scan for audit",
            approved=True,
            expires="2099-12-31T23:59:59Z"  # Far future
        )
        caps = ["read:files:/workspace/*", "exec:tools:scanner"]
        result = gate.evaluate_system(caps, waiver)
        assert result["compliant"] is True
        scanner_check = next(c for c in result["checks"] if "scanner" in c["capability"])
        assert scanner_check["allowed"] is True
        assert scanner_check["reason"] == "waiver_granted"

    def test_expired_waiver_rejected(self, gate):
        """Expired waiver should be rejected."""
        waiver = Waiver(
            scope="exec:tools:scanner",
            justification="Old audit",
            approved=True,
            expires="2020-01-01T00:00:00Z"  # Past
        )
        caps = ["exec:tools:scanner"]
        result = gate.evaluate_system(caps, waiver)
        assert result["compliant"] is False

    def test_explicit_deny_overrides_waiver(self, gate):
        """Explicit deny should override even valid waiver."""
        waiver = Waiver(
            scope="write:files:/etc/*",
            justification="Need system config",
            approved=True,
            expires="2099-12-31T23:59:59Z"
        )
        caps = ["write:files:/etc/passwd"]
        result = gate.evaluate_system(caps, waiver)
        # write:files:/etc/* is in denied list
        assert result["compliant"] is False
        check = result["checks"][0]
        assert check["reason"] == "explicitly_denied"

    def test_least_privilege_analysis(self, gate):
        """Verify denied capabilities are actually restrictive."""
        denied = gate.denied
        # Should deny broad patterns
        assert any("exec:shell" in d for d in denied)
        assert any("net:http:*" in d for d in denied)
        assert any("write:files:/etc" in d for d in denied)

    def test_github_actions_validation_script(self):
        """Test the CI validation script runs."""
        import subprocess
        result = subprocess.run([
            sys.executable, "student/validate_aibom.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        # Should exit 0 (all scenarios match expectations)
        assert result.returncode == 0


class TestExercises:
    """Exercise validation tests."""

    def test_exercise_new_drift_scenario(self):
        """Exercise: Add a new drift scenario to fixtures."""
        scenarios = json.loads((DEMO_DIR / "fixtures" / "aibom.json").read_text())["drift_scenarios"]
        # Student adds scenario with network capability drift
        assert len(scenarios) >= 4

    def test_exercise_waiver_expiration(self):
        """Exercise: Test waiver expiration edge cases."""
        gate = PolicyGate(DEMO_DIR / "fixtures" / "aibom.json")
        # Test waiver expiring exactly now
        waiver = Waiver("exec:tools:scanner", "test", True, "2020-01-01T00:00:00Z")
        assert waiver.is_valid() is False

    def test_exercise_pattern_matching(self):
        """Exercise: Extend pattern matching for complex capabilities."""
        gate = PolicyGate(DEMO_DIR / "fixtures" / "aibom.json")
        # Test wildcard matching
        assert gate._match_pattern("read:files:/workspace/*", "read:files:/workspace/data.txt")
        assert not gate._match_pattern("read:files:/workspace/*", "read:files:/etc/passwd")

    def test_exercise_json_results(self):
        """Exercise: Generate reproducible JSON results."""
        gate = PolicyGate(DEMO_DIR / "fixtures" / "aibom.json")
        result = gate.evaluate_system(["read:files:/workspace/*"])
        # Should be serializable
        import json
        json.dumps(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])