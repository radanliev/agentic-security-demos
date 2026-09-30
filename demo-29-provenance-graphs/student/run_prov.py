#!/usr/bin/env python3
"""Evaluator for Demo 29.

Reconstructs attribution over six synthetic actions, builds a sha256
chain, verifies it, then tampers a copy to show detection.

Writes results/provenance.json and prints the summary table.
"""

import copy
import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from provenance import attributable, build_chain, verify  # noqa: E402


def main() -> dict:
    """Reconstruct provenance, verify chain, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "actions.json").read_text())
    actions = pack["actions"]
    root_id = pack["root"]
    part = attributable(actions, root_id)
    chain = build_chain(actions)
    ok = verify(actions, chain)
    tampered = copy.deepcopy(actions)
    for rec in tampered:
        if rec["id"] == "a2":
            rec["authority"] = "operator"
    tamper_detected = not verify(tampered, chain)

    out = {
        "demo": "demo-29-provenance-graphs",
        "experiment": "attribution-reconstruction",
        "seed": pack["seed"],
        "total": len(actions),
        "attributable": len(part["attributable"]),
        "unattributable": part["unattributable"],
        "chain_verified": ok,
        "tamper_detected": tamper_detected,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "provenance.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("id   cause  attributable")
    for rec in sorted(actions, key=lambda r: r["id"]):
        cause = rec["cause"] if rec["cause"] is not None else "-"
        flag = "yes" if rec["id"] in part["attributable"] else "no"
        print(f"{rec['id']}   {cause:<5}  {flag}")
    print(f"attributable {len(part['attributable'])}/{len(actions)}  unattributable {','.join(part['unattributable'])}")
    print(f"chain verified {str(ok)}  tamper-detected {str(tamper_detected)}")
    return out


if __name__ == "__main__":
    main()
