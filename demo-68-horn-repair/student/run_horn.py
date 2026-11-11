"""Run the Demo-68 toy: minimum Horn deletions that restore consistency."""

import json
from pathlib import Path
from horn import is_inconsistent, min_deletion

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "theories.json").read_text())
    rows = []
    for theory in data["theories"]:
        bad = is_inconsistent(theory["facts"], theory["clauses"])
        deleted, _ = min_deletion(theory["facts"], theory["clauses"])
        rows.append({"id": theory["id"], "inconsistent": bad, "deleted": deleted, "deletions": len(deleted)})
        print(f"{theory['id']:<4} inconsistent={bad} deletions={len(deleted)}")
    out = ROOT / "results" / "horn.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
