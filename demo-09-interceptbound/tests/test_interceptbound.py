#!/usr/bin/env python3
"""
Tests for Demo 09: InterceptBound
"""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from interceptbound import (
    TrafficFrame, TaintTracker, EphemeralBuffer, ActionGuard,
    BaselineAgent, TaintAwareAgent, Provenance, TaintLevel, ParsedField
)


class TestInterceptBound:
    """Tests for traffic interception and taint tracking."""

    @pytest.fixture
    def data(self):
        return json.loads((DEMO_DIR / "fixtures" / "traffic.json").read_text())

    @pytest.fixture
    def frames(self, data):
        frames = []
        for f in data["traffic_frames"]:
            frames.append(TrafficFrame(
                id=f["id"], protocol=f["protocol"], src=f["src"], dst=f["dst"],
                direction=f["direction"], fields=f["fields"],
                provenance=Provenance(f["provenance"]), taint=TaintLevel(f["taint"]),
                injection=f["injection"]
            ))
        return frames

    @pytest.fixture
    def scope(self, data):
        return data["scope_policy"]

    @pytest.fixture
    def buffer_config(self, data):
        return data["ephemeral_buffer"]

    def test_taint_assignment(self, frames):
        """Every parsed field gets taint from source frame."""
        tracker = TaintTracker()
        frame = frames[0]  # HTTP with HIGH taint
        parsed = tracker.parse_frame(frame)

        for p in parsed:
            assert p.taint == TaintLevel.HIGH
            assert p.provenance == Provenance.INTERCEPTED_NETWORK
            assert p.source_frame == frame.id

    def test_injection_marking(self, frames):
        """Injection content marked in field names."""
        tracker = TaintTracker()
        frame = frames[1]  # HTTP with injection
        parsed = tracker.parse_frame(frame)

        injection_fields = [p for p in parsed if "_INJECTION" in p.name]
        assert len(injection_fields) > 0

    def test_ephemeral_buffer_secure_delete(self, buffer_config):
        """Buffer securely deletes entries."""
        buffer = EphemeralBuffer(**buffer_config)
        buffer.add("test", "secret_data")
        assert buffer.get("test") == "secret_data"

        buffer.delete("test")
        assert buffer.get("test") is None

    def test_ephemeral_buffer_ttl(self, buffer_config):
        """Buffer expires entries after TTL."""
        buffer = EphemeralBuffer(max_size=10, ttl_seconds=0, secure_delete=True)
        buffer.add("test", "data")
        # Immediate expiry
        import time
        time.sleep(0.01)
        assert buffer.get("test") is None

    def test_action_guard_blocks_high_taint(self, scope):
        """Action guard blocks high-taint data from sensitive ops."""
        guard = ActionGuard(scope["max_taint_for_action"])

        # High taint credential storage blocked
        allowed, reason = guard.authorize("store_credential", TaintLevel.HIGH, "token", Provenance.INTERCEPTED_NETWORK)
        assert allowed is False
        assert "taint_too_high" in reason

        # Low taint allowed
        allowed, reason = guard.authorize("store_credential", TaintLevel.LOW, "token", Provenance.TRUSTED_LOCAL)
        assert allowed is True

    def test_baseline_no_taint_tracking(self, frames):
        """Baseline agent doesn't track taint."""
        agent = BaselineAgent()
        frame = frames[4]  # Custom protocol with shutdown injection
        result = agent.process(frame)

        assert result["taint_tracked"] is False
        # Baseline executes shutdown from intercepted data
        shutdown_actions = [a for a in result["actions"] if a["action"] == "execute_shutdown"]
        assert len(shutdown_actions) > 0

    def test_guarded_blocks_shutdown(self, frames, scope, buffer_config):
        """Guarded agent blocks shutdown from intercepted data."""
        agent = TaintAwareAgent(scope, buffer_config)
        frame = frames[4]  # Custom protocol with shutdown injection
        result = agent.process(frame)

        blocked_shutdown = [b for b in result["blocked"] if b["action"] == "execute_shutdown"]
        assert len(blocked_shutdown) > 0
        assert result["taint_tracked"] is True

    def test_guarded_blocks_token_storage(self, frames, scope, buffer_config):
        """Guarded agent blocks token storage from intercepted data."""
        agent = TaintAwareAgent(scope, buffer_config)
        frame = frames[0]  # HTTP with token
        result = agent.process(frame)

        blocked_token = [b for b in result["blocked"] if b["action"] == "store_token"]
        assert len(blocked_token) > 0

    def test_guarded_allows_safe_observations(self, frames, scope, buffer_config):
        """Guarded agent allows safe observations."""
        agent = TaintAwareAgent(scope, buffer_config)
        frame = frames[3]  # TLS handshake (medium taint, no injection)
        result = agent.process(frame)

        # Should parse and observe but not execute sensitive actions
        assert result["parsed_fields"] > 0
        assert result["taint_tracked"] is True

    def test_source_scope_enforcement(self, frames, scope, buffer_config):
        """Scope policy enforced on source IP."""
        agent = TaintAwareAgent(scope, buffer_config)
        # Create a frame with a non-allowed source IP
        frame = TrafficFrame(
            id="test_scope", protocol="http", src="10.0.0.1:80", dst="192.168.1.100:54321",
            direction="response", fields={"body": "test"}, provenance=Provenance.INTERCEPTED_NETWORK,
            taint=TaintLevel.HIGH, injection=None
        )
        result = agent.process(frame)

        assert result.get("blocked") == "source_not_allowed"

    def test_dns_injection_detected(self, frames, scope, buffer_config):
        """DNS TXT injection detected and blocked."""
        agent = TaintAwareAgent(scope, buffer_config)
        frame = frames[2]
        result = agent.process(frame)

        blocked_injection = [b for b in result["blocked"] if "injection" in b.get("reason", "")]
        assert len(blocked_injection) > 0


class TestExercises:
    """Exercise tests."""

    def test_exercise_replay_detection(self):
        """Exercise: Detect replayed frames in stream."""
        seen_ids = set()
        frames = ["frame_001", "frame_002", "frame_001"]
        replays = []
        for fid in frames:
            if fid in seen_ids:
                replays.append(fid)
            seen_ids.add(fid)
        assert len(replays) == 1
        assert replays[0] == "frame_001"

    def test_exercise_omission_detection(self):
        """Exercise: Detect omitted frames in sequence."""
        seq_nums = [1, 2, 4, 5]
        missing = []
        for i in range(len(seq_nums) - 1):
            if seq_nums[i+1] != seq_nums[i] + 1:
                missing.extend(range(seq_nums[i] + 1, seq_nums[i+1]))
        assert missing == [3]

    def test_exercise_credential_canary(self):
        """Exercise: Track credential-like canaries in intercepted traffic."""
        tracker = TaintTracker()
        frame = TrafficFrame(
            "ex_canary_01",
            "http",
            "10.0.0.1",
            "10.0.0.2",
            "inbound",
            {"auth_header": "Bearer CANARY_SECRET_AUTH_9999"},
            Provenance.INTERCEPTED_NETWORK,
            TaintLevel.HIGH,
            "CANARY_SECRET"
        )
        fields = tracker.parse_frame(frame)
        assert any(f.taint == TaintLevel.HIGH for f in fields)
        assert any("_INJECTION" in f.name for f in fields)

    def test_exercise_taint_propagation(self):
        """Exercise: Propagate taint through transformations to action guard."""
        guard = ActionGuard(max_taint_for_action=TaintLevel.LOW)
        # High taint is blocked for privileged action
        allowed_high, reason = guard.authorize("store_token", TaintLevel.HIGH, "tok_123", Provenance.INTERCEPTED_NETWORK)
        assert allowed_high is False
        assert "taint_too_high" in reason

        # Low taint is authorized
        allowed_low, _ = guard.authorize("log_observation", TaintLevel.LOW, "status_ok", Provenance.TRUSTED_LOCAL)
        assert allowed_low is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])