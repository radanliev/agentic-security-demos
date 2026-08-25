#!/usr/bin/env python3
"""
Tests for Demo 10: ScanBound
"""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from scanbound import (
    Target, ScannerCheck, ScopeValidator, CheckValidator,
    TaintTracker, ActionPolicy, UnconstrainedScanner, ScopeBoundScanner,
    TaintLevel, ActionType
)


class TestScanBound:
    """Tests for vulnerability assessment scope control."""

    @pytest.fixture
    def data(self):
        return json.loads((DEMO_DIR / "fixtures" / "scanbound.json").read_text())

    @pytest.fixture
    def scope(self, data):
        return ScopeValidator(
            data["target_scope"]["allowed_hosts"],
            data["target_scope"]["allowed_ports"],
            data["target_scope"]["allowed_protocols"]
        )

    @pytest.fixture
    def check_validator(self):
        return CheckValidator()

    @pytest.fixture
    def taint_tracker(self):
        return TaintTracker()

    @pytest.fixture
    def action_policy(self, data):
        return ActionPolicy(
            data["downstream_policy"]["allowed_actions"],
            data["downstream_policy"]["denied_actions"],
            TaintLevel(data["downstream_policy"]["max_taint_for_report"])
        )

    @pytest.fixture
    def checks(self, data):
        checks = []
        for c in data["scanner_checks"]:
            checks.append(ScannerCheck(
                id=c["id"], name=c["name"], check_type=c["type"],
                target=Target(c["target"].split(":")[0], int(c["target"].split(":")[1]), c.get("protocol", "http")),
                payload=c["payload"], expected=c["expected"], modifies_state=c.get("modifies_state", False)
            ))
        return checks

    @pytest.fixture
    def scanner_output(self, data):
        return data["poisoned_scanner_output"]

    def test_scope_validation(self, scope):
        """Scope validator enforces host/port/protocol."""
        assert scope.validate(Target("localhost", 8080, "http")) == (True, "in_scope")
        assert scope.validate(Target("127.0.0.1", 8443, "https")) == (True, "in_scope")
        assert scope.validate(Target("scan-target.local", 80, "http")) == (True, "in_scope")
        assert scope.validate(Target("evil.com", 80, "http"))[0] is False
        assert scope.validate(Target("localhost", 22, "ssh"))[0] is False
        assert scope.validate(Target("localhost", 8080, "ftp"))[0] is False

    def test_check_validator_safe_checks(self, check_validator):
        """Safe checks pass validation."""
        safe_check = ScannerCheck("c1", "test", "safe", Target("localhost", 8080, "http"), "GET /", "ok")
        assert check_validator.validate(safe_check)[0] is True

    def test_check_validator_unsafe_type_rejected(self, check_validator):
        """Unsafe check type rejected."""
        unsafe_check = ScannerCheck("c1", "test", "unsafe", Target("localhost", 8080, "http"), "GET /", "ok")
        valid, reason = check_validator.validate(unsafe_check)
        assert valid is False
        assert "check_type_unsafe" in reason

    def test_check_validator_state_modification_rejected(self, check_validator):
        """State-modifying checks rejected."""
        check = ScannerCheck("c1", "test", "safe", Target("localhost", 8080, "http"), "GET /", "ok", modifies_state=True)
        valid, reason = check_validator.validate(check)
        assert valid is False
        assert "modifies_state" in reason

    def test_check_validator_dangerous_payload_rejected(self, check_validator):
        """Dangerous payload keywords rejected."""
        check = ScannerCheck("c1", "test", "safe", Target("localhost", 8080, "http"), "rm -rf /", "ok")
        valid, reason = check_validator.validate(check)
        assert valid is False
        assert "dangerous_payload_keyword" in reason

    def test_check_validator_ast_detection(self, check_validator):
        """AST analysis detects dangerous Python code."""
        check = ScannerCheck("c1", "test", "safe", Target("localhost", 8080, "http"),
                           "exec('malicious')", "ok")
        valid, reason = check_validator.validate(check)
        assert valid is False
        assert "dangerous_ast_pattern" in reason

    def test_taint_tracking_injection(self, taint_tracker):
        """Injection canaries produce HIGH taint."""
        output = {"details": "test", "injected": "CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI"}
        taint = taint_tracker.track_output("check_001", output)
        assert taint == TaintLevel.HIGH

    def test_taint_tracking_credentials(self, taint_tracker):
        """Credential patterns produce HIGH taint."""
        output = {"details": "password: secret123", "injected": None}
        taint = taint_tracker.track_output("check_002", output)
        assert taint == TaintLevel.HIGH

    def test_taint_tracking_default_medium(self, taint_tracker):
        """Clean output gets MEDIUM taint."""
        output = {"details": "Server: nginx", "injected": None}
        taint = taint_tracker.track_output("check_003", output)
        assert taint == TaintLevel.MEDIUM

    def test_unconstrained_trusts_all_output(self, checks, scanner_output):
        """Unconstrained scanner trusts all output, low taint."""
        scanner = UnconstrainedScanner(checks)
        results = scanner.run(scanner_output)

        for r in results:
            assert r.taint == TaintLevel.LOW  # Incorrectly low

    def test_guarded_blocks_out_of_scope(self, checks, scanner_output, scope, check_validator, taint_tracker, action_policy):
        """Guarded scanner blocks out-of-scope targets."""
        # Add out-of-scope check
        oob_check = ScannerCheck("oob", "test", "safe", Target("evil.com", 80, "http"), "GET /", "ok")
        all_checks = checks + [oob_check]

        scanner = ScopeBoundScanner(scope, check_validator, taint_tracker, action_policy)
        result = scanner.run(all_checks, scanner_output)

        blocked = [b for b in result["blocked_checks"] if b["check"] == "oob"]
        assert len(blocked) == 1
        assert "host_not_allowed" in blocked[0]["reason"]

    def test_guarded_blocks_unsafe_checks(self, checks, scanner_output, scope, check_validator, taint_tracker, action_policy):
        """Guarded scanner blocks unsafe checks."""
        scanner = ScopeBoundScanner(scope, check_validator, taint_tracker, action_policy)
        result = scanner.run(checks, scanner_output)

        # check_003 (sql_injection) and check_004 (rce_attempt) should be blocked
        blocked_ids = [b["check"] for b in result["blocked_checks"]]
        assert "check_003" in blocked_ids
        assert "check_004" in blocked_ids

    def test_guarded_tracks_taint(self, checks, scanner_output, scope, check_validator, taint_tracker, action_policy):
        """Guarded scanner tracks taint correctly."""
        scanner = ScopeBoundScanner(scope, check_validator, taint_tracker, action_policy)
        result = scanner.run(checks, scanner_output)

        # check_001 and check_004 have injection canaries -> HIGH taint
        taints = {r.check_id: r.taint for r in result["results"]}
        assert taints["check_001"] == TaintLevel.HIGH
        assert taints["check_004"] == TaintLevel.HIGH

        # check_002, 003, 005 no injection -> MEDIUM
        assert taints["check_002"] == TaintLevel.MEDIUM
        assert taints["check_003"] == TaintLevel.MEDIUM
        assert taints["check_005"] == TaintLevel.MEDIUM

    def test_action_policy_blocks_high_taint(self, action_policy):
        """Action policy blocks high-taint actions."""
        allowed, reason = action_policy.authorize(ActionType.REPORT_FINDING, TaintLevel.HIGH)
        assert allowed is False
        assert "taint_too_high" in reason

        allowed, reason = action_policy.authorize(ActionType.REPORT_FINDING, TaintLevel.LOW)
        assert allowed is True

    def test_action_policy_blocks_denied_actions(self, action_policy):
        """Action policy blocks denied actions."""
        allowed, reason = action_policy.authorize(ActionType.EXPLOIT, TaintLevel.LOW)
        assert allowed is False
        assert "action_denied" in reason

    def test_address_ambiguity_prevented(self, scope):
        """DNS/address ambiguity prevented by explicit allowlist."""
        # Only explicit hosts allowed, no wildcard resolution
        assert scope.validate(Target("127.0.0.1", 8080, "http"))[0] is True
        assert scope.validate(Target("localhost", 8080, "http"))[0] is True
        # But not resolved names not in list
        assert scope.validate(Target("scan-target.local", 80, "http"))[0] is True


class TestExercises:
    """Exercise tests."""

    def test_exercise_scope_escape(self):
        """Exercise: Demonstrate and prevent scope escape attempts."""
        scope = ScopeValidator(["localhost", "127.0.0.1"], [80, 443], ["http", "https"])
        assert scope.validate(Target("external-host.com", 80, "http"))[0] is False
        assert scope.validate(Target("localhost", 22, "ssh"))[0] is False
        assert scope.validate(Target("127.0.0.1", 443, "https"))[0] is True

    def test_exercise_poisoned_output(self):
        """Exercise: Verify high taint assigned to poisoned scanner output."""
        tracker = TaintTracker()
        output = {"details": "password: SECRET_ADMIN_TOKEN_999", "injected": "CANARY_SCANNER_INJECTION_123"}
        taint = tracker.track_output("chk_ex_01", output)
        assert taint == TaintLevel.HIGH

    def test_exercise_unsafe_check_ast(self):
        """Exercise: AST validation rejects destructive code checks."""
        validator = CheckValidator()
        destructive_check = ScannerCheck(
            "ex_ast_01",
            "Destructive Probe",
            "code_exec",
            Target("localhost", 8080, "http"),
            "rm -rf /data",
            "safe",
            modifies_state=True
        )
        assert validator.validate(destructive_check)[0] is False

    def test_exercise_address_validation(self):
        """Exercise: Validate allowed vs forbidden address formats including wildcards and CIDRs."""
        scope = ScopeValidator(["scan-target.local", "*.internal.net", "192.168.1.0/24"], [80, 443], ["http", "https"])
        # Exact match
        assert scope.validate(Target("scan-target.local", 80, "http"))[0] is True
        # Suffix / domain escaping blocked
        assert scope.validate(Target("scan-target.local.evil.com", 80, "http"))[0] is False
        # Wildcard subdomain allowed
        assert scope.validate(Target("api.internal.net", 443, "https"))[0] is True
        # CIDR IP allowed
        assert scope.validate(Target("192.168.1.50", 80, "http"))[0] is True
        # Outside CIDR blocked
        assert scope.validate(Target("10.0.0.1", 80, "http"))[0] is False

    def test_exercise_fail_closed(self):
        """Exercise: Verify fail-closed behavior on unsafe check types."""
        validator = CheckValidator()
        unsafe_check = ScannerCheck(
            "ex_unk_01",
            "Unsafe Check",
            "unsafe",
            Target("localhost", 8080, "http"),
            "probe",
            "safe",
            modifies_state=False
        )
        assert validator.validate(unsafe_check)[0] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])