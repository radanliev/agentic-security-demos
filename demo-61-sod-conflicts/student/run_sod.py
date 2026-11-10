"""Run the Demo-61 toy: audit eight synthetic users for SoD conflicts."""

import json
from pathlib import Path
from sod import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "policies.json").read_text())
    rows = audit(data["users"], data["role_members"], data["role_permissions"], data["constraints"])
    gapped = [row["user"] for row in rows if row["gapped"]]
    print(f"users {len(rows)}  conflicts {len(gapped)}")
    for row in rows:
        flag = "YES" if row["gapped"] else "no"
        print(f"{row['user']:<4} perms={','.join(row['permissions']) or '-':<40} sod={flag}")
    print(f"gapped users: {', '.join(gapped) if gapped else '(none)'}")
    out = ROOT / "results" / "sod.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rows": rows, "gapped": gapped}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
