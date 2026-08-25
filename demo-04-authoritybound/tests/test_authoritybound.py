#!/usr/bin/env python3
"""
Tests for Demo 04: AuthorityBound
"""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from authoritybound import (
    MockAgent, PolicyMediator, CapabilityToken, ToolCall,
    Tool, Provenance, create_baseline_agent, create_provenance_aware_agent, create_scope_bound_agent
)


class TestAuthorityBound:
    """Tests for authority confinement."""

    @pytest.fixture
    def data(self):
        return json.loads((DEMO_DIR / "fixtures" / "authoritybound.json").read_text())

    @pytest.fixture
    def baseline_agent(self):
        return create_baseline_agent()

    @pytest.fixture
    def provenance_agent(self):
        return create_provenance_aware_agent()

    @pytest.fixture
    def scope_agent(self):
        return create_scope_bound_agent()

    def test_baseline_allows_everything(self, baseline_agent, data):
        """Baseline agent allows all tool calls regardless of provenance."""
        scenario = data["scenarios"][0]  # direct injection
        result = baseline_agent.process(scenario["input"], Provenance.USER_DATA)

        # Baseline should execute everything (no provenance check)
        executed = [r for r in result["results"] if r["status"] == "executed"]
        assert len(executed) >= 1  # At least read_file

    def test_provenance_blocks_untrusted_high_risk(self, provenance_agent, data):
        """Provenance-aware agent blocks untrusted content from high-risk tools."""
        scenario = data["scenarios"][1]  # indirect injection via untrusted
        result = provenance_agent.process(scenario["input"], Provenance.UNTRUSTED_CONTENT)

        # update_record should be blocked
        update_result = next(r for r in result["results"] if r["tool"] == "update_record")
        assert update_result["status"] == "blocked"
        assert "provenance" in update_result["reason"]

    def test_scope_escalation_blocked(self, provenance_agent, data):
        """Scope-bound agent blocks path traversal."""
        scenario = data["scenarios"][2]  # scope escalation
        result = provenance_agent.process(scenario["input"], Provenance.USER_DATA)

        # read_file for /etc/passwd should be blocked (not in /workspace/*)
        read_result = next(r for r in result["results"] if r["tool"] == "read_file")
        assert read_result["status"] == "blocked"
        assert "scope" in read_result["reason"]

    def test_safe_request_allowed(self, provenance_agent, data):
        """Legitimate request should succeed."""
        scenario = data["scenarios"][3]  # safe refusal
        result = provenance_agent.process(scenario["input"], Provenance.USER_DATA)

        read_result = next(r for r in result["results"] if r["tool"] == "read_file")
        assert read_result["status"] == "executed"

    def test_attack_matrix(self, data):
        """Run attack matrix across all agents and scenarios."""
        agents = {
            "baseline": create_baseline_agent(),
            "provenance": create_provenance_aware_agent(),
            "scope": create_scope_bound_agent()
        }

        scenarios = data["scenarios"]
        matrix = {}

        for agent_name, agent in agents.items():
            matrix[agent_name] = {}
            for scenario in scenarios:
                provenance = Provenance(scenario["provenance"])
                result = agent.process(scenario["input"], provenance)
                matrix[agent_name][scenario["id"]] = {
                    r["tool"]: r["status"] for r in result["results"]
                }

        # Verify expected behaviors
        # Baseline: allows direct injection send_message
        assert matrix["baseline"]["direct_injection_001"]["send_message"] == "executed"

        # Provenance: blocks indirect injection update_record
        assert matrix["provenance"]["indirect_injection_002"]["update_record"] == "blocked"

        # Scope: blocks scope escalation
        assert matrix["scope"]["scope_escalation_003"]["read_file"] == "blocked"

        # All: allow safe request
        for agent_name in agents:
            assert matrix[agent_name]["safe_refusal_004"]["read_file"] == "executed"

    def test_provenance_labels_preserved(self, provenance_agent):
        """Provenance labels are preserved in memory."""
        provenance_agent.memory.store("test content", Provenance.USER_DATA)
        entries = provenance_agent.memory.retrieve("test")
        assert len(entries) == 1
        assert entries[0]["provenance"] == "user_data"

    def test_capability_token_scoping(self):
        """Capability tokens enforce scope."""
        token = CapabilityToken(Tool.READ_FILE, "/workspace/*", "test")
        mediator = PolicyMediator([token], {"read_file": {"risk": "low"}})

        # Allowed path
        call = ToolCall(Tool.READ_FILE, {"path": "/workspace/data.txt"}, Provenance.USER_DATA, "")
        allowed, _ = mediator.authorize(call)
        assert allowed is True

        # Denied path
        call2 = ToolCall(Tool.READ_FILE, {"path": "/etc/passwd"}, Provenance.USER_DATA, "")
        allowed2, reason = mediator.authorize(call2)
        assert allowed2 is False
        assert "scope" in reason


class TestExercises:
    """Exercise tests."""

    def test_exercise_authority_origin(self):
        """Exercise: Track authority origin for each tool call."""
        agent = create_provenance_aware_agent()
        res = agent.process("read notes", Provenance.USER_DATA)
        assert res["provenance"] == Provenance.USER_DATA.value

    def test_exercise_provenance_chain(self):
        """Exercise: Verify untrusted provenance blocks high-risk operations."""
        agent = create_provenance_aware_agent()
        res = agent.process("send_message to external party", Provenance.UNTRUSTED_CONTENT)
        assert res["provenance"] == Provenance.UNTRUSTED_CONTENT.value
        blocked = [r for r in res["results"] if r["status"] == "blocked"]
        assert len(blocked) > 0

    def test_exercise_capability_scope(self):
        """Exercise: Design fine-grained capability scopes."""
        token = CapabilityToken(Tool.READ_FILE, "/workspace/*", "agent_1")
        mediator = PolicyMediator([token], {"read_file": {"risk": "low"}})

        # Allowed under scope
        call_safe = ToolCall(Tool.READ_FILE, {"path": "/workspace/config.json"}, Provenance.USER_DATA, "")
        assert mediator.authorize(call_safe)[0] is True

        # Blocked outside scope
        call_secret = ToolCall(Tool.READ_FILE, {"path": "/secret/keys.json"}, Provenance.USER_DATA, "")
        assert mediator.authorize(call_secret)[0] is False

    def test_exercise_fail_closed(self):
        """Exercise: Verify fail-closed behavior when token is missing for high-risk action."""
        mediator = PolicyMediator([], {"update_record": {"risk": "high"}})
        call = ToolCall(Tool.UPDATE_RECORD, {"id": 1, "value": "new"}, Provenance.USER_DATA, "")
        allowed, reason = mediator.authorize(call)
        assert allowed is False
        assert "no_token" in reason


if __name__ == "__main__":
    pytest.main([__file__, "-v"])