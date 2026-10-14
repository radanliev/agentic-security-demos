"""Score two synthetic swaps against the frozen mean cosine shift."""

import json
from pathlib import Path

from drift import shift

ROOT = Path(__file__).resolve().parents[1]


def main():
    spec = json.loads((ROOT / "fixtures" / "cases.json").read_text())
    frozen = spec["frozen_mean_cosine_shift"]
    rows = []
    for case in spec["cases"]:
        value = shift(case["baseline"], case["replacement"])
        rows.append({
            "id": case["id"],
            "cosine_shift": round(value, 4),
            "above_frozen_mean": value > frozen,
        })
        print(f"{case['id']}: shift={value:.4f} above_frozen_mean={value > frozen}")
    out = ROOT / "results" / "drift.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"frozen_mean_cosine_shift": frozen, "cases": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
