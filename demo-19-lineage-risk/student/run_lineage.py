#!/usr/bin/env python3
"""Runner for Demo 19.

Classifies the synthetic model lineage, counts risky models split by
origin / introduced / inherited. Writes results/lineage.json and prints
a summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from lineage import classify  # noqa: E402


def main() -> dict:
    """Classify lineage, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "models.json").read_text())
    models = pack["models"]
    result = classify(models)
    kinds = result["kinds"]

    rows = [{"id": m["id"], "kind": kinds[m["id"]]} for m in models]
    risky_ids = sorted(mid for mid, kind in kinds.items() if kind != "safe")
    by_kind: dict = {}
    for kind in kinds.values():
        by_kind[kind] = by_kind.get(kind, 0) + 1

    out = {
        "demo": "demo-19-lineage-risk",
        "experiment": "lineage-inheritance",
        "seed": pack["seed"],
        "n_models": len(models),
        "n_risky": len(risky_ids),
        "risky_ids": risky_ids,
        "by_kind": by_kind,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "lineage.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"models {len(models)}  risky {len(risky_ids)}/{len(models)}")
    print("id   kind")
    for r in rows:
        print(f"{r['id']:<4} {r['kind']}")
    print(f"origin {by_kind.get('origin', 0)}  introduced {by_kind.get('introduced', 0)}  inherited {by_kind.get('inherited', 0)}")
    print("lesson: 6/8 risky; clean-looking children inherit risk from flagged parents.")
    return out


if __name__ == "__main__":
    main()
