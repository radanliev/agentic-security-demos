#!/usr/bin/env python3
"""Evaluator for Demo 43.

Codes the eight synthetic platform-terms records into clause tallies.

Writes results/terms.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from terms import tally  # noqa: E402


def main() -> dict:
    """Tally clauses, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "platforms.json").read_text())
    res = tally(pack["platforms"])
    out = {
        "demo": "demo-43-terms-coding",
        "experiment": "terms-coding",
        "seed": pack["seed"],
        "tally": res,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "terms.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"platforms {res['n']}")
    print("clause                   count")
    for clause in ("disclaims_autonomy", "requires_monitoring",
                   "consent_for_delegation"):
        print(f"{clause:<24} {res['counts'][clause]}/{res['n']}")
    return out


if __name__ == "__main__":
    main()
