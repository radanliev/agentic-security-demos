#!/usr/bin/env python3
"""Evaluator for Demo 32.

Audits ten synthetic papers for code+data sharing and reproduction.

Writes results/sok_audit.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from audit import invariant_holds, rates  # noqa: E402


def main() -> dict:
    """Audit papers, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "papers.json").read_text())
    papers = pack["papers"]
    summary = rates(papers)
    ok = invariant_holds(papers)
    out = {
        "demo": "demo-32-reproducibility-audit",
        "experiment": "sok-audit",
        "seed": pack["seed"],
        "total": summary["n"],
        "code_data": summary["code_data"],
        "reproduces": summary["reproduces"],
        "by_channel": summary["by_channel"],
        "invariant_holds": ok,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "sok_audit.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("channel     n  reproduces")
    for channel in sorted(summary["by_channel"]):
        bucket = summary["by_channel"][channel]
        print(f"{channel:<11} {bucket['n']}  {bucket['reproduces']}")
    print(f"code+data {summary['code_data']}/{summary['n']}  reproduces {summary['reproduces']}/{summary['n']}")
    return out


if __name__ == "__main__":
    main()
