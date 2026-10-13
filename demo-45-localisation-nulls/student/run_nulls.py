"""Run the Demo-45 toy: score 8 synthetic localisation attempts under the exact null."""

import json
from pathlib import Path

from nulls import lift, required_pool, scores, tail

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ALPHA = 0.01


def main():
    cases = json.loads((ROOT / "fixtures" / "cases.json").read_text())["cases"]
    rows = []
    for c in cases:
        p = tail(c["pool"], c["defective"], c["budget"], c["tp"])
        recall, precision, f1 = scores(c["defective"], c["budget"], c["tp"])
        rows.append(
            {
                "id": c["id"],
                "pool": c["pool"],
                "defective": c["defective"],
                "budget": c["budget"],
                "tp": c["tp"],
                "recall": round(recall, 4),
                "precision": round(precision, 4),
                "f1": round(f1, 4),
                "p_value": p,
                "significant_at_0.01": p <= ALPHA,
                "lift": round(lift(c["pool"], c["defective"], c["budget"], c["tp"]), 4),
            }
        )
    print(f"cases {len(rows)}  alpha {ALPHA}")
    print(f"{'id':<18}{'P/D/k/TP':<14}{'recall':<8}{'prec':<8}{'F1':<8}{'p':<12}{'sig'}")
    for r in rows:
        geom = f"{r['pool']}/{r['defective']}/{r['budget']}/{r['tp']}"
        print(
            f"{r['id']:<18}{geom:<14}{r['recall']:<8}{r['precision']:<8}"
            f"{r['f1']:<8}{r['p_value']:<12.6g}{'YES' if r['significant_at_0.01'] else 'no'}"
        )
    a = next(r for r in rows if r["id"] == "case5-transfer-A")
    b = next(r for r in rows if r["id"] == "case6-transfer-B")
    print(
        f"transfer check: same recall {a['recall']} but p {a['p_value']:.6g} vs "
        f"{b['p_value']:.6g}; lift {a['lift']} vs {b['lift']} (not comparable)."
    )
    print(f"design limit D=10 k=2 alpha=0.01: need pool >= {required_pool(10, 2, ALPHA)}")
    out = ROOT / "results" / "nulls.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"alpha": ALPHA, "rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
