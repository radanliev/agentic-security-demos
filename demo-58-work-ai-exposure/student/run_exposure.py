#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from exposure import agentic_share, family_means, load, occupation_mean


def main() -> None:
    data = load(ROOT / "fixtures" / "tasks.json")
    by_occ = {occ["id"]: occupation_mean(occ) for occ in data["occupations"]}
    report = {
        "occupation_means": by_occ,
        "family_means": family_means(data["occupations"]),
        "agentic_share": agentic_share(data["occupations"]),
    }
    out = ROOT / "results" / "exposure.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print("Demo 58: task exposure on synthetic higher-education roles")
    print()
    for occ, mean in by_occ.items():
        print("  %s mean exposure %s" % (occ, mean))
    print("  family means %s" % report["family_means"])
    print("  share of tasks marked agentic %s" % report["agentic_share"])
    print()
    print("Exposure is not displacement; these rows are toys.")


if __name__ == "__main__":
    main()
