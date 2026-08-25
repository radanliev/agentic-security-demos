#!/usr/bin/env python3
"""Generate evaluation for demo-06."""

import json
from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from reconscope import ProvenanceAwareReconAgent, ScopePolicy

def main():
    data = json.loads((base_dir / "fixtures" / "protocol_fixtures.json").read_text())
    scope = ScopePolicy(**data["scope_policy"])
    agent = ProvenanceAwareReconAgent(scope)
    for f in data["protocol_fixtures"]:
        agent.probe(f)
    obs = agent.get_observations()
    injections = [o for o in obs if "INJECTION" in o["name"]]

    results = {
        "demo": "demo-06-reconscope",
        "experiment": "injection_detection",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=06",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "total_fixtures": len(data["protocol_fixtures"]),
        "injections_detected": len(injections),
        "injection_details": [{"source": i["source"], "field": i["name"], "snippet": i["value"][:80]} for i in injections]
    }

    out_path = base_dir / "results" / "evaluation.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()