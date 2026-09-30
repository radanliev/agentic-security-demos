#!/usr/bin/env python3
"""Evaluator for Demo 30.

Checks ten synthetic deployment stacks for insecure defaults and
summarises how many are insecure and how many pin a vuln.

Writes results/defaults.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from checker import check_all, is_insecure  # noqa: E402


def main() -> dict:
    """Check all stacks, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "stacks.json").read_text())
    stacks = pack["stacks"]
    summary = check_all(stacks)
    rows = []
    for stack in sorted(stacks, key=lambda s: s["id"]):
        reasons = is_insecure(stack)
        rows.append(
            {
                "id": stack["id"],
                "insecure": bool(reasons),
                "reasons": reasons,
            }
        )
    out = {
        "demo": "demo-30-default-configs",
        "experiment": "insecure-defaults",
        "seed": pack["seed"],
        "total": len(stacks),
        "insecure": len(summary["insecure"]),
        "insecure_ids": summary["insecure"],
        "pinned": len(summary["pinned"]),
        "pinned_ids": summary["pinned"],
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "defaults.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("id   insecure  reasons")
    for row in rows:
        reasons = ",".join(row["reasons"]) if row["reasons"] else "-"
        print(f"{row['id']}  {str(row['insecure']):<8}  {reasons}")
    print(f"insecure {len(summary['insecure'])}/{len(stacks)}  pinned-vuln {len(summary['pinned'])}/{len(stacks)}")
    return out


if __name__ == "__main__":
    main()
