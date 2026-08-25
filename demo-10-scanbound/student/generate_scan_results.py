#!/usr/bin/env python3
"""Generate scan results for demo-10."""

import json
from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from scanbound import (
    Target, ScannerCheck, ScopeValidator, CheckValidator,
    TaintTracker, ActionPolicy, ScopeBoundScanner, TaintLevel, ActionType
)

def main():
    data = json.loads((base_dir / "fixtures" / "scanbound.json").read_text())
    scope = ScopeValidator(data["target_scope"]["allowed_hosts"], data["target_scope"]["allowed_ports"], data["target_scope"]["allowed_protocols"])
    check_validator = CheckValidator()
    taint_tracker = TaintTracker()
    action_policy = ActionPolicy(data["downstream_policy"]["allowed_actions"], data["downstream_policy"]["denied_actions"], TaintLevel(data["downstream_policy"]["max_taint_for_report"]))
    checks = [ScannerCheck(c["id"], c["name"], c["type"], Target(c["target"].split(":")[0], int(c["target"].split(":")[1]), c.get("protocol","http")), c["payload"], c["expected"], c.get("modifies_state", False)) for c in data["scanner_checks"]]
    scanner = ScopeBoundScanner(scope, check_validator, taint_tracker, action_policy)
    result = scanner.run(checks, data["poisoned_scanner_output"])

    out = {
        "demo": "demo-10-scanbound",
        "experiment": "scope_control",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=10",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "results": [{"check": r.check_id, "target": str(r.target), "finding": r.finding[:80], "taint": r.taint.value} for r in result["results"]],
        "blocked_checks": result["blocked_checks"],
        "actions_taken": result["actions_taken"],
        "actions_blocked": result["actions_blocked"]
    }

    out_path = base_dir / "results" / "scan_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()