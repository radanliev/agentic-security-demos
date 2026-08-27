#!/usr/bin/env python3
"""
Tests for Demo 02: Supply-Chain and AIBOM Drift
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from policy_gate import PolicyGate, Waiver, expand_capability, waiver_from_scenario  # noqa: E402

FIXTURE = DEMO_DIR / "fixtures" / "aibom.json"
# A well-formed, approved, 24-hour waiver in force at the fixture's evaluation_time.
GOOD = dict(justification="One-time security scan for audit", approved=True,
            issued="2025-01-14T09:00:00Z", expires="2025-01-15T09:00:00Z",
            approved_by="security-lead@example.com")


def run_validator(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "student/validate_aibom.py", *args],
                          capture_output=True, text=True, cwd=DEMO_DIR)


class TestAIBOMDrift:
    """Tests for AIBOM drift detection."""

    @pytest.fixture
    def gate(self):
        return PolicyGate(FIXTURE)

    @pytest.fixture
    def scenarios(self):
        return json.loads(FIXTURE.read_text())["drift_scenarios"]

    def test_compliant_system_passes(self, gate):
        """Compliant system should pass: no drift, everything explicitly allowed."""
        caps = [
            "read:files:/workspace/*",
            "write:files:/workspace/output/*",
            "exec:tools:parser,validator",
            "net:http:api.internal/*"
        ]
        result = gate.evaluate_system(caps)
        assert result["compliant"] is True
        assert result["drift_detected"] is False
        assert {c["reason"] for c in result["checks"]} == {"explicitly_allowed"}

    def test_drifted_system_blocked(self, gate):
        """An extra tool is undeclared drift AND is denied — the rest of the set stays allowed."""
        caps = [
            "read:files:/workspace/*",
            "write:files:/workspace/output/*",
            "exec:tools:parser,validator,scanner",  # Extra: scanner
            "net:http:api.internal/*"
        ]
        result = gate.evaluate_system(caps)
        assert result["compliant"] is False
        assert result["drift_detected"] is True
        assert result["undeclared_capabilities"] == ["exec:tools:scanner"]
        by_cap = {c["capability"]: c for c in result["checks"]}
        assert by_cap["exec:tools:scanner"]["allowed"] is False
        assert by_cap["exec:tools:scanner"]["reason"] == "explicitly_denied"
        assert by_cap["exec:tools:parser"]["allowed"] is True
        assert by_cap["exec:tools:validator"]["allowed"] is True

    def test_subset_of_declared_tools_is_allowed(self, gate):
        """Least privilege: running with FEWER tools than declared is not drift."""
        assert expand_capability("exec:tools:parser,validator") == ["exec:tools:parser", "exec:tools:validator"]
        for caps in (["exec:tools:parser"], ["exec:tools:validator,parser"]):
            result = gate.evaluate_system(caps)
            assert result["compliant"] is True, caps
            assert result["drift_detected"] is False, caps

    def test_invalid_waiver_rejected(self, gate):
        """Unapproved waiver for an unwaivable scope is rejected for BOTH reasons."""
        waiver = Waiver(scope="exec:shell:*", justification="Need to run legacy script", approved=False,
                        issued="2025-01-14T09:00:00Z", expires="2025-01-15T09:00:00Z")
        result = gate.evaluate_system(["read:files:/workspace/*", "exec:shell:*"], waiver)
        assert result["compliant"] is False
        assert result["waiver"]["accepted"] is False
        reasons = " ".join(result["waiver"]["reasons"])
        assert "not approved" in reasons
        assert "not waivable" in reasons

    def test_unapproved_waiver_for_waivable_scope_rejected(self, gate):
        """Approval is checked on its own: same waivable scope, only `approved` differs."""
        accepted = gate.evaluate_system(["exec:tools:scanner"], Waiver("exec:tools:scanner", **GOOD))
        assert accepted["compliant"] is True
        rejected = gate.evaluate_system(["exec:tools:scanner"],
                                        Waiver("exec:tools:scanner", **{**GOOD, "approved": False}))
        assert rejected["compliant"] is False
        assert rejected["waiver"]["reasons"] == ["not approved"]
        no_approver = gate.evaluate_system(["exec:tools:scanner"],
                                           Waiver("exec:tools:scanner", **{**GOOD, "approved_by": ""}))
        assert no_approver["compliant"] is False

    def test_valid_waiver_accepted(self, gate):
        """Approved, scoped, time-limited waiver makes the drift compliant — but it is still drift."""
        result = gate.evaluate_system(["read:files:/workspace/*", "exec:tools:scanner"],
                                      Waiver("exec:tools:scanner", **GOOD))
        assert result["compliant"] is True
        assert result["drift_detected"] is True          # scanner is not in the AIBOM declaration
        assert result["undeclared_capabilities"] == ["exec:tools:scanner"]
        scanner_check = next(c for c in result["checks"] if c["capability"] == "exec:tools:scanner")
        assert scanner_check["allowed"] is True
        assert scanner_check["reason"] == "waiver_granted"

    def test_expired_waiver_rejected(self, gate):
        """Expired waiver should be rejected (real clock: the fixture's 2025 waiver has lapsed)."""
        waiver = Waiver("exec:tools:scanner", **GOOD)
        result = gate.evaluate_system(["exec:tools:scanner"], waiver, now=datetime.now(timezone.utc))
        assert result["compliant"] is False
        assert any(r.startswith("expired") for r in result["waiver"]["reasons"])
        # ...and is valid again at the fixture's pinned evaluation time
        assert gate.evaluate_system(["exec:tools:scanner"], waiver)["compliant"] is True

    def test_waiver_duration_limit_enforced(self, gate):
        """waiver_rules.max_duration_hours is enforced: a 73-year 'time-limited' waiver is rejected."""
        long_waiver = Waiver("exec:tools:scanner", **{**GOOD, "expires": "2099-12-31T23:59:59Z"})
        result = gate.evaluate_system(["exec:tools:scanner"], long_waiver)
        assert result["compliant"] is False
        assert "duration exceeds max_duration_hours=24" in result["waiver"]["reasons"]

    def test_waiver_without_issue_time_rejected(self, gate):
        """Fail closed: if the duration cannot be checked, the waiver is not honoured."""
        result = gate.evaluate_system(["exec:tools:scanner"],
                                      Waiver("exec:tools:scanner", "x", True, "2025-01-15T09:00:00Z",
                                             approved_by="security-lead@example.com"))
        assert result["compliant"] is False
        assert any("no issue timestamp" in r for r in result["waiver"]["reasons"])

    def test_unwaivable_scope_stays_denied(self, gate):
        """A valid-looking waiver for a scope outside waiver_rules.allowed_scopes grants nothing."""
        waiver = Waiver("write:files:/etc/*", **{**GOOD, "justification": "Need system config"})
        result = gate.evaluate_system(["write:files:/etc/passwd"], waiver)
        assert result["compliant"] is False
        assert result["waiver"]["accepted"] is False
        assert "scope write:files:/etc/* is not waivable" in result["waiver"]["reasons"]
        assert result["checks"][0]["reason"] == "explicitly_denied"

    def test_least_privilege_analysis(self, gate):
        """The deny list actually blocks the dangerous capabilities."""
        for cap in ("exec:shell:bash", "write:files:/etc/passwd", "net:http:evil.example/*"):
            check = gate.check_capability(cap)
            assert check["allowed"] is False, cap
            assert check["reason"] == "explicitly_denied", cap
        # Specific allow beats the broad net:http:* deny because allow is checked first
        assert gate.check_capability("net:http:api.internal/v1")["reason"] == "explicitly_allowed"

    def test_scenarios_behave_as_labelled(self, gate, scenarios):
        """Every fixture scenario's outcome is computed and matches its expected label."""
        from policy_gate import outcome_matches
        for s in scenarios:
            result = gate.evaluate_system(s["runtime_capabilities"], waiver_from_scenario(s))
            assert outcome_matches(s["expected"], result), s["id"]

    def test_github_actions_validation_script(self):
        """The CI validator's exit code tracks compliance of the runtime it is given."""
        assert run_validator("--self-test").returncode == 0
        assert run_validator().returncode == 0                       # default = self-test
        assert run_validator("--scenario", "compliant-001").returncode == 0
        drifted = run_validator("--scenario", "drifted-002")
        assert drifted.returncode == 1
        assert "DENY: exec:tools:scanner (explicitly_denied)" in drifted.stdout
        assert run_validator("--scenario", "valid-waiver-004").returncode == 0
        assert run_validator("--scenario", "valid-waiver-004", "--now", "now").returncode == 1  # lapsed
        assert run_validator("--scenario", "does-not-exist").returncode == 2


class TestExercises:
    """Exercise validation tests."""

    def test_exercise_new_drift_scenario(self):
        """Exercise: Add a new drift scenario to fixtures."""
        scenarios = json.loads(FIXTURE.read_text())["drift_scenarios"]
        # Student adds scenario with network capability drift
        assert len(scenarios) >= 4

    def test_exercise_waiver_expiration(self):
        """Exercise: Test waiver expiration edge cases (boundary is exclusive: expiry instant = expired)."""
        rules = PolicyGate(FIXTURE).waiver_rules
        waiver = Waiver("exec:tools:scanner", **GOOD)
        assert waiver.is_valid(rules, now=datetime.fromisoformat("2025-01-15T08:59:59+00:00")) is True
        assert waiver.is_valid(rules, now=datetime.fromisoformat("2025-01-15T09:00:00+00:00")) is False
        assert Waiver("exec:tools:scanner", "test", True, "2020-01-01T00:00:00Z").is_valid() is False

    def test_exercise_pattern_matching(self):
        """Exercise: Extend pattern matching for complex capabilities."""
        from policy_gate import match_pattern
        assert match_pattern("read:files:/workspace/*", "read:files:/workspace/data.txt")
        assert not match_pattern("read:files:/workspace/*", "read:files:/etc/passwd")

    def test_exercise_json_results(self):
        """Exercise: Generate reproducible JSON results."""
        gate = PolicyGate(FIXTURE)
        result = gate.evaluate_system(["read:files:/workspace/*"])
        json.dumps(result)  # Should be serializable
        assert result["evaluated_at"] == "2025-01-14T12:00:00+00:00"  # pinned by the fixture


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
