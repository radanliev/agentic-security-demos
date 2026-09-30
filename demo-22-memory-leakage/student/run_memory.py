#!/usr/bin/env python3
"""Runner for Demo 22.

Applies the memory-leakage checks to the synthetic fixture set, writes
results/memory_leak.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from memory import erasure_failures, persists_high, resurfaced  # noqa: E402


def main() -> dict:
    """Run the leakage screen, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "memory.json").read_text())
    entries = pack["entries"]
    high = persists_high(entries)
    resurf = resurfaced(entries)
    erasure = erasure_failures(entries)
    n_deleted = sum(1 for e in entries if e.get("deleted"))

    out = {
        "demo": "demo-22-memory-leakage",
        "experiment": "memory-leak-screen",
        "seed": pack["seed"],
        "n_entries": len(entries),
        "persists_high": high,
        "resurfaced": resurf,
        "erasure_failures": erasure,
        "n_deleted": n_deleted,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "memory_leak.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"memory-leak screen (seed {pack['seed']}): {len(entries)} entries")
    print("check          count  ids")
    print(f"persists-high  {len(high)}      {','.join(high)}")
    print(f"resurfaced     {len(resurf)}      {','.join(resurf)}")
    print(f"erasure-fail   {len(erasure)}/{n_deleted}    {','.join(erasure)}")
    print("lesson: 2 high-sensitivity persists; 2 cross-session resurfaces; 1/3 erasures fail.")
    return out


if __name__ == "__main__":
    main()
