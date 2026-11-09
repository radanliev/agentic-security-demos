#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from power import load, plan_table


def main() -> None:
    cfg = load(ROOT / "fixtures" / "plan.json")
    table = plan_table(cfg)
    out = ROOT / "results" / "power.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"plan": cfg, "power": table}, indent=2) + "\n")
    print("Demo 55: analytic power for a two-arm retention contrast (synthetic plan)")
    print()
    print("  n per arm %s  alpha %s  sd %s" % (cfg["n_per_arm"], cfg["alpha"], cfg["sd"]))
    print("  power against an immediate difference of %s : %s" % (cfg["raw_difference"], table["immediate_power"]))
    print("  power against a residual difference of %s  : %s" % (cfg["residual_difference"], table["residual_power"]))
    print()
    print("These figures are a planning calculation on a toy plan, not a trial result.")


if __name__ == "__main__":
    main()
