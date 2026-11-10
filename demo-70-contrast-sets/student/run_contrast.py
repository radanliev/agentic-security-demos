"""Run the Demo-70 toy: contrast-set growth versus a global top-k baseline."""

import json
from pathlib import Path
from contrast import emerging, top_frequency

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "windows.json").read_text())
    rows = []
    for case in data["cases"]:
        detail, flagged = emerging(case["window_a"], case["window_b"], data["min_support_b"], data["min_growth"])
        baseline = top_frequency(case["window_a"], case["window_b"], data["top_k"])
        rows.append({"id": case["id"], "emerging": flagged, "baseline_top": baseline, "detail": detail})
        print(f"{case['id']:<4} emerging={flagged}  baseline={baseline}")
    out = ROOT / "results" / "contrast.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"min_support_b": data["min_support_b"], "min_growth": data["min_growth"], "rows": rows}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
