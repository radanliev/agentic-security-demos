#!/usr/bin/env python3
"""Census runner for Demo 15.

Applies the poisoning classifier, the rug-pull detector and the capability
tally over twelve synthetic server manifests. Writes results/census.json
and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from poisoning_detector import is_poisoned  # noqa: E402
from drift_detector import has_drifted  # noqa: E402
from capability_tally import tally  # noqa: E402

POPULAR_THRESHOLD = 10000


def main() -> dict:
    """Run the census over fixtures and write results."""
    pack = json.loads((DEMO_DIR / "fixtures" / "servers.json").read_text())
    servers = pack["servers"]

    poisoned = [s["id"] for s in servers if is_poisoned(s["description"])]
    high = [s for s in servers if s["downloads"] >= POPULAR_THRESHOLD]
    low = [s for s in servers if s["downloads"] < POPULAR_THRESHOLD]
    poisoned_high = [s["id"] for s in high if is_poisoned(s["description"])]
    poisoned_low = [s["id"] for s in low if is_poisoned(s["description"])]

    pairs = [(s["id"], s["v1"], s["v2"]) for s in servers if s["v2"] is not None]
    drifted = [sid for sid, v1, v2 in pairs if has_drifted(v1, v2)]

    cap = tally(servers)

    out = {
        "demo": "demo-15-mcp-ecosystem",
        "experiment": "mcp-census",
        "seed": pack["seed"],
        "n_servers": len(servers),
        "n_poisoned": len(poisoned),
        "poisoned_ids": sorted(poisoned),
        "poisoned_high": sorted(poisoned_high),
        "poisoned_low": sorted(poisoned_low),
        "n_pairs": len(pairs),
        "n_drifted": len(drifted),
        "drifted_ids": sorted(drifted),
        "capabilities": cap,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "census.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"servers {len(servers)}  poisoned {len(poisoned)} "
          f"(high {len(poisoned_high)}/{len(high)}, low {len(poisoned_low)}/{len(low)})")
    print(f"version pairs {len(pairs)}  drifted {len(drifted)}: {', '.join(sorted(drifted))}")
    print(f"shell {cap['n_shell']}  shell+network {cap['n_shell_with_network']}  "
          f"top4 maintainers {len(cap['top4_maintainers'])} ({', '.join(cap['top4_maintainers'])})")
    print("lesson: poisoning is non-trivial and concentrated low; drift is measurable; "
          "shell bundles with network.")
    return out


if __name__ == "__main__":
    main()
