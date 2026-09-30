#!/usr/bin/env python3
"""Evaluator for Demo 35.

Regresses ten synthetic unsafe-rate rows by benchmark and by scale bin.

Writes results/meta.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from meta import group_means  # noqa: E402


def main() -> dict:
    """Compute group means, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "results.json").read_text())
    rows = pack["rows"]
    summary = group_means(rows)
    out = {
        "demo": "demo-35-scaling-metaregression",
        "experiment": "scaling-meta",
        "seed": pack["seed"],
        "total": len(rows),
        "mean_A": summary["mean_A"],
        "mean_B": summary["mean_B"],
        "bench_gap": summary["bench_gap"],
        "mean_small": summary["mean_small"],
        "mean_large": summary["mean_large"],
        "scale_gap": summary["scale_gap"],
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "meta.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"benchmark A mean {summary['mean_A']:.3f} (n={summary['n_A']})")
    print(f"benchmark B mean {summary['mean_B']:.3f} (n={summary['n_B']})")
    print(f"bench gap {summary['bench_gap']:.3f}")
    print(f"scale small mean {summary['mean_small']:.3f} (n={summary['n_small']})")
    print(f"scale large mean {summary['mean_large']:.3f} (n={summary['n_large']})")
    print(f"scale gap {summary['scale_gap']:.3f}")
    print("lesson: benchmark explains more than scale.")
    return out


if __name__ == "__main__":
    main()
