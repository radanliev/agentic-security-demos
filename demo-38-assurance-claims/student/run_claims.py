#!/usr/bin/env python3
"""Evaluator for Demo 38.

Codes the eight synthetic system cards against five assurance obligations
and reports the coverage table.

Writes results/claims.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from claims import coverage  # noqa: E402


def main() -> dict:
    """Code the fixture cards, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "cards8.json").read_text())
    cov = coverage(pack["cards"], pack["obligations"])
    out = {
        "demo": "demo-38-assurance-claims",
        "experiment": "assurance-coverage",
        "seed": pack["seed"],
        "obligations": pack["obligations"],
        "coverage": cov,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "claims.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"cards {cov['n']}  obligations {len(pack['obligations'])}")
    print("obligation    covered")
    for ob in pack["obligations"]:
        print(f"{ob:<13} {cov['per_obligation'][ob]}/{cov['n']}")
    print(f"full coverage {cov['full_coverage']}/{cov['n']}")
    print(f"weakest: {cov['weakest']} ({cov['weakest_count']}/{cov['n']}).")
    return out


if __name__ == "__main__":
    main()
