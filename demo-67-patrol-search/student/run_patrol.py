"""Run the Demo-67 toy: exhaustive versus greedy patrol allocations."""

import json
from pathlib import Path
from patrol import exhaustive, greedy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "graphs.json").read_text())
    k = data["k"]
    rows = []
    for case in data["cases"]:
        ex_set, ex_uncovered = exhaustive(case["nodes"], case["paths"], k)
        gr_set, gr_uncovered = greedy(case["nodes"], case["paths"], k)
        rows.append({
            "id": case["id"], "paths": len(case["paths"]),
            "exhaustive": ex_set, "exhaustive_uncovered": ex_uncovered,
            "greedy": gr_set, "greedy_uncovered": gr_uncovered,
            "greedy_optimal": gr_uncovered == ex_uncovered,
        })
        print(f"{case['id']:<4} ex_uncovered={ex_uncovered} greedy_uncovered={gr_uncovered} optimal={gr_uncovered == ex_uncovered}")
    out = ROOT / "results" / "patrol.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"k": k, "rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
