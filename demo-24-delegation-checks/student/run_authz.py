#!/usr/bin/env python3
"""Runner for Demo 24.

Checks every delegation chain, writes results/authz.json and prints
the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from authz import check  # noqa: E402


def main() -> dict:
    """Check all chains, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "chains.json").read_text())
    chains = pack["chains"]
    rows = []
    for c in chains:
        violations = check(c)
        rows.append(
            {"id": c["id"], "violations": violations, "clean": not violations}
        )
    n_clean = sum(r["clean"] for r in rows)
    n_viol = len(rows) - n_clean

    out = {
        "demo": "demo-24-delegation-checks",
        "experiment": "delegation-properties",
        "seed": pack["seed"],
        "n_chains": len(chains),
        "n_clean": n_clean,
        "n_violations": n_viol,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "authz.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"delegation checks (seed {pack['seed']}): {len(chains)} chains")
    print("chain  verdict")
    for r in rows:
        verdict = "clean" if r["clean"] else "; ".join(r["violations"])
        print(f"{r['id']:<6} {verdict}")
    print(f"lesson: {n_clean} clean, {n_viol} violations (c5 audience, c6 scope).")
    return out


if __name__ == "__main__":
    main()
