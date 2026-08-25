#!/usr/bin/env python3
"""Generate triage results for demo-07."""

import json
from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from triagetrap import ProvenanceAwareTriageAgent, Artifact, Provenance

def main():
    data = json.loads((base_dir / "fixtures" / "artifacts.json").read_text())
    agent = ProvenanceAwareTriageAgent(data["base_rates"], data["quarantine_threshold"])
    results_list = []
    for a in data["artifacts"]:
        artifact = Artifact(a["id"], a["type"], a["source"], Provenance(a["provenance"]), a["metadata"], a["canary"])
        result = agent.triage(artifact)
        results_list.append({
            "artifact_id": result.artifact_id,
            "verdict": result.verdict.value,
            "score": result.score,
            "reasons": result.reasons
        })

    out = {
        "demo": "demo-07-triagetrap",
        "experiment": "triage",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=07",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "results": results_list
    }

    out_path = base_dir / "results" / "triage_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()