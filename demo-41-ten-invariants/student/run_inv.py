#!/usr/bin/env python3
"""Evaluator for Demo 41.

Runs the ten-invariant checklist over the synthetic fixture and reports
which invariants hold and which are violated.

Writes results/invariants.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from invariants import evaluate  # noqa: E402


def main() -> dict:
    """Evaluate the checklist, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "checks.json").read_text())
    res = evaluate(pack["invariants"])
    out = {
        "demo": "demo-41-ten-invariants",
        "experiment": "invariant-checklist",
        "seed": pack["seed"],
        "evaluation": res,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "invariants.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"invariants {res['n']}  holding {res['n_holding']}  violated {res['n_violated']}")
    print("verdict      name")
    for name in sorted(res["holding"]):
        print(f"hold         {name}")
    for name in sorted(res["violated"]):
        print(f"VIOLATED     {name}")
    return out


if __name__ == "__main__":
    main()
