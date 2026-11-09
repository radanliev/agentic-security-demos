#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from validate import coverage, design_based_error_rate, load, planted


def main() -> None:
    data = load(ROOT / "fixtures" / "outputs.json")
    cov = coverage(data["items"], data["sample_ids"])
    rate = design_based_error_rate(data["items"], data["sample_ids"])
    report = {
        "n_items": len(data["items"]),
        "n_planted": len(planted(data["items"])),
        "sample_ids": data["sample_ids"],
        "coverage": cov,
        "sample_error_rate": rate,
    }
    out = ROOT / "results" / "validation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print("Demo 53: sampled validation of synthetic agent outputs")
    print()
    print("  items %s  planted %s" % (report["n_items"], report["n_planted"]))
    print("  sample %s" % ",".join(data["sample_ids"]))
    print("  planted-in-sample %s/%s  coverage %s" % (cov["planted_in_sample"], cov["planted"], cov["coverage"]))
    print("  sample error rate %s" % rate)
    print()
    print("Fixtures are placeholders that exercise the checker; they are not results.")


if __name__ == "__main__":
    main()
