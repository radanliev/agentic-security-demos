#!/usr/bin/env python3
"""Evaluator for Demo 31.

Flags integrations with a declaration gap and computes the least-declaration
authority set over eight synthetic integrations.

Writes results/declarations.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from declarations import check_all, least_declaration, gapped  # noqa: E402


def main() -> dict:
    """Evaluate declarations, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "declarations.json").read_text())
    integrations = pack["integrations"]
    summary = check_all(integrations)
    least = least_declaration(integrations)
    rows = []
    for integration in sorted(integrations, key=lambda i: i["id"]):
        rows.append(
            {
                "id": integration["id"],
                "gapped": gapped(integration),
                "declared": integration["declared"],
                "exercised": integration["exercised"],
            }
        )
    out = {
        "demo": "demo-31-declaration-gap",
        "experiment": "declaration-gap",
        "seed": pack["seed"],
        "total": len(integrations),
        "gapped": len(summary["over"]),
        "gapped_ids": summary["over"],
        "least_declaration": least,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "declarations.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("id   gap   declared>exercised")
    for row in rows:
        print(f"{row['id']}   {str(row['gapped']):<5}  {len(row['declared'])}>{len(row['exercised'])}")
    print(f"gapped {len(summary['over'])}/{len(integrations)}  least-declaration {len(least)} authority items")
    print(f"least: {','.join(least)}")
    return out


if __name__ == "__main__":
    main()
