"""Run the Demo-66 toy: link synthetic advisories and count disagreements."""

import json
from pathlib import Path
from linkage import link

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "advisories.json").read_text())
    rows = link(data["source_a"], data["source_b"])
    matched = [row for row in rows if row["matched"]]
    sev = sum(1 for row in matched if row["severity_disagree"])
    prod = sum(1 for row in matched if row["product_disagree"])
    print(f"left {len(rows)}  matched {len(matched)}  severity {sev}  product {prod}")
    for row in rows:
        print(f"{row['id']:<16} matched={row['matched']} sev={row['severity_disagree']} prod={row['product_disagree']}")
    out = ROOT / "results" / "linkage.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"matched": len(matched), "severity_disagree": sev, "product_disagree": prod, "rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
