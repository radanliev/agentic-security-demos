"""Run the Demo-65 toy: spectral versus Frobenius Lipschitz products."""

import json
from pathlib import Path
from lipschitz import bounds

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "maps.json").read_text())
    rows = []
    for item in data["maps"]:
        result = bounds(item["W1"], item["W2"])
        result["id"] = item["id"]
        result["frobenius_dominates"] = result["frobenius_product"] + 1e-12 >= result["spectral_product"]
        rows.append(result)
        print(f"{item['id']:<4} spectral={result['spectral_product']:.4f} frobenius={result['frobenius_product']:.4f} ok={result['frobenius_dominates']}")
    out = ROOT / "results" / "lipschitz.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
