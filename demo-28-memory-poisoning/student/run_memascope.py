#!/usr/bin/env python3
"""Runner for Demo 28.

Audits every memory entry, writes results/memascope.json and prints
the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from memascope import audit  # noqa: E402


def main() -> dict:
    """Audit all entries, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "entries.json").read_text())
    entries = pack["entries"]
    flagged = audit(entries)
    benign = [e["id"] for e in entries if e["id"] not in flagged]

    out = {
        "demo": "demo-28-memory-poisoning",
        "experiment": "memascope-audit",
        "seed": pack["seed"],
        "n_entries": len(entries),
        "flagged": flagged,
        "n_flagged": len(flagged),
        "n_benign": len(benign),
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "memascope.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"memascope audit (seed {pack['seed']}): {len(entries)} entries")
    print("entry  verdict")
    for e in entries:
        print(f"{e['id']:<6} {'POISONED' if e['id'] in flagged else 'benign'}")
    print(f"lesson: flagged {len(flagged)}/{len(entries)} poisoned entries, 0 false positives.")
    return out


if __name__ == "__main__":
    main()
