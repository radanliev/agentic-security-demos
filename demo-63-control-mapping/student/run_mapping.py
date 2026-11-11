"""Run the Demo-63 toy: align synthetic techniques to compensating controls."""

import json
from pathlib import Path
from mapping import recommend

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "alignments.json").read_text())
    rows = []
    for profile in data["profiles"]:
        result = recommend(profile["techniques"], data["alignment"])
        result["id"] = profile["id"]
        rows.append(result)
        print(f"{profile['id']:<4} controls={len(result['controls'])} covered={len(result['covered'])} uncovered={len(result['uncovered'])}")
    out = ROOT / "results" / "mapping.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
