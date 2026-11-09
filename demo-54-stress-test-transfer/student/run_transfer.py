#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from transfer import evaluate, load, transfer_gap


def main() -> None:
    data = load(ROOT / "fixtures" / "cases.json")
    thr = data["threshold"]
    ind = evaluate(data["in_distribution"], thr)
    sh = evaluate(data["shifted"], thr)
    gap = transfer_gap(ind, sh)
    report = {"threshold": thr, "in_distribution": ind, "shifted": sh, "gap": gap}
    out = ROOT / "results" / "transfer.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print("Demo 54: stress-test transfer on synthetic detector scores")
    print()
    print("  threshold %s" % thr)
    print("  in-distribution recall %s  accuracy %s" % (ind["recall"], ind["accuracy"]))
    print("  shifted recall         %s  accuracy %s" % (sh["recall"], sh["accuracy"]))
    print("  recall drop %s  (shifted attacks fall below the threshold)" % gap["recall_drop"])
    print()
    print("Fixtures are placeholders that exercise the checker; they are not results.")


if __name__ == "__main__":
    main()
