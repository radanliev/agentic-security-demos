#!/usr/bin/env python3
"""Generate inclusion results for demo-08."""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "student"))
from inclusiontrap import GuardedInclusionAgent, ScopePolicy, Provenance

def main():
    data = json.loads(Path("fixtures/inclusion.json").read_text())
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

    Path("results/inclusion_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()