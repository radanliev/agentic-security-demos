"""Run the Demo-64 toy: open-set NCM versus forced nearest neighbour."""

import json
from pathlib import Path
from ncm import class_means, predict_forced_nn, predict_ncm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "patterns.json").read_text())
    means = class_means(data["train"])
    rows = []
    for query in data["queries"]:
        ncm = predict_ncm(query["vec"], means, data["threshold"])
        forced = predict_forced_nn(query["vec"], data["train"])
        rows.append({
            "id": query["id"], "true": query["true"], "ncm": ncm["label"],
            "ncm_rejected": ncm["rejected"], "forced": forced["label"],
            "ncm_ok": ncm["label"] == query["true"], "forced_ok": forced["label"] == query["true"],
        })
        print(f"{query['id']:<4} true={query['true']:<8} ncm={ncm['label']:<8} forced={forced['label']}")
    out = ROOT / "results" / "ncm.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"threshold": data["threshold"], "rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
