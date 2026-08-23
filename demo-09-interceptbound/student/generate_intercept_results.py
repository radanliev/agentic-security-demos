#!/usr/bin/env python3
"""Generate intercept results for demo-09."""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "student"))
from interceptbound import TaintAwareAgent, TrafficFrame, Provenance, TaintLevel

def main():
    data = json.loads(Path("fixtures/traffic.json").read_text())
    scope = data["scope_policy"]
    buffer_config = data["ephemeral_buffer"]
    frames = [TrafficFrame(f["id"], f["protocol"], f["src"], f["dst"], f["direction"], f["fields"],
                 Provenance(f["provenance"]), TaintLevel(f["taint"]), f["injection"]) for f in data["traffic_frames"]]
    agent = TaintAwareAgent(scope, buffer_config)
    results = []
    for frame in frames:
        r = agent.process(frame)
        results.append({"frame": frame.id, "actions": r.get("actions", []), "blocked": r.get("blocked", [])})

    out = {
        "demo": "demo-09-interceptbound",
        "experiment": "taint_tracking",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=09",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "results": results
    }

    Path("results/intercept_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()