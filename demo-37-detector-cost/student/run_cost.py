#!/usr/bin/env python3
"""Cost comparison of two toy detectors for Demo 37.

Scores both detectors on the synthetic fixture, prices false positives at
10 and false negatives at 25, and declares the cheaper operating point.

Writes results/detector_cost.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from detectors import lenient, strict  # noqa: E402


def score(inputs: list, detector) -> dict:
    """Score one detector: TP/FP/FN/TN plus priced cost."""
    tp = fp = fn = tn = 0
    for item in inputs:
        flagged = detector(item["text"])
        if item["injected"] and flagged:
            tp += 1
        elif item["injected"]:
            fn += 1
        elif flagged:
            fp += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def main() -> dict:
    """Evaluate both detectors, price them, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "inputs.json").read_text())
    fp_cost = pack["fp_cost"]
    fn_cost = pack["fn_cost"]
    strict_res = score(pack["inputs"], strict)
    strict_res["cost"] = strict_res["fp"] * fp_cost + strict_res["fn"] * fn_cost
    lenient_res = score(pack["inputs"], lenient)
    lenient_res["cost"] = lenient_res["fp"] * fp_cost + lenient_res["fn"] * fn_cost
    winner = "strict" if strict_res["cost"] <= lenient_res["cost"] else "lenient"
    out = {
        "demo": "demo-37-detector-cost",
        "experiment": "detector-cost",
        "seed": pack["seed"],
        "fp_cost": fp_cost,
        "fn_cost": fn_cost,
        "strict": strict_res,
        "lenient": lenient_res,
        "winner": winner,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "detector_cost.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"fp_cost {fp_cost}  fn_cost {fn_cost}")
    print("detector  tp   fp   fn   cost")
    for name in ("strict", "lenient"):
        r = out[name]
        print(
            f"{name:<9} {r['tp']}/4  {r['fp']}/6  {r['fn']}/4  {r['cost']}"
        )
    print(
        f"winner: {winner} (cost {out[winner]['cost']} < "
        f"{out['lenient' if winner == 'strict' else 'strict']['cost']})."
    )
    return out


if __name__ == "__main__":
    main()
