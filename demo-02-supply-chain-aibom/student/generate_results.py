#!/usr/bin/env python3
"""Generate drift results for demo-02."""

import json
from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from policy_gate import PolicyGate, Waiver

def main():
    gate = PolicyGate(base_dir / "fixtures" / "aibom.json")
    scenarios = json.loads((base_dir / "fixtures" / "aibom.json").read_text())["drift_scenarios"]
    results = []
    for s in scenarios:
        waiver = None
        if "waiver" in s:
            w = s["waiver"]
            waiver = Waiver(w["scope"], w["justification"], w["approved"], w["expires"])
        r = gate.evaluate_system(s["runtime_capabilities"], waiver)
        results.append({"scenario": s["id"], "expected": s["expected"], "compliant": r["compliant"]})

    output = {
        "demo": "demo-02-supply-chain-aibom",
        "experiment": "drift_detection",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=02",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "scenarios": results
    }
    out_path = base_dir / "results" / "drift_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()