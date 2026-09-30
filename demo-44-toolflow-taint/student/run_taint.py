#!/usr/bin/env python3
"""Evaluator for Demo 44.

Reports unlabelled toolflow edges reaching sensitive sinks.

Writes results/taint.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from taint import unlabelled_to_sensitive  # noqa: E402


def main() -> dict:
    """Find tainted flows, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "edges.json").read_text())
    flows = pack["flows"]
    bad = unlabelled_to_sensitive(flows)
    out = {
        "demo": "demo-44-toolflow-taint",
        "experiment": "toolflow-taint",
        "seed": pack["seed"],
        "n": len(flows),
        "n_unlabelled_sensitive": len(bad),
        "flow_ids": bad,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "taint.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"flows {len(flows)}  sensitive sinks code/shell/file/network/memory")
    print("id     sink     provenance")
    for f in flows:
        print(f"{f['id']:<6} {f['sink']:<8} {f['provenance']}")
    print(f"unlabelled to sensitive: {len(bad)}/{len(flows)} ({', '.join(bad)}).")
    return out


if __name__ == "__main__":
    main()
