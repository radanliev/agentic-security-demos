#!/usr/bin/env python3
"""Evaluator for Demo 39.

Tallies the synthetic incident fixture into its top attack pattern and
scores the static control catalogue.

Writes results/taxonomy.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from taxonomy import supported_controls, top_pattern  # noqa: E402


def main() -> dict:
    """Tally incidents and controls, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "incidents.json").read_text())
    top = top_pattern(pack["incidents"])
    ctrls = supported_controls(pack["controls"])
    out = {
        "demo": "demo-39-incident-taxonomy",
        "experiment": "incident-tally",
        "seed": pack["seed"],
        "top_pattern": top,
        "controls": ctrls,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "taxonomy.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"incidents {top['n']}  controls {ctrls['n']}")
    print("pattern               count")
    for pattern in sorted(top["counts"]):
        print(f"{pattern:<21} {top['counts'][pattern]}/{top['n']}")
    print(f"top pattern: {top['pattern']} ({top['count']}/{top['n']})")
    print(f"supported controls: {ctrls['supported']}/{ctrls['n']}.")
    return out


if __name__ == "__main__":
    main()
