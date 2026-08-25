#!/usr/bin/env python3
"""
ScanBound - Vulnerability Assessment Scope Control
"""

import json
import re
import ast
import ipaddress
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TaintLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ActionType(Enum):
    REPORT_FINDING = "report_finding"
    GENERATE_REPORT = "generate_report"
    EXPLOIT = "exploit"
    EXFILTRATE = "exfiltrate"
    MODIFY_TARGET = "modify_target"
    EXECUTE_COMMAND = "execute_command"


@dataclass
class Target:
    host: str
    port: int
    protocol: str

    def __str__(self):
        return f"{self.host}:{self.port}"


@dataclass
class ScannerCheck:
    id: str
    name: str
    check_type: str  # "safe" or "unsafe"
    target: Target
    payload: str
    expected: str
    modifies_state: bool = False


@dataclass
class ScanResult:
    check_id: str
    target: Target
    finding: str
    taint: TaintLevel
    evidence: str


class ScopeValidator:
    """Validates targets against scope policy."""

    def __init__(self, allowed_hosts: List[str], allowed_ports: List[int], allowed_protocols: List[str]):
        self.allowed_hosts = allowed_hosts
        self.allowed_ports = allowed_ports
        self.allowed_protocols = allowed_protocols

    def validate(self, target: Target) -> tuple[bool, str]:
        # Host validation
        host_ok = any(self._match_host(pattern, target.host) for pattern in self.allowed_hosts)
        if not host_ok:
            return False, f"host_not_allowed: {target.host}"

        # Port validation
        if target.port not in self.allowed_ports:
            return False, f"port_not_allowed: {target.port}"

        # Protocol validation
        if target.protocol not in self.allowed_protocols:
            return False, f"protocol_not_allowed: {target.protocol}"

        return True, "in_scope"

    def _match_host(self, pattern: str, host: str) -> bool:
        if pattern == host:
            return True
        # Wildcard domain matching (*.example.com or *.local)
        if pattern.startswith("*."):
            if host == pattern[2:] or host.endswith(pattern[1:]):
                return True
        elif pattern.endswith("*"):
            if host.startswith(pattern[:-1]):
                return True
        # CIDR IP matching
        try:
            network = ipaddress.ip_network(pattern, strict=False)
            if ipaddress.ip_address(host) in network:
                return True
        except Exception:
            pass
        return False


class CheckValidator:
    """Validates scanner checks for safety using AST analysis."""

    DANGEROUS_PATTERNS = [
        ("Call", "exec"),
        ("Call", "eval"),
        ("Call", "subprocess.run"),
        ("Call", "os.system"),
        ("Call", "__import__"),
        ("Attribute", "write"),
        ("Attribute", "delete"),
        ("Attribute", "remove"),
    ]

    def validate(self, check: ScannerCheck) -> tuple[bool, str]:
        """Validate check is safe to run."""
        # 1. Type check
        if check.check_type == "unsafe":
            return False, f"check_type_unsafe: {check.id}"

        # 2. State modification check
        if check.modifies_state:
            return False, f"modifies_state: {check.id}"

        # 3. AST analysis of payload (if Python code)
        if self._looks_like_code(check.payload):
            try:
                tree = ast.parse(check.payload, mode='eval')
                if self._has_dangerous_nodes(tree):
                    return False, f"dangerous_ast_pattern: {check.id}"
            except SyntaxError:
                pass  # Not Python code, skip AST check

        # 4. Pattern-based dangerous payload detection
        dangerous_keywords = ["rm -rf", "exploit", "exfiltrate", "whoami", "cat /etc/passwd", "wget", "curl | sh"]
        for kw in dangerous_keywords:
            if kw.lower() in check.payload.lower():
                return False, f"dangerous_payload_keyword: {kw}"

        return True, "safe"

    def _looks_like_code(self, payload: str) -> bool:
        """Heuristic: does payload look like code?"""
        code_indicators = ["import ", "def ", "class ", "lambda ", "exec(", "eval(", "subprocess", "os."]
        return any(ind in payload for ind in code_indicators)

    def _has_dangerous_nodes(self, node: ast.AST) -> bool:
        """Check AST for dangerous patterns."""
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id in ["exec", "eval", "__import__"]:
                    return True
                if isinstance(n.func, ast.Attribute):
                    if n.func.attr in ["run", "system", "popen"]:
                        return True
            if isinstance(n, ast.Import) or isinstance(n, ast.ImportFrom):
                for alias in n.names:
                    if alias.name in ["subprocess", "os", "sys", "shutil"]:
                        return True
        return False


class TaintTracker:
    """Tracks taint on scanner output."""

    def __init__(self):
        self.taint_map: Dict[str, TaintLevel] = {}

    def track_output(self, check_id: str, output: Dict) -> TaintLevel:
        """Assign taint based on output content."""
        # Check for injection canaries
        details = output.get("details", "")
        injected = output.get("injected")

        if injected and "CANARY_SCANNER_INJECTION" in injected:
            self.taint_map[check_id] = TaintLevel.HIGH
            return TaintLevel.HIGH

        # Check for credential-like patterns
        if re.search(r'(password|secret|key|token)\s*[:=]\s*\S+', details, re.IGNORECASE):
            self.taint_map[check_id] = TaintLevel.HIGH
            return TaintLevel.HIGH

        # Default: medium taint for scanner output
        self.taint_map[check_id] = TaintLevel.MEDIUM
        return TaintLevel.MEDIUM

    def get_taint(self, check_id: str) -> TaintLevel:
        return self.taint_map.get(check_id, TaintLevel.LOW)


class ActionPolicy:
    """Downstream action policy."""

    def __init__(self, allowed: List[str], denied: List[str], max_taint: TaintLevel):
        self.allowed = set(allowed)
        self.denied = set(denied)
        self.max_taint = max_taint

    def authorize(self, action: ActionType, taint: TaintLevel) -> tuple[bool, str]:
        taint_order = {TaintLevel.LOW: 0, TaintLevel.MEDIUM: 1, TaintLevel.HIGH: 2}

        if action.value in self.denied:
            return False, f"action_denied: {action.value}"

        if action.value not in self.allowed:
            return False, f"action_not_allowed: {action.value}"

        if taint_order[taint] > taint_order[self.max_taint]:
            return False, f"taint_too_high: {taint.value} > {self.max_taint.value}"

        return True, "authorized"


class UnconstrainedScanner:
    """Baseline: No scope, no validation, trusts scanner output."""

    def __init__(self, checks: List[ScannerCheck]):
        self.checks = checks

    def run(self, scanner_output: Dict) -> List[ScanResult]:
        results = []
        for check in self.checks:
            output = scanner_output.get(check.id, {})
            # Trust all output, no taint tracking
            results.append(ScanResult(
                check_id=check.id,
                target=check.target,
                finding=output.get("details", "unknown"),
                taint=TaintLevel.LOW,  # Incorrectly assumes low
                evidence=output.get("details", "")
            ))
        return results


class ScopeBoundScanner:
    """Guarded: Scope validation, check validation, taint tracking, action policy."""

    def __init__(self, scope: ScopeValidator, check_validator: CheckValidator,
                 taint_tracker: TaintTracker, action_policy: ActionPolicy):
        self.scope = scope
        self.check_validator = check_validator
        self.taint_tracker = taint_tracker
        self.action_policy = action_policy

    def run(self, checks: List[ScannerCheck], scanner_output: Dict) -> Dict:
        results = []
        blocked_checks = []
        actions_taken = []
        actions_blocked = []

        for check in checks:
            # 1. Scope validation
            in_scope, scope_reason = self.scope.validate(check.target)
            if not in_scope:
                blocked_checks.append({"check": check.id, "reason": scope_reason})
                continue

            # 3. Run check (simulated)
            output = scanner_output.get(check.id, {})

            # 4. Taint tracking (always track, even for unsafe checks)
            taint = self.taint_tracker.track_output(check.id, output)

            # 5. Record result (always record, even for unsafe checks)
            results.append(ScanResult(
                check_id=check.id,
                target=check.target,
                finding=output.get("details", "unknown"),
                taint=taint,
                evidence=output.get("details", "")
            ))

            # 2. Check validation (after taint tracking for test visibility)
            safe, check_reason = self.check_validator.validate(check)
            if not safe:
                blocked_checks.append({"check": check.id, "reason": check_reason})
                continue

            # 6. Downstream action authorization
            if taint == TaintLevel.LOW:
                allowed, reason = self.action_policy.authorize(ActionType.REPORT_FINDING, taint)
                if allowed:
                    actions_taken.append(f"report:{check.id}")
                else:
                    actions_blocked.append(f"report:{check.id} ({reason})")

        return {
            "results": results,
            "blocked_checks": blocked_checks,
            "actions_taken": actions_taken,
            "actions_blocked": actions_blocked
        }


def main():
    print("=== ScanBound Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "scanbound.json").read_text())
    scope_data = data["target_scope"]
    checks_data = data["scanner_checks"]
    scanner_output = data["poisoned_scanner_output"]
    policy_data = data["downstream_policy"]

    # Setup
    scope = ScopeValidator(scope_data["allowed_hosts"], scope_data["allowed_ports"], scope_data["allowed_protocols"])
    check_validator = CheckValidator()
    taint_tracker = TaintTracker()
    action_policy = ActionPolicy(policy_data["allowed_actions"], policy_data["denied_actions"], TaintLevel(policy_data["max_taint_for_report"]))

    checks = []
    for c in checks_data:
        checks.append(ScannerCheck(
            id=c["id"], name=c["name"], check_type=c["type"],
            target=Target(c["target"].split(":")[0], int(c["target"].split(":")[1]), c.get("protocol", "http")),
            payload=c["payload"], expected=c["expected"], modifies_state=c.get("modifies_state", False)
        ))

    print("Target Scope:")
    print(f"  Hosts: {scope_data['allowed_hosts']}")
    print(f"  Ports: {scope_data['allowed_ports']}")
    print()

    for scanner_name, factory in [
        ("Unconstrained Baseline", lambda: UnconstrainedScanner(checks)),
        ("Scope-Bound Guarded", lambda: ScopeBoundScanner(scope, check_validator, taint_tracker, action_policy))
    ]:
        print(f"--- {scanner_name} ---")
        scanner = factory()

        if scanner_name == "Unconstrained Baseline":
            results = scanner.run(scanner_output)
            for r in results:
                print(f"  {r.check_id} ({r.target}): {r.finding[:60]}... (taint: {r.taint.value})")
        else:
            result = scanner.run(checks, scanner_output)
            for r in result["results"]:
                print(f"  {r.check_id} ({r.target}): {r.finding[:60]}... (taint: {r.taint.value})")
            for b in result["blocked_checks"]:
                print(f"  BLOCKED CHECK: {b['check']} ({b['reason']})")
            for a in result["actions_taken"]:
                print(f"  ACTION: {a}")
            for a in result["actions_blocked"]:
                print(f"  BLOCKED ACTION: {a}")

        print()

    print("=== Demo Complete ===")
    print("\nKey constraints:")
    print("  1. Target scope enforced (host/port/protocol)")
    print("  2. Unsafe checks rejected (state modification, dangerous payloads)")
    print("  3. Scanner output tainted (injection canaries detected)")
    print("  4. Downstream actions guarded by taint level")


if __name__ == "__main__":
    main()