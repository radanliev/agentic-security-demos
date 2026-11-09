#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from coding import cohen_kappa, load, percent_agreement, validate_codebook


def main() -> None:
    data = load(ROOT / "fixtures" / "codes.json")
    bad = validate_codebook(data)
    pa = percent_agreement(data["documents"])
    kappa = cohen_kappa(data["documents"], data["codebook"])
    report = {"invalid": bad, "n": len(data["documents"]), "percent_agreement": pa, "kappa": kappa}
    out = ROOT / "results" / "coding.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print("Demo 57: double-coding a synthetic governance excerpt")
    print()
    print("  documents %s  invalid codes %s" % (report["n"], len(bad)))
    print("  percent agreement %s" % pa)
    print("  Cohen kappa %s" % kappa)
    print()
    print("Fixtures are placeholders that exercise the checker; they are not results.")


if __name__ == "__main__":
    main()
