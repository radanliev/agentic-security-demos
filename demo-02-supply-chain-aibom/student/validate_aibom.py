#!/usr/bin/env python3
"""
GitHub Actions Compatible Validation Script
Exit codes: 0 = compliant, 1 = drift detected, 2 = error
"""

import json
import sys
from pathlib import Path

# Add student module to path
sys.path.insert(0, str(Path(__file__).parent / "student"))
from policy_gate import PolicyGate, Waiver


def validate_aibom(aibom_path: str = "fixtures/aibom.json") -> int:
    """Validate AIBOM compliance. Returns exit code."""
    try:
        gate = PolicyGate(Path(aibom_path))
        scenarios = json.loads(Path(aibom_path).read_text())["drift_scenarios"]

        # In real CI, you'd check the actual runtime capabilities here
        # For demo, we test all scenarios and fail if any unexpected drift
        has_unexpected_drift = False

        for scenario in scenarios:
            waiver = None
            if "waiver" in scenario:
                w = scenario["waiver"]
                waiver = Waiver(w["scope"], w["justification"], w["approved"], w["expires"])

            result = gate.evaluate_system(scenario["runtime_capabilities"], waiver)

            expected = scenario["expected"]
            matches = (
                (expected == "pass" and result["compliant"]) or
                (expected == "block" and not result["compliant"]) or
                (expected == "reject_waiver" and not result["compliant"]) or
                (expected == "accept_waiver" and result["compliant"])
            )

            if not matches:
                print(f"UNEXPECTED: {scenario['id']} expected {expected} but got compliant={result['compliant']}")
                has_unexpected_drift = True

        if has_unexpected_drift:
            return 1
        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(validate_aibom())