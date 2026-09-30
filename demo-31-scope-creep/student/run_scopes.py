#!/usr/bin/env python3
"""Evaluator for Demo 31.

Flags over-privileged integrations and computes the least-privilege
scope set over eight synthetic integrations.

Writes results/scopes.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from scopes import check_all, least_privilege, overprivileged  # noqa: E402


def main() -> dict:
    """Evaluate scopes, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "integrations.json").read_text())
    integrations = pack["integrations"]
    summary = check_all(integrations)
    least = least_privilege(integrations)
    rows = []
    for integration in sorted(integrations, key=lambda i: i["id"]):
        rows.append(
            {
                "id": integration["id"],
                "overprivileged": overprivileged(integration),
                "requested": integration["requested"],
                "used": integration["used"],
            }
        )
    out = {
        "demo": "demo-31-scope-creep",
        "experiment": "scope-creep",
        "seed": pack["seed"],
        "total": len(integrations),
        "overprivileged": len(summary["over"]),
        "overprivileged_ids": summary["over"],
        "least_privilege": least,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "scopes.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("id   over  requested>used")
    for row in rows:
        print(f"{row['id']}   {str(row['overprivileged']):<5}  {len(row['requested'])}>{len(row['used'])}")
    print(f"over-privileged {len(summary['over'])}/{len(integrations)}  least-privilege {len(least)} scopes")
    print(f"least: {','.join(least)}")
    return out


if __name__ == "__main__":
    main()
