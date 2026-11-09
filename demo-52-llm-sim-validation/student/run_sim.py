#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from sim_validate import contamination_probe, honest_predict, load_cohorts, memorizer_predict, score_heldout


def main() -> None:
    data = load_cohorts(ROOT / "fixtures" / "cohorts.json")
    train, heldout, probe = data["train_modules"], data["heldout_modules"], data["renamed_probe"]
    honest = {
        "heldout": score_heldout(honest_predict, train, heldout),
        "probe": contamination_probe(honest_predict, train, probe),
    }
    memo = {
        "heldout": score_heldout(memorizer_predict, train, heldout),
        "probe": contamination_probe(memorizer_predict, train, probe),
    }
    out = ROOT / "results" / "sim_validation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"honest": honest, "memorizer": memo}, indent=2) + "\n")
    print("Demo 52: verifying toy cohort simulators against held-out and renamed modules")
    print()
    print("  honest held-out pass MAE     %s" % honest["heldout"]["pass_mae"])
    print("  memorizer held-out pass MAE  %s" % memo["heldout"]["pass_mae"])
    print("  honest rename probe source   %s (transfers AAA to ZZZ)" % honest["probe"]["source"])
    print("  memorizer rename probe       %s (fails to transfer)" % memo["probe"]["source"])
    print()
    print("Fixtures are placeholders that exercise the checker; they are not results.")


if __name__ == "__main__":
    main()
