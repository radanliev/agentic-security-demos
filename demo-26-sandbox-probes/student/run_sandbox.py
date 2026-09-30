#!/usr/bin/env python3
"""Runner for Demo 26.

Scores each sandbox config, writes results/sandbox.json and prints
the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from sandbox import escape_rate, escaped_probes  # noqa: E402


def main() -> dict:
    """Score all configs, write results, print table."""
    matrix = json.loads((DEMO_DIR / "fixtures" / "matrix.json").read_text())
    rows = {}
    for config in ("none", "subprocess", "strict"):
        n_esc, total, rate = escape_rate(matrix, config)
        rows[config] = {
            "escaped": n_esc,
            "total": total,
            "rate": rate,
            "probes": escaped_probes(matrix, config),
        }

    out = {
        "demo": "demo-26-sandbox-probes",
        "experiment": "isolation-ladder",
        "seed": matrix["seed"],
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "sandbox.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"sandbox ladder (seed {matrix['seed']}): {len(matrix['probes'])} probes")
    print("config      escaped  rate")
    for config in ("none", "subprocess", "strict"):
        r = rows[config]
        print(f"{config:<11} {r['escaped']}/{r['total']}       {r['rate']:.2f}")
    print("lesson: none 8/8 escapes; subprocess leaks 3/8; strict holds 0/8.")
    return out


if __name__ == "__main__":
    main()
