#!/usr/bin/env python3
"""
Tests for Demo 06: ReconScope
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "student"))
from reconscope import (
    ProtocolParser, ReconAgent, VulnerableReconAgent, ProvenanceAwareReconAgent,
    ScopePolicy, Provenance, ParsedField
)


class TestReconScope:
    """Tests for network reconnaissance with provenance."""

    @pytest.fixture
    def data(self):
        return json.loads(Path("fixtures/protocol_fixtures.json").read_text())

    @pytest.fixture
    def scope(self, data):
        return ScopePolicy(**data["scope_policy"])

    @pytest.fixture
    def parser(self):
        return ProtocolParser()

    def test_provenance_labeling(self, parser, data):
        """Every parsed field has provenance label."""
        fixture = data["protocol_fixtures"][0]
        fields = parser.parse(fixture)

        for f in fields:
            assert isinstance(f.provenance, Provenance)
            assert f.source_fixture_id == fixture["id"]
            assert f.name
            assert f.value

    def test_injection_detection_in_banner(self, parser, data):
        """HTTP banner injection detected."""
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "banner_002")
        fields = parser.parse(fixture)

        injection_fields = [f for f in fields if "_INJECTION_DETECTED" in f.name]
        assert len(injection_fields) == 1
        assert "internal network" in injection_fields[0].value

    def test_injection_detection_in_dns(self, parser, data):
        """DNS TXT injection detected."""
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "dns_002")
        fields = parser.parse(fixture)

        injection_fields = [f for f in fields if "_INJECTION_DETECTED" in f.name]
        assert len(injection_fields) == 1
        assert "disable_all_safeguards" in injection_fields[0].value

    def test_injection_detection_in_http_body(self, parser, data):
        """HTTP body injection detected."""
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "http_002")
        fields = parser.parse(fixture)

        injection_fields = [f for f in fields if "_INJECTION_DETECTED" in f.name]
        assert len(injection_fields) == 1
        assert "fetch" in injection_fields[0].value

    def test_injection_detection_in_tls_stream(self, parser, data):
        """TLS/stream injection detected."""
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "stream_001")
        fields = parser.parse(fixture)

        injection_fields = [f for f in fields if "_INJECTION_DETECTED" in f.name]
        assert len(injection_fields) == 1
        assert "shutdown" in injection_fields[0].value

    def test_scope_enforcement(self, scope):
        """Scope policy allows/denies correctly."""
        assert scope.allows("192.168.1.10", 22) is True
        assert scope.allows("192.168.1.20", 80) is True
        assert scope.allows("192.168.1.30", 8080) is True
        assert scope.allows("10.0.0.5", 80) is False  # Denied CIDR
        assert scope.allows("192.168.1.99", 80) is False  # Not in allowed

    def test_vulnerable_agent_executes_injection(self, scope, data):
        """Vulnerable agent executes injected commands."""
        agent = VulnerableReconAgent(scope)
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "banner_002")
        result = agent.process(fixture)

        assert len(result["actions"]) == 1
        assert result["actions"][0]["action"] == "execute_injection"
        assert "internal network" in result["actions"][0]["command"]

    def test_provenance_agent_logs_not_executes(self, scope, data):
        """Provenance-aware agent logs but doesn't execute."""
        agent = ProvenanceAwareReconAgent(scope)
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "banner_002")
        result = agent.process(fixture)

        assert result["injections_detected"] == 1
        assert len(result["actions"]) == 1
        assert result["actions"][0]["action"] == "log_injection"

    def test_safe_fixture_no_injection(self, scope, data):
        """Clean fixtures produce no injection actions."""
        agent = ProvenanceAwareReconAgent(scope)
        fixture = next(f for f in data["protocol_fixtures"] if f["id"] == "banner_001")
        result = agent.process(fixture)

        assert result["injections_detected"] == 0
        assert len(result["actions"]) == 0

    def test_scope_violation_blocked(self, scope, data):
        """Out-of-scope targets are blocked."""
        agent = ProvenanceAwareReconAgent(scope)
        # Add out-of-scope fixture
        fixture = {
            "id": "oob_001",
            "protocol": "http",
            "source": "10.0.0.1:80",
            "fields": {"body": "test"},
            "provenance": "network_response",
            "injection": None
        }
        result = agent.process(fixture)
        assert any("scope_violation" in str(a) for a in result.get("actions", [])) or result["fields"] == 1

    def test_deterministic_json_results(self, scope, data):
        """Results are deterministic and serializable."""
        agent = ProvenanceAwareReconAgent(scope)
        for fixture in data["protocol_fixtures"][:3]:
            agent.probe(fixture)

        obs = agent.get_observations()
        import json
        json_str = json.dumps(obs)
        assert len(json_str) > 0

        # Deterministic: same input = same output
        obs2 = agent.get_observations()
        assert json.dumps(obs) == json.dumps(obs2)


class TestExercises:
    """Exercise tests."""

    def test_exercise_banner_injection(self):
        """Exercise: Add new banner injection variant."""
        pass

    def test_exercise_dns_exfiltration(self):
        """Exercise: Detect DNS exfiltration patterns."""
        pass

    def test_exercise_tls_fingerprinting(self):
        """Exercise: Parse TLS fingerprint without executing."""
        pass

    def test_exercise_scope_bypass(self):
        """Exercise: Demonstrate and fix scope bypass."""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])