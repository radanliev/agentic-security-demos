#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from battery import load, score_battery


def main() -> None:
    data = load(ROOT / "fixtures" / "tasks.json")
    report = score_battery(data["tasks"])
    out = ROOT / "results" / "battery.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print("Demo 60: scoring a synthetic engineering-biology analysis battery")
    print()
    for row in report["rows"]:
        print("  %s  predicted %s  reference %s  %s" % (
            row["id"], row["predicted"], row["reference"], "ok" if row["correct"] else "miss"))
    print("  accuracy %s (%s/%s)" % (report["accuracy"], report["correct"], report["n"]))
    print()
    print("Series and sequences are toys; no biological sample was used.")


if __name__ == "__main__":
    main()
