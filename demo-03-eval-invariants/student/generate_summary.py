#!/usr/bin/env python3
"""Generate summary table for demo-03."""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "student"))
from eval_invariants import EvaluationInvariants

def main():
    invariants = EvaluationInvariants(Path("fixtures/eval_data.json"))
    results = invariants.run_all()

    print("Invariant Summary:")
    print("=" * 60)
    for k, v in results.items():
        if k == "summary":
            continue
        status = "PASS" if v["passed"] else "FAIL"
        details = v.get("details", v.get("issues", ""))
        print(f"  {status}  {v['invariant']}: {details}")
    print("=" * 60)
    overall = "ALL PASSED" if results["summary"]["all_passed"] else "SOME FAILED"
    print(f"Overall: {overall}")

    # Save results
    Path("results/invariant_results.json").parent.mkdir(exist_ok=True)
    Path("results/invariant_results.json").write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()