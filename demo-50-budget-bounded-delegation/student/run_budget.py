"""Replay the demo 50 synthetic plans through the budget ledger and write results/delegation_budget.json."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from delegation_budget import INVARIANTS, replay, requested_spend  # noqa: E402


def main() -> int:
    fixture = json.loads((ROOT / "fixtures" / "synthetic_plans.json").read_text(encoding="utf-8"))
    print("Demo 50: budget-attenuated delegation (synthetic fixtures)\n")
    for key, text in INVARIANTS.items():
        print(f"  {key}  {text}")
    print()
    rows = []
    for plan in fixture["plans"]:
        ledger = replay(plan)
        audit = ledger.audit()
        rows.append({
            "plan": plan["name"],
            "requested_spend": requested_spend(plan),
            "total_spent": ledger.total_spent(),
            "root_budget": plan["root_budget"],
            "denials": [
                {"op": d.op, "node": d.node, "requested": d.requested, "reason": d.reason}
                for d in ledger.denials()
            ],
            "invariants": audit,
        })
        print(
            f"{plan['name']}: requested spend {requested_spend(plan)}, spent {ledger.total_spent()} "
            f"of root budget {plan['root_budget']}, denials {len(ledger.denials())}, "
            f"invariants {'all hold' if all(audit.values()) else audit}"
        )
        for d in ledger.denials():
            print(f"    denied {d.op} {d.node} ({d.requested}): {d.reason}")
    out = ROOT / "results" / "delegation_budget.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2) + "\n")
    print("\nFixtures are placeholders that exercise the ledger; they are not results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
