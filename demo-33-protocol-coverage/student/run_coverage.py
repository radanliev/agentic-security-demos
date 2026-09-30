#!/usr/bin/env python3
"""Evaluator for Demo 33.

Maps six synthetic protocol elements to their coverage gaps.

Writes results/coverage.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from coverage import covered, gaps  # noqa: E402


def main() -> dict:
    """Map coverage, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "elements.json").read_text())
    elements = pack["elements"]
    gap_ids = gaps(elements)
    covered_ids = covered(elements)
    out = {
        "demo": "demo-33-protocol-coverage",
        "experiment": "protocol-coverage",
        "seed": pack["seed"],
        "total": len(elements),
        "gaps": len(gap_ids),
        "gap_ids": gap_ids,
        "covered_ids": covered_ids,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "coverage.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("element       mitigation  attack  gap")
    for element in sorted(elements, key=lambda e: e["id"]):
        is_gap = element["id"] in gap_ids
        print(f"{element['id']:<13} {str(element['stated_mitigation']):<11} {str(element['known_attack']):<7} {str(is_gap)}")
    print(f"gaps {len(gap_ids)}/{len(elements)}: {','.join(gap_ids)}")
    return out


if __name__ == "__main__":
    main()
