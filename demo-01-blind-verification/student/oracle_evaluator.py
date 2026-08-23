#!/usr/bin/env python3
"""
Oracle Evaluator - Evaluates commitments against sealed oracles.

Run AFTER agents have produced their commitments.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


class OracleEvaluator:
    """Evaluates agent commitments against ground truth oracles."""

    def __init__(self, oracles_path: Path):
        self.oracles = json.loads(oracles_path.read_text())["sealed_oracles"]

    def evaluate(self, scenario_id: str, commitment: str) -> Dict[str, Any]:
        """Evaluate a single commitment."""
        oracle = self.oracles[scenario_id]

        # Write commitment to temp file for eval script
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(commitment)
            temp_path = f.name

        try:
            # Replace commitment placeholder in eval script
            eval_script = oracle["eval_script"].replace("'commitment.patch'", f"'{temp_path}'").replace("'commitment.txt'", f"'{temp_path}'")

            result = subprocess.run(
                ["bash", "-c", eval_script],
                capture_output=True,
                text=True,
                timeout=10
            )

            passed = "PASS" in result.stdout
            output = result.stdout.strip()

        finally:
            Path(temp_path).unlink(missing_ok=True)

        return {
            "scenario_id": scenario_id,
            "passed": passed,
            "oracle_type": oracle["oracle_type"],
            "output": output
        }

    def evaluate_all(self, commitments: Dict[str, str]) -> Dict[str, Any]:
        """Evaluate all commitments."""
        results = {}
        for scenario_id, commitment in commitments.items():
            if scenario_id in self.oracles:
                results[scenario_id] = self.evaluate(scenario_id, commitment)
            else:
                results[scenario_id] = {"passed": False, "error": "No oracle for scenario"}

        passed_count = sum(1 for r in results.values() if r.get("passed", False))
        total = len(results)

        return {
            "results": results,
            "summary": {
                "passed": passed_count,
                "total": total,
                "rate": passed_count / total if total > 0 else 0
            }
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--commitments", required=True, help="Path to commitments JSON")
    parser.add_argument("--oracles", default="fixtures/sealed_oracles.json")
    parser.add_argument("--output", default="results/evaluation.json")
    args = parser.parse_args()

    commitments = json.loads(Path(args.commitments).read_text())
    evaluator = OracleEvaluator(Path(args.oracles))
    results = evaluator.evaluate_all(commitments)

    Path(args.output).parent.mkdir(exist_ok=True)
    Path(args.output).write_text(json.dumps(results, indent=2))

    print(f"Evaluation complete: {results['summary']['passed']}/{results['summary']['total']} passed")
    for sid, res in results["results"].items():
        status = "PASS" if res.get("passed") else "FAIL"
        print(f"  {sid}: {status}")