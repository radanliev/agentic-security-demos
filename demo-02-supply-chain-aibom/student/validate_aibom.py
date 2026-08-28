#!/usr/bin/env python3
"""
GitHub Actions Compatible Validation Script

Validates ONE observed runtime capability set against the AIBOM policy:

  python3 student/validate_aibom.py --scenario drifted-002      # runtime caps taken from a fixture scenario
  python3 student/validate_aibom.py --runtime observed.json     # {"runtime_capabilities": [...], "waiver": {...}?}
  python3 student/validate_aibom.py --self-test                 # every fixture scenario behaves as its `expected` label

Exit codes: 0 = compliant, 1 = non-compliant (drift not covered by policy or a valid waiver), 2 = error
With --self-test: 0 = every scenario matched its expected label, 1 = a scenario did not, 2 = error.

The clock defaults to the fixture's `evaluation_time` (reproducible); pass
`--now now` to use the real clock, or `--now 2025-06-01T00:00:00Z`.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Add student module to path
base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from policy_gate import PolicyGate, outcome_matches, parse_time, waiver_from_scenario  # noqa: E402

DEFAULT_AIBOM = base_dir / "fixtures" / "aibom.json"


def resolve_now(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None                      # fixture evaluation_time, else real clock
    if value == "now":
        return datetime.now(timezone.utc)
    return parse_time(value)


def self_test(gate: PolicyGate, data: dict, now: Optional[datetime]) -> int:
    mismatches = 0
    for scenario in data["drift_scenarios"]:
        result = gate.evaluate_system(scenario["runtime_capabilities"], waiver_from_scenario(scenario), now)
        if not outcome_matches(scenario["expected"], result):
            print(f"UNEXPECTED: {scenario['id']} expected {scenario['expected']} but got "
                  f"compliant={result['compliant']} drift={result['drift_detected']}")
            mismatches += 1
    total = len(data["drift_scenarios"])
    print(f"self-test: {total - mismatches}/{total} scenarios behave as their expected label")
    return 1 if mismatches else 0


def validate_runtime(gate: PolicyGate, label: str, runtime: dict, now: Optional[datetime]) -> int:
    result = gate.evaluate_system(runtime["runtime_capabilities"], waiver_from_scenario(runtime), now)
    denied = [c for c in result["checks"] if not c["allowed"]]
    for c in denied:
        print(f"DENY: {c['capability']} ({c['reason']})")
    if result["drift_detected"]:
        print(f"drift: undeclared capabilities {result['undeclared_capabilities']}")
    if "waiver" in result and not result["waiver"]["accepted"]:
        print(f"waiver {result['waiver']['scope']} rejected: {'; '.join(result['waiver']['reasons'])}")
    verdict = "COMPLIANT" if result["compliant"] else "NON-COMPLIANT"
    print(f"{label}: {verdict} (evaluated at {result['evaluated_at']})")
    return 0 if result["compliant"] else 1


def validate_aibom(argv: Optional[list] = None) -> int:
    """Validate AIBOM compliance. Returns exit code."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--aibom", default=str(DEFAULT_AIBOM), help="AIBOM + policy JSON")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--scenario", help="fixture scenario id whose runtime capabilities are validated")
    mode.add_argument("--runtime", help="JSON file with observed runtime_capabilities (and optional waiver)")
    mode.add_argument("--self-test", action="store_true",
                      help="check every fixture scenario against its expected label (default)")
    parser.add_argument("--now", default=None, help="'now' for the real clock, or an ISO-8601 time")
    args = parser.parse_args(argv)

    try:
        aibom_path = Path(args.aibom)
        gate = PolicyGate(aibom_path)
        data = json.loads(aibom_path.read_text())
        now = resolve_now(args.now)

        if args.scenario:
            scenario = next((s for s in data["drift_scenarios"] if s["id"] == args.scenario), None)
            if scenario is None:
                print(f"ERROR: no scenario {args.scenario!r} in {aibom_path}")
                return 2
            return validate_runtime(gate, args.scenario, scenario, now)

        if args.runtime:
            runtime = json.loads(Path(args.runtime).read_text())
            return validate_runtime(gate, args.runtime, runtime, now)

        return self_test(gate, data, now)

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(validate_aibom())
