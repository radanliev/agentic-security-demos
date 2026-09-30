#!/usr/bin/env python3
"""Runner for Demo 16.

Computes R0 per topology, simulates uncontained spread from node 0 and
contained spread on the chain (4 edges blocked). Writes
results/spread.json and prints a summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from epidemic import degrees_of, r0, simulate  # noqa: E402


def main() -> dict:
    """Run the spread toy, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "graphs.json").read_text())
    p = pack["p"]
    topologies = pack["topologies"]
    blocked = pack["containment"]["chain_blocked_edges"]

    r0_by_topo = {}
    infected_counts = {}
    for name, topo in topologies.items():
        degrees = degrees_of(topo["nodes"], topo["edges"])
        r0_by_topo[name] = r0(p, degrees)
        infected_counts[name] = len(simulate(topo["nodes"], topo["edges"]))

    chain = topologies["chain"]
    contained = len(simulate(chain["nodes"], chain["edges"], blocked))

    out = {
        "demo": "demo-16-infection-spread",
        "experiment": "epidemic-containment",
        "seed": pack["seed"],
        "p": p,
        "r0": r0_by_topo,
        "infected": infected_counts,
        "contained": {"chain": contained},
        "blocked_edges": blocked,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "spread.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"p {p}  seed {pack['seed']}")
    print("topo   r0    infected  contained")
    for name in ("chain", "star", "mesh", "tree"):
        cont = str(contained) + "/6" if name == "chain" else "-"
        print(f"{name:<6} {r0_by_topo[name]:.2f}  {infected_counts[name]}/6       {cont}")
    print("lesson: uncontained spread reaches 6/6 everywhere; blocking 4 chain edges holds the chain at 2/6.")
    return out


if __name__ == "__main__":
    main()
