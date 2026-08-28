#!/usr/bin/env python3
"""Generate drift results for demo-02 in the standardized result schema."""

import json
import platform
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from policy_gate import PolicyGate, outcome_matches, waiver_from_scenario  # noqa: E402


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def main() -> None:
    aibom_path = base_dir / "fixtures" / "aibom.json"
    gate = PolicyGate(aibom_path)
    data = json.loads(aibom_path.read_text())
    results = []
    for s in data["drift_scenarios"]:
        r = gate.evaluate_system(s["runtime_capabilities"], waiver_from_scenario(s))
        results.append({
            "scenario": s["id"],
            "expected": s["expected"],
            "compliant": r["compliant"],
            "drift_detected": r["drift_detected"],
            "waiver_accepted": r["waiver"]["accepted"] if "waiver" in r else None,
            "matches_expected": outcome_matches(s["expected"], r),
        })

    output = {
        "demo": "demo-02-supply-chain-aibom",
        "experiment": "drift_detection",
        "seed": 42,
        "commit": git_commit(),
        "environment": f"Python {platform.python_version()}, {platform.system()}",
        "command": "make demo DEMO=02",
        # Computed, not asserted: the run passes only if every scenario behaved as labelled.
        "result": "pass" if all(r["matches_expected"] for r in results) else "fail",
        "notes": "Synthetic teaching fixture; evaluated at fixture evaluation_time " + data.get("evaluation_time", "(real clock)"),
        "scenarios": results,
    }
    out_path = base_dir / "results" / "drift_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
