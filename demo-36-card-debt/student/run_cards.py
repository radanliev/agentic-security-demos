#!/usr/bin/env python3
"""Evaluator for Demo 36.

Measures safety-section disclosure debt over twelve synthetic model
cards and splits the gap by download popularity.

Writes results/cards.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from cards import missing_safety, popularity_gap  # noqa: E402


def main() -> dict:
    """Audit cards, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "cards.json").read_text())
    cards = pack["cards"]
    missing = missing_safety(cards)
    gap = popularity_gap(cards)
    out = {
        "demo": "demo-36-card-debt",
        "experiment": "card-debt",
        "seed": pack["seed"],
        "total": len(cards),
        "missing_safety": len(missing),
        "missing_ids": missing,
        "top_missing": len(gap["top_missing"]),
        "top_missing_ids": gap["top_missing"],
        "bottom_missing": len(gap["bottom_missing"]),
        "bottom_missing_ids": gap["bottom_missing"],
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "cards.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("id   downloads  safety")
    for card in sorted(cards, key=lambda c: c["downloads"], reverse=True):
        print(f"{card['id']}   {card['downloads']:<9}  {str(card['safety'])}")
    print(f"missing safety {len(missing)}/{len(cards)}")
    print(f"top-4 missing {len(gap['top_missing'])}/4  bottom-8 missing {len(gap['bottom_missing'])}/8")
    return out


if __name__ == "__main__":
    main()
