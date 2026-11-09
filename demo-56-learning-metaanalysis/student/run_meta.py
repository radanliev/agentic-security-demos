#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from meta import fixed_effect, load


def main() -> None:
    data = load(ROOT / "fixtures" / "studies.json")
    summary = fixed_effect(data["studies"])
    out = ROOT / "results" / "meta.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"note": data["note"], "summary": summary}, indent=2) + "\n")
    print("Demo 56: fixed-effect mean on synthetic study rows")
    print()
    print("  %s" % data["note"])
    print("  k %s  mean %s  se %s  Q %s (df %s)" % (summary["k"], summary["mean"], summary["se"], summary["Q"], summary["df"]))
    print()
    print("These rows are toys; they are not a literature estimate.")


if __name__ == "__main__":
    main()
