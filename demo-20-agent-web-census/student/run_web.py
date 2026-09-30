#!/usr/bin/env python3
"""Runner for Demo 20.

Tallies agent-directive adoption and injection exposure over the
synthetic sites. Writes results/web_census.json and prints a summary
table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from census import adopted, exposed  # noqa: E402


def main() -> dict:
    """Tally the census, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "sites.json").read_text())
    sites = pack["sites"]

    rows = []
    for s in sites:
        rows.append(
            {
                "id": s["id"],
                "adopted": adopted(s),
                "exposed": exposed(s),
                "popularity": s["popularity"],
            }
        )
    adopting = [r for r in rows if r["adopted"]]
    exposing = [r for r in rows if r["exposed"]]

    out = {
        "demo": "demo-20-agent-web-census",
        "experiment": "agent-facing-census",
        "seed": pack["seed"],
        "n_sites": len(sites),
        "n_adopting": len(adopting),
        "n_exposed": len(exposing),
        "exposed_ids": sorted(r["id"] for r in exposing),
        "exposed_popularity": sorted(r["popularity"] for r in exposing),
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "web_census.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"sites {len(sites)}  adopting {len(adopting)}/{len(sites)}  exposed {len(exposing)}/{len(sites)}")
    print("id   popularity  adopted  exposed")
    for r in rows:
        print(f"{r['id']:<4} {r['popularity']:<10} {str(r['adopted']):<8} {r['exposed']}")
    print("lesson: adoption 4/10; injections 2/10, both on low-popularity sites.")
    return out


if __name__ == "__main__":
    main()
