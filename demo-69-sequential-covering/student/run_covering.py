"""Run the Demo-69 toy: learn a sequential-covering decision list."""

import json
from pathlib import Path
from covering import accuracy, learn

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    data = json.loads((ROOT / "fixtures" / "urls.json").read_text())
    rules, default = learn(data["rows"], data["positive_label"])
    acc = accuracy(data["rows"], rules, default)
    print(f"rows {len(data['rows'])}  rules {len(rules)}  default {default}  accuracy {acc:.3f}")
    for rule in rules:
        print(f"if {rule['feature']} then {rule['label']} (precision {rule['precision']:.3f}, support {rule['support']})")
    out = ROOT / "results" / "covering.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"rules": rules, "default": default, "accuracy": acc, "n_rows": len(data["rows"])}, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
