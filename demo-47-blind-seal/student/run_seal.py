"""Run the three synthetic pre-reveal seal cases and write results/seals.json."""

import json
from pathlib import Path

from seal import score, seal

ROOT = Path(__file__).resolve().parents[1]


def main():
    cases = json.loads((ROOT / "fixtures" / "cases.json").read_text())
    prev = "0" * 64
    rows = []
    for case in cases:
        link = seal(case["id"], case["commitment"], prev)
        shown = case.get("after_seal", case["commitment"])
        rows.append({
            "id": case["id"],
            "verdict": score(link, shown, case["truth"]),
            "seal": link["seal"],
        })
        prev = link["seal"]
    out = ROOT / "results" / "seals.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2) + "\n")
    for row in rows:
        print(f"{row['id']}: {row['verdict']}")


if __name__ == "__main__":
    main()
