#!/usr/bin/env python3
"""
AIBOM Drift Detector - Policy Gate Implementation

Two questions are answered separately for every runtime capability set:

  drift      -- does the runtime use anything the AIBOM does not DECLARE?
  compliance -- is every runtime capability PERMITTED by the policy
                (allow list, or a waiver the waiver_rules sanction)?

A waiver can make drift *compliant* (it is an approved, time-limited
exception); it never makes the drift disappear from the report.

Decision order per capability (fail-closed):
  explicit allow -> valid waiver (only for waivable scopes) -> explicit deny -> default deny
"""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set


def parse_time(value: str) -> datetime:
    """Parse an ISO-8601 timestamp; naive values are treated as UTC."""
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def expand_capability(cap: str) -> List[str]:
    """Split a composite tool capability into one capability per tool.

    'exec:tools:parser,validator' -> ['exec:tools:parser', 'exec:tools:validator']
    Every other capability string is returned unchanged. This keeps matching
    per-tool, so a runtime with FEWER tools than declared is not flagged as
    drift, and an extra tool is caught individually.
    """
    prefix = "exec:tools:"
    if cap.startswith(prefix) and "," in cap:
        return [prefix + tool.strip() for tool in cap[len(prefix):].split(",") if tool.strip()]
    return [cap]


def match_pattern(pattern: str, cap: str) -> bool:
    """Simple glob-style matching: a trailing '*' is a prefix wildcard, otherwise exact."""
    if pattern.endswith("*"):
        return cap.startswith(pattern[:-1])
    return pattern == cap


@dataclass
class Waiver:
    scope: str
    justification: str
    approved: bool
    expires: str                    # ISO-8601
    issued: Optional[str] = None    # ISO-8601; required so the duration can be checked
    approved_by: str = ""           # who approved it (recorded, not cryptographically signed)

    def validate(self, rules: Optional[Dict] = None, now: Optional[datetime] = None) -> List[str]:
        """Return every reason this waiver must be rejected (empty list = valid).

        Intrinsic checks (approval, timestamps) always run. Policy checks
        (max duration, waivable scopes, whether approval is required) run
        when the policy's waiver_rules are supplied.
        """
        rules = rules or {}
        now = now or datetime.now(timezone.utc)
        reasons: List[str] = []

        if rules.get("requires_approval", True):
            if not self.approved:
                reasons.append("not approved")
            elif not self.approved_by:
                reasons.append("approved flag set but no approver recorded")

        try:
            expires = parse_time(self.expires)
        except (TypeError, ValueError):
            return reasons + ["unparseable expiry"]
        if now >= expires:
            reasons.append(f"expired at {self.expires}")

        if self.issued is None:
            reasons.append("no issue timestamp, duration cannot be checked")
        else:
            try:
                issued = parse_time(self.issued)
            except (TypeError, ValueError):
                return reasons + ["unparseable issue timestamp"]
            if issued > now:
                reasons.append(f"not in force until {self.issued}")
            max_hours = rules.get("max_duration_hours")
            if max_hours is not None and expires - issued > timedelta(hours=max_hours):
                reasons.append(f"duration exceeds max_duration_hours={max_hours}")

        if "allowed_scopes" in rules and not any(match_pattern(s, self.scope) for s in rules["allowed_scopes"]):
            reasons.append(f"scope {self.scope} is not waivable")

        return reasons

    def is_valid(self, rules: Optional[Dict] = None, now: Optional[datetime] = None) -> bool:
        return not self.validate(rules, now)


class PolicyGate:
    """Fail-closed policy gate for AIBOM drift detection."""

    def __init__(self, aibom_path: Path):
        data = json.loads(aibom_path.read_text())
        aibom = data["aibom"]
        self.declared_caps: Set[str] = self._expand_all(aibom["agent_capabilities"])
        self.allowed: Set[str] = self._expand_all(aibom["policy"]["allowed_capabilities"])
        self.denied: Set[str] = self._expand_all(aibom["policy"]["denied_capabilities"])
        self.waiver_rules: Dict = aibom["policy"]["waiver_rules"]
        # Optional fixed clock so the fixture evaluates identically on every run.
        self.evaluation_time: Optional[datetime] = (
            parse_time(data["evaluation_time"]) if data.get("evaluation_time") else None)

    @staticmethod
    def _expand_all(caps: List[str]) -> Set[str]:
        return {c for cap in caps for c in expand_capability(cap)}

    def _matches(self, patterns: Set[str], cap: str) -> bool:
        return any(match_pattern(p, cap) for p in patterns)

    def check_capability(self, cap: str, waiver: Optional[Waiver] = None,
                         now: Optional[datetime] = None) -> Dict:
        """Check whether one (already expanded) capability is permitted."""
        # 1. Explicit allow
        if self._matches(self.allowed, cap):
            return {"allowed": True, "reason": "explicitly_allowed", "capability": cap}

        # 2. Valid waiver covering this capability (waiver_rules enforced inside validate)
        if waiver and match_pattern(waiver.scope, cap) and waiver.is_valid(self.waiver_rules, now):
            return {"allowed": True, "reason": "waiver_granted", "capability": cap,
                    "waiver_scope": waiver.scope}

        # 3. Explicit deny (exact matches and wildcards)
        if self._matches(self.denied, cap):
            return {"allowed": False, "reason": "explicitly_denied", "capability": cap}

        # 4. Default deny (fail-closed)
        return {"allowed": False, "reason": "not_allowed_default_deny", "capability": cap}

    def evaluate_system(self, runtime_caps: List[str], waiver: Optional[Waiver] = None,
                        now: Optional[datetime] = None) -> Dict:
        """Evaluate an entire runtime capability set: drift AND compliance."""
        now = now or self.evaluation_time or datetime.now(timezone.utc)
        caps = [c for cap in runtime_caps for c in expand_capability(cap)]

        checks = [self.check_capability(cap, waiver, now) for cap in caps]
        undeclared = [cap for cap in caps if not self._matches(self.declared_caps, cap)]

        result = {
            "evaluated_at": now.isoformat(),
            "compliant": all(c["allowed"] for c in checks),
            "drift_detected": bool(undeclared),
            "undeclared_capabilities": undeclared,
            "checks": checks,
        }
        if waiver is not None:
            reasons = waiver.validate(self.waiver_rules, now)
            result["waiver"] = {"scope": waiver.scope, "accepted": not reasons, "reasons": reasons}
        return result


def outcome_matches(expected: str, result: Dict) -> bool:
    """Does a gate result satisfy a scenario's `expected` label?"""
    waiver = result.get("waiver")
    if expected == "pass":
        return result["compliant"] and not result["drift_detected"]
    if expected == "block":
        return not result["compliant"]
    if expected == "reject_waiver":
        return not result["compliant"] and waiver is not None and not waiver["accepted"]
    if expected == "accept_waiver":
        return result["compliant"] and waiver is not None and waiver["accepted"]
    return False


def waiver_from_scenario(scenario: Dict) -> Optional[Waiver]:
    if "waiver" not in scenario:
        return None
    w = scenario["waiver"]
    return Waiver(w["scope"], w["justification"], w["approved"], w["expires"],
                  w.get("issued"), w.get("approved_by", ""))


def main():
    base_dir = Path(__file__).resolve().parent.parent
    aibom_path = base_dir / "fixtures" / "aibom.json"
    gate = PolicyGate(aibom_path)
    data = json.loads(aibom_path.read_text())

    print(f"Declared capabilities (AIBOM): {sorted(gate.declared_caps)}")
    if gate.evaluation_time:
        print(f"Evaluation time: {data['evaluation_time']} (fixed by the fixture for reproducibility)")

    for scenario in data["drift_scenarios"]:
        print(f"\n=== {scenario['id']}: {scenario['description']} ===")
        result = gate.evaluate_system(scenario["runtime_capabilities"], waiver_from_scenario(scenario))

        drift = result["drift_detected"]
        print(f"Drift detected: {drift}" + (f" (undeclared: {', '.join(result['undeclared_capabilities'])})" if drift else ""))
        if "waiver" in result:
            w = result["waiver"]
            verdict = "ACCEPTED" if w["accepted"] else "REJECTED: " + "; ".join(w["reasons"])
            print(f"Waiver {w['scope']}: {verdict}")
        for check in result["checks"]:
            status = "ALLOW" if check["allowed"] else "DENY"
            print(f"  {status}: {check['capability']} ({check['reason']})")
        print(f"Compliant: {result['compliant']}")

        expected = scenario["expected"]
        labels = {"pass": "PASS", "block": "BLOCKED", "reject_waiver": "WAIVER REJECTED",
                  "accept_waiver": "WAIVER ACCEPTED"}
        if outcome_matches(expected, result):
            print(f"✓ Matches expected: {labels[expected]}")
        else:
            print(f"✗ MISMATCH: expected {expected}, got compliant={result['compliant']} drift={drift}")


if __name__ == "__main__":
    main()
