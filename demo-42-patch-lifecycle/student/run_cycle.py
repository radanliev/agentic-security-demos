#!/usr/bin/env python3
"""Evaluator for Demo 42.

Summarises the synthetic patch-lifecycle fixture into a median adoption
lag and a pin-blocked count.

Writes results/lifecycle.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from lifecycle import blocked, median  # noqa: E402


def main() -> dict:
    """Summarise lags, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "vulns.json").read_text())
    vulns = pack["vulns"]
    lags = [v["adopt_lag_days"] for v in vulns]
    med = median(lags)
    blocked_ids = blocked(vulns)
    out = {
        "demo": "demo-42-patch-lifecycle",
        "experiment": "patch-lifecycle",
        "seed": pack["seed"],
        "n": len(vulns),
        "median_adopt_lag_days": med,
        "n_blocked": len(blocked_ids),
        "blocked_ids": blocked_ids,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "lifecycle.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"vulns {len(vulns)}  lags {sorted(lags)}")
    print(f"median adopt lag {med} days")
    print(f"blocked by pin {len(blocked_ids)}/{len(vulns)}: {', '.join(blocked_ids)}.")
    return out


if __name__ == "__main__":
    main()
