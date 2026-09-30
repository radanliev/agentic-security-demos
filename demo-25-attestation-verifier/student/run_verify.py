#!/usr/bin/env python3
"""Runner for Demo 25.

Applies the verifier under both policies, writes
results/attest.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from verifier import decide  # noqa: E402


def main() -> dict:
    """Verify all packages under both policies, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "packages.json").read_text())
    packages = pack["packages"]
    closed = [decide(p, "fail-closed") for p in packages]
    opened = [decide(p, "fail-open") for p in packages]
    n_blocked_closed = sum(d == "block" for d in closed)
    n_warned_open = sum(d == "allow-with-warning" for d in opened)

    out = {
        "demo": "demo-25-attestation-verifier",
        "experiment": "fail-closed-vs-open",
        "seed": pack["seed"],
        "n_packages": len(packages),
        "n_attested": sum(1 for p in packages if p["attested"]),
        "fail_closed_blocked": n_blocked_closed,
        "fail_open_warnings": n_warned_open,
        "closed_decisions": closed,
        "open_decisions": opened,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "attest.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"attestation screen (seed {pack['seed']}): {len(packages)} packages")
    print("policy       blocked  warned  allowed")
    print(f"fail-closed  {n_blocked_closed}/{len(packages)}        0/{len(packages)}       {len(packages) - n_blocked_closed}/{len(packages)}")
    print(f"fail-open    0/{len(packages)}        {n_warned_open}/{len(packages)}       {len(packages)}/{len(packages)}")
    print("lesson: fail-closed blocks 6/10 unattested; fail-open warns instead.")
    return out


if __name__ == "__main__":
    main()
