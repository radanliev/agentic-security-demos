#!/usr/bin/env python3
"""Runner for Demo 17.

Audits the synthetic trajectories with the fidelity checker, counts
faithful runs and violations by type. Writes results/fidelity.json and
prints a summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from fidelity import audit  # noqa: E402


def main() -> dict:
    """Audit all runs, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "trajectories.json").read_text())
    runs = pack["runs"]

    rows = []
    for run in runs:
        violations = audit(run)
        rows.append(
            {
                "id": run["id"],
                "faithful": not violations,
                "violations": violations,
            }
        )
    faithful = [r for r in rows if r["faithful"]]
    violating = [r for r in rows if not r["faithful"]]
    by_type: dict = {}
    for r in violating:
        for v in r["violations"]:
            by_type[v] = by_type.get(v, 0) + 1

    out = {
        "demo": "demo-17-report-fidelity",
        "experiment": "claims-vs-logs",
        "seed": pack["seed"],
        "n_runs": len(runs),
        "n_faithful": len(faithful),
        "n_violations": len(violating),
        "violations_by_type": by_type,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "fidelity.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"runs {len(runs)}  faithful {len(faithful)}  violations {len(violating)}")
    print("id   faithful  violations")
    for r in rows:
        detail = ",".join(r["violations"]) if r["violations"] else "-"
        print(f"{r['id']:<4} {str(r['faithful']):<8} {detail}")
    print("lesson: 5 faithful, 3 violations (one per type: tests_run, untouched, destructive).")
    return out


if __name__ == "__main__":
    main()
