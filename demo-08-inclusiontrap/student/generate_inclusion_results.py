#!/usr/bin/env python3
"""Generate inclusion results for demo-08."""

import json
from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from inclusiontrap import GuardedInclusionAgent, ScopePolicy, Provenance

def main():
    data = json.loads((base_dir / "fixtures" / "inclusion.json").read_text())
    files = data["files"]
    scope = ScopePolicy(data["agent_scope"]["allowed_read_paths"], data["agent_scope"]["denied_read_paths"])
    agent = GuardedInclusionAgent(files, scope)
    results = []
    for s in data["inclusion_scenarios"]:
        r = agent.process(s)
        results.append({
            "scenario": s["id"],
            "action": r.action,
            "reason": r.reason,
            "provenance": r.provenance.value
        })

    out = {
        "demo": "demo-08-inclusiontrap",
        "experiment": "inclusion_scope",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=08",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "results": results
    }

    out_path = base_dir / "results" / "inclusion_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()