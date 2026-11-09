#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from delphi import load, summarise


def main() -> None:
    data = load(ROOT / "fixtures" / "ratings.json")
    rows = [summarise(p) for p in data["propositions"]]
    out = ROOT / "results" / "delphi.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rows, indent=2) + "\n")
    print("Demo 59: Delphi summaries on synthetic panel ratings")
    print()
    for row in rows:
        print("  %s  median %s  IQR %s  consensus=%s  briefing %s" % (
            row["id"], row["median"], row["iqr"], row["consensus"], row["briefing_hash"]))
    print()
    print("No panellists were recruited; the ratings are toys.")


if __name__ == "__main__":
    main()
