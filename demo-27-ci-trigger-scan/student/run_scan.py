#!/usr/bin/env python3
"""Runner for Demo 27.

Scans every repo fixture, writes results/ci_scan.json and prints
the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from scanner import is_vulnerable  # noqa: E402


def main() -> dict:
    """Scan all repos, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "repos.json").read_text())
    repos = pack["repos"]
    rows = [
        {"id": r["id"], "vulnerable": is_vulnerable(r)} for r in repos
    ]
    flagged = [r["id"] for r in rows if r["vulnerable"]]

    out = {
        "demo": "demo-27-ci-trigger-scan",
        "experiment": "ci-wiring-scan",
        "seed": pack["seed"],
        "n_repos": len(repos),
        "n_vulnerable": len(flagged),
        "flagged": flagged,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "ci_scan.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"ci-trigger scan (seed {pack['seed']}): {len(repos)} repos")
    print("repo  verdict")
    for r in rows:
        print(f"{r['id']:<5} {'VULNERABLE' if r['vulnerable'] else 'ok'}")
    print(f"lesson: {len(flagged)}/{len(repos)} repos expose public write triggers without review.")
    return out


if __name__ == "__main__":
    main()
