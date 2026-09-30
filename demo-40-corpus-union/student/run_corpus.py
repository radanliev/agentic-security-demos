#!/usr/bin/env python3
"""Evaluator for Demo 40.

Unions twelve synthetic source records, dedupes exact cross-source
duplicates, and applies the licence gate.

Writes results/corpus.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from corpus import dedupe, releasable  # noqa: E402


def main() -> dict:
    """Union, dedupe, gate, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "records.json").read_text())
    records = pack["records"]
    unique = dedupe(records)
    released = releasable(records)
    blocked = [r["id"] for r in unique if r not in released]
    out = {
        "demo": "demo-40-corpus-union",
        "experiment": "corpus-union",
        "seed": pack["seed"],
        "n_records": len(records),
        "n_unique": len(unique),
        "n_releasable": len(released),
        "released_ids": sorted(r["id"] for r in released),
        "blocked_ids": sorted(blocked),
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "corpus.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"records {len(records)}  unique {len(unique)}")
    print(f"duplicates removed {len(records) - len(unique)}")
    print(f"releasable {len(released)}/{len(unique)}")
    print(f"blocked: {', '.join(sorted(blocked))}.")
    return out


if __name__ == "__main__":
    main()
