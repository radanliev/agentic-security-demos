#!/usr/bin/env python3
"""
AIBOM Drift Detector - Policy Gate Implementation
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class Waiver:
    scope: str
    justification: str
    approved: bool
    expires: str  # ISO format

    def is_valid(self) -> bool:
        if not self.approved:
            return False
        try:
            exp = datetime.fromisoformat(self.expires.replace('Z', '+00:00'))
            return datetime.now(exp.tzinfo) < exp
        except Exception:
            return False


class PolicyGate:
    """Fail-closed policy gate for AIBOM drift detection."""

    def __init__(self, aibom_path: Path):
        data = json.loads(aibom_path.read_text())
        self.declared_caps: Set[str] = set(data["aibom"]["agent_capabilities"])
        self.allowed: Set[str] = set(data["aibom"]["policy"]["allowed_capabilities"])
        self.denied: Set[str] = set(data["aibom"]["policy"]["denied_capabilities"])
        self.waiver_rules = data["aibom"]["policy"]["waiver_rules"]

    def check_capability(self, cap: str, waiver: Optional[Waiver] = None) -> Dict:
        """Check if a capability is allowed."""
        # Check explicit allow first
        if self._matches_allowed(cap):
            return {"allowed": True, "reason": "explicitly_allowed", "capability": cap}

        # Check waiver - but only for scopes allowed by waiver_rules
        if waiver and waiver.is_valid():
            if self._waiver_scope_matches(waiver.scope, cap):
                # Verify waiver scope is in allowed_scopes
                allowed_scopes = self.waiver_rules.get("allowed_scopes", [])
                if any(self._match_pattern(scope, waiver.scope) for scope in allowed_scopes):
                    return {"allowed": True, "reason": "waiver_granted", "capability": cap, "waiver_scope": waiver.scope}

        # Check explicit deny (exact matches and wildcards)
        if self._matches_denied(cap):
            return {"allowed": False, "reason": "explicitly_denied", "capability": cap}

        # Default deny (fail-closed)
        return {"allowed": False, "reason": "not_allowed_default_deny", "capability": cap}

    def _matches_allowed(self, cap: str) -> bool:
        for pattern in self.allowed:
            if self._match_pattern(pattern, cap):
                return True
        return False

    def _matches_denied(self, cap: str) -> bool:
        for pattern in self.denied:
            if self._match_pattern(pattern, cap):
                return True
        return False

    def _match_pattern(self, pattern: str, cap: str) -> bool:
        """Simple glob-style matching."""
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return cap.startswith(prefix)
        return pattern == cap

    def _waiver_scope_matches(self, waiver_scope: str, cap: str) -> bool:
        return self._match_pattern(waiver_scope, cap)

    def evaluate_system(self, runtime_caps: List[str], waiver: Optional[Waiver] = None) -> Dict:
        """Evaluate entire system capability set."""
        results = []
        all_allowed = True

        for cap in runtime_caps:
            result = self.check_capability(cap, waiver)
            results.append(result)
            if not result["allowed"]:
                all_allowed = False

        return {
            "compliant": all_allowed,
            "checks": results,
            "drift_detected": not all_allowed
        }


def main():
    base_dir = Path(__file__).resolve().parent.parent
    aibom_path = base_dir / "fixtures" / "aibom.json"
    gate = PolicyGate(aibom_path)

    scenarios = json.loads(aibom_path.read_text())["drift_scenarios"]

    for scenario in scenarios:
        print(f"\n=== {scenario['id']}: {scenario['description']} ===")

        waiver = None
        if "waiver" in scenario:
            w = scenario["waiver"]
            waiver = Waiver(w["scope"], w["justification"], w["approved"], w["expires"])

        result = gate.evaluate_system(scenario["runtime_capabilities"], waiver)

        print(f"Compliant: {result['compliant']}")
        print(f"Drift detected: {result['drift_detected']}")
        for check in result["checks"]:
            status = "ALLOW" if check["allowed"] else "DENY"
            print(f"  {status}: {check['capability']} ({check['reason']})")

        # Verify expectation
        expected = scenario["expected"]
        if expected == "pass" and result["compliant"]:
            print("✓ Matches expected: PASS")
        elif expected == "block" and not result["compliant"]:
            print("✓ Matches expected: BLOCKED")
        elif expected == "reject_waiver" and not result["compliant"]:
            print("✓ Matches expected: WAIVER REJECTED")
        elif expected == "accept_waiver" and result["compliant"]:
            print("✓ Matches expected: WAIVER ACCEPTED")
        else:
            print(f"✗ MISMATCH: expected {expected}, got compliant={result['compliant']}")


if __name__ == "__main__":
    main()