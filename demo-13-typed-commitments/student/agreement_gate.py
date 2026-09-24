#!/usr/bin/env python3
"""Agreement gate for Demo 13.

Runs both toy assessors over the six synthetic instances, scores each
nomination against the oracle, and reports per-cue-level accuracy plus the
pairwise agreement that a redundant pipeline would gate on.

Writes results/toy_eval.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from cue_follower import CueFollower  # noqa: E402
from independent_heuristic import IndependentHeuristic  # noqa: E402


def main() -> dict:
    instances = json.loads((DEMO_DIR / "fixtures" / "instances.json").read_text())["instances"]
    follower, independent = CueFollower(), IndependentHeuristic()

    rows: list = []
    summary: dict = {"n": len(instances), "by_cue": {}}
    for inst in instances:
        oracle = inst["vulnerable_file"]
        f_pick = follower.solve(inst["files"], inst["cue"])
        h_pick = independent.solve(inst["files"], inst["cue"])
        row = {
            "id": inst["id"],
            "cue": inst["cue"]["kind"],
            "oracle": oracle,
            "follower": f_pick,
            "independent": h_pick,
            "follower_correct": f_pick == oracle,
            "independent_correct": h_pick == oracle,
            "agree": f_pick == h_pick,
        }
        rows.append(row)

    summary["follower_correct"] = sum(r["follower_correct"] for r in rows)
    summary["independent_correct"] = sum(r["independent_correct"] for r in rows)
    summary["agreed"] = sum(r["agree"] for r in rows)
    summary["agreed_and_wrong"] = sum(r["agree"] and not r["follower_correct"] for r in rows)
    for kind in ("none", "true", "wrong"):
        group = [r for r in rows if r["cue"] == kind]
        summary["by_cue"][kind] = {
            "n": len(group),
            "follower_correct": sum(r["follower_correct"] for r in group),
            "independent_correct": sum(r["independent_correct"] for r in group),
            "agreed": sum(r["agree"] for r in group),
        }

    out = {"rows": rows, "summary": summary}
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "toy_eval.json").write_text(json.dumps(out, indent=2) + "\n")

    print("cue    n  follower  independent  agreed")
    for kind in ("none", "true", "wrong"):
        g = summary["by_cue"][kind]
        print(f"{kind:<6} {g['n']}  {g['follower_correct']}/{g['n']}        "
              f"{g['independent_correct']}/{g['n']}           {g['agreed']}/{g['n']}")
    print(f"total  {summary['n']}  {summary['follower_correct']}/{summary['n']}        "
          f"{summary['independent_correct']}/{summary['n']}           {summary['agreed']}/{summary['n']}")
    print(f"agreed-but-wrong (gate passes, answer wrong): "
          f"{summary['agreed_and_wrong']}/{summary['agreed']}")
    return out


if __name__ == "__main__":
    main()
