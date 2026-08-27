#!/usr/bin/env python3
"""Generate the human-readable summary table for demo-03."""

import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from eval_invariants import EvaluationInvariants, save_results  # noqa: E402


def main() -> None:
    inv = EvaluationInvariants(base_dir / "fixtures" / "eval_data.json")
    results = inv.run_all()

    print("Invariant Summary:")
    print("=" * 60)
    for name, r in results.items():
        if name == "summary":
            continue
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  {status}  {r['invariant']}: {r['details']}")
    print("=" * 60)
    s = results["summary"]
    overall = "ALL PASSED" if s["all_passed"] else f"SOME FAILED ({s['passed_count']}/{s['total']} passed)"
    print(f"Overall: {overall}")

    print()
    print("Headline vs clean-task mean (leaked tasks excluded):")
    for model, v in inv.headline_vs_clean(results["invariant_1_no_leakage"]).items():
        delta = v["clean"] - v["headline"]
        print(f"  {model:16} {v['headline']:.2f} -> {v['clean']:.2f}  ({delta:+.2f})")

    save_results(results, base_dir)


if __name__ == "__main__":
    main()
