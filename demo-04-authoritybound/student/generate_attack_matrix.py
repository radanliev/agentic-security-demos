#!/usr/bin/env python3
"""Generate attack matrix for demo-04."""

import json
from pathlib import Path
import sys
base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from authoritybound import (
    create_baseline_agent, create_provenance_aware_agent, create_scope_bound_agent, Provenance
)

def main():
    data = json.loads((base_dir / "fixtures" / "authoritybound.json").read_text())
    agents = {
        "baseline": create_baseline_agent(),
        "provenance": create_provenance_aware_agent(),
        "scope": create_scope_bound_agent()
    }

    matrix = {}
    for name, agent in agents.items():
        matrix[name] = {}
        for s in data["scenarios"]:
            prov = Provenance(s["provenance"])
            r = agent.process(s["input"], prov)
            matrix[name][s["id"]] = {t["tool"]: t["status"] for t in r["results"]}

    out = {
        "demo": "demo-04-authoritybound",
        "experiment": "attack_matrix",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=04",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "matrix": matrix
    }
    out_path = base_dir / "results" / "attack_matrix.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()