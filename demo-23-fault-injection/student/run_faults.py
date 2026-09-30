#!/usr/bin/env python3
"""Runner for Demo 23.

Evaluates the fault-outcome table without retries and with retry
budget 2, writes results/faults.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from faults import outcome  # noqa: E402


def tally(faults: list, retries: int) -> dict:
    """Count outcomes for a fault list at a retry budget."""
    counts = {"graceful": 0, "cascade": 0, "silent-wrong": 0, "cost-blowup": 0}
    rows = []
    for f in faults:
        o = outcome(f, retries)
        counts[o] += 1
        rows.append({"id": f["id"], "type": f["type"], "outcome": o})
    return {"n": len(faults), "counts": counts, "rows": rows}


def main() -> dict:
    """Run both retry modes, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "faults.json").read_text())
    faults = pack["faults"]
    no_retry = tally(faults, 0)
    with_retry = tally(faults, 2)

    out = {
        "demo": "demo-23-fault-injection",
        "experiment": "retry-budget-scorecard",
        "seed": pack["seed"],
        "no_retry": no_retry,
        "with_retry": with_retry,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "faults.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"fault-injection scorecard (seed {pack['seed']}): {len(faults)} faults")
    print("mode       graceful  cascade  silent-wrong  cost-blowup")
    for name, t in (("no-retry", no_retry), ("retry-2", with_retry)):
        c = t["counts"]
        print(
            f"{name:<10} {c['graceful']}/{t['n']}        {c['cascade']}/{t['n']}        "
            f"{c['silent-wrong']}/{t['n']}             {c['cost-blowup']}/{t['n']}"
        )
    print("lesson: retries lift graceful from 2/6 to 5/6; the permanent fault still cascades.")
    return out


if __name__ == "__main__":
    main()
