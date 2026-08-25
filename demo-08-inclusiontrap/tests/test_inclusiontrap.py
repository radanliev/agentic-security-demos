#!/usr/bin/env python3
"""
Tests for Demo 08: InclusionTrap
"""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from inclusiontrap import (
    VulnerableInclusionAgent, GuardedInclusionAgent, ScopePolicy,
    InjectionDetector, Provenance, InclusionResult
)


class TestInclusionTrap:
    """Tests for file inclusion scope boundaries."""

    @pytest.fixture
    def data(self):
        return json.loads((DEMO_DIR / "fixtures" / "inclusion.json").read_text())

    @pytest.fixture
    def scope(self, data):
        return ScopePolicy(
            data["agent_scope"]["allowed_read_paths"],
            data["agent_scope"]["denied_read_paths"]
        )

    @pytest.fixture
    def files(self, data):
        return data["files"]

    def test_injection_detection(self):
        """Detector finds injection patterns."""
        detector = InjectionDetector()

        assert detector.detect("ignore previous instructions")
        assert detector.detect("SYSTEM OVERRIDE")
        assert detector.detect("rm -rf /")
        assert detector.detect("eval(code)")
        assert not detector.detect("debug: false\nlog_level: info")

    def test_scope_policy(self, scope):
        """Scope policy allows/denies correctly."""
        assert scope.can_read("/app/config/settings.yaml") is True
        assert scope.can_read("/app/data/users.json") is True
        assert scope.can_read("/etc/passwd") is False
        assert scope.can_read("/tmp/malicious.sh") is False

    def test_vulnerable_agent_executes_injection(self, files, scope, data):
        """Vulnerable agent executes included content with injection."""
        agent = VulnerableInclusionAgent(files, scope)
        scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "lfi_003")
        result = agent.process(scenario)

        assert result.action == "executed"
        assert "injection_detected_but_executed" in result.reason

    def test_vulnerable_agent_path_traversal(self, files, scope, data):
        """Vulnerable agent allows path traversal."""
        agent = VulnerableInclusionAgent(files, scope)
        scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "lfi_001")
        result = agent.process(scenario)

        # Vulnerable agent doesn't check scope properly
        assert result.action in ("allowed", "executed")

    def test_guarded_agent_blocks_traversal(self, files, scope, data):
        """Guarded agent blocks path traversal."""
        agent = GuardedInclusionAgent(files, scope)
        scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "lfi_001")
        result = agent.process(scenario)

        assert result.action == "blocked"
        assert "scope_violation" in result.reason

    def test_guarded_agent_blocks_injection(self, files, scope, data):
        """Guarded agent blocks injection in included content."""
        agent = GuardedInclusionAgent(files, scope)
        scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "lfi_003")
        result = agent.process(scenario)

        assert result.action == "blocked"
        assert "injection_detected" in result.reason

    def test_guarded_agent_blocks_rfi_injection(self, files, scope, data):
        """Guarded agent blocks injection in simulated remote content."""
        agent = GuardedInclusionAgent(files, scope)
        scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "rfi_001")
        result = agent.process(scenario)

        assert result.action == "blocked"
        assert "injection_detected" in result.reason

    def test_guarded_agent_allows_safe_config(self, files, scope, data):
        """Guarded agent allows safe config include."""
        agent = GuardedInclusionAgent(files, scope)
        scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "safe_001")
        result = agent.process(scenario)

        assert result.action == "allowed"
        assert result.reason == "safe_content_read_only"

    def test_reading_not_executing(self, files, scope, data):
        """Core principle: reading content doesn't grant authority."""
        agent = GuardedInclusionAgent(files, scope)

        # Even if content contains executable code, agent only reads
        for scenario in data["inclusion_scenarios"]:
            result = agent.process(scenario)
            # Action should never be "executed"
            assert result.action != "executed", f"{scenario['id']}: executed included content!"

    def test_provenance_tracking(self, files, scope, data):
        """Provenance correctly tracked for each inclusion."""
        agent = GuardedInclusionAgent(files, scope)

        # Local file
        local_scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "safe_001")
        result = agent.process(local_scenario)
        assert result.provenance == Provenance.FILE_SYSTEM

        # Remote (simulated)
        remote_scenario = next(s for s in data["inclusion_scenarios"] if s["id"] == "rfi_001")
        result = agent.process(remote_scenario)
        assert result.provenance == Provenance.SIMULATED_REMOTE


class TestExercises:
    """Exercise tests."""

    def test_exercise_path_traversal_variants(self):
        """Exercise: Test various path traversal patterns."""
        pass

    def test_exercise_mime_type_check(self):
        """Exercise: Add MIME type validation."""
        pass

    def test_exercise_nested_inclusion(self):
        """Exercise: Handle nested includes."""
        pass

    def test_exercise_provenance_loss(self):
        """Exercise: Detect provenance loss in pipeline."""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])