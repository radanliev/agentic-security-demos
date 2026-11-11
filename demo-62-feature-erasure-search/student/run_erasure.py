"""Run the Demo-62 toy: exhaustive versus greedy feature erasure."""

import json
from pathlib import Path
from erasure import exhaustive_min_erasure, greedy_erasure, score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "instances.json").read_text())
    rows = []
    for inst in data["instances"]:
        original = score(inst["weights"], inst["x"], inst["bias"])
        ex_idx, ex_score = exhaustive_min_erasure(inst["weights"], inst["x"], inst["bias"])
        gr_idx, gr_score = greedy_erasure(inst["weights"], inst["x"], inst["bias"])
        rows.append({
            "id": inst["id"],
            "original": original,
            "exhaustive": ex_idx,
            "exhaustive_size": None if ex_idx is None else len(ex_idx),
            "exhaustive_score": ex_score,
            "greedy": gr_idx,
            "greedy_size": None if gr_idx is None else len(gr_idx),
            "greedy_score": gr_score,
            "greedy_matches": ex_idx is not None and gr_idx is not None and len(ex_idx) == len(gr_idx),
        })
    print(f"instances {len(rows)}")
    for row in rows:
        print(f"{row['id']:<4} orig={row['original']:<6} ex={row['exhaustive_size']} greedy={row['greedy_size']} match={row['greedy_matches']}")
    out = ROOT / "results" / "erasure.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
