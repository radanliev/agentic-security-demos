"""Run the demo 49 checker over the synthetic fixture traces and write results/tier_invariance.json."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from tier_invariance import RULES, check_trace  # noqa: E402


def main() -> int:
    fixture = json.loads((ROOT / "fixtures" / "synthetic_traces.json").read_text(encoding="utf-8"))
    policy = fixture["policy"]
    print("Demo 49: authority invariance across model-tier transitions (synthetic fixtures)\n")
    for rule, text in RULES.items():
        print(f"  {rule}  {text}")
    print()
    rows = []
    for trace in fixture["traces"]:
        found = check_trace(trace, policy)
        rows.append({
            "trace": trace["name"],
            "violations": [{"step": v.step, "rule": v.rule, "detail": v.detail} for v in found],
        })
        status = "no violations" if not found else f"{len(found)} violation(s)"
        print(f"{trace['name']}: {status}")
        for v in found:
            print(f"    step {v.step}  {v.rule}  {v.detail}")
    out = ROOT / "results" / "tier_invariance.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2) + "\n")
    print("\nFixtures are placeholders that exercise the checker; they are not results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
