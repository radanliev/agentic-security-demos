#!/usr/bin/env python3
"""
Oracle Evaluator - Evaluates commitments against sealed oracles.

Run AFTER agents have produced their commitments.

If a commitment-hash ledger is supplied (--hashes), every commitment is first
checked against the hash that was published before the oracle was opened.
A commitment whose hash does not match the ledger is rejected as post-hoc.
"""

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional


class OracleEvaluator:
    """Evaluates agent commitments against ground truth oracles."""

    def __init__(self, oracles_path: Path):
        self.oracles = json.loads(oracles_path.read_text())["sealed_oracles"]

    def evaluate(self, scenario_id: str, commitment: str) -> Dict[str, Any]:
        """Evaluate a single commitment by running the oracle's eval script."""
        oracle = self.oracles[scenario_id]

        # Write commitment to temp file for eval script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(commitment)
            temp_path = f.name

        try:
            # Replace commitment placeholder in eval script
            eval_script = (oracle["eval_script"]
                           .replace("'commitment.patch'", f"'{temp_path}'")
                           .replace("'commitment.txt'", f"'{temp_path}'"))

            result = subprocess.run(
                ["bash", "-c", eval_script],
                capture_output=True,
                text=True,
                timeout=10
            )
        finally:
            Path(temp_path).unlink(missing_ok=True)

        output = result.stdout.strip()
        verdict = output.split()[-1] if output else ""
        record: Dict[str, Any] = {
            "scenario_id": scenario_id,
            "passed": verdict == "PASS",
            "oracle_type": oracle["oracle_type"],
            "output": output,
        }
        # An oracle that crashed (syntax error in the commitment, python3
        # missing, ...) is an ERROR, not a silent FAIL: record why.
        if result.returncode != 0 or verdict not in ("PASS", "FAIL"):
            record["error"] = (result.stderr.strip().splitlines() or ["oracle produced no verdict"])[-1]
        return record

    def evaluate_all(self, commitments: Dict[str, str],
                     published_hashes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Evaluate all commitments (optionally verifying them against a hash ledger)."""
        results = {}
        for scenario_id, commitment in commitments.items():
            if published_hashes is not None:
                actual = hashlib.sha256(commitment.encode("utf-8")).hexdigest()
                expected = published_hashes.get(scenario_id)
                if actual != expected:
                    results[scenario_id] = {
                        "scenario_id": scenario_id,
                        "passed": False,
                        "error": "commitment_hash_mismatch: commitment was changed after its hash was published"
                                 if expected else "commitment_hash_missing: no hash was published for this scenario",
                    }
                    continue
            if scenario_id in self.oracles:
                results[scenario_id] = self.evaluate(scenario_id, commitment)
            else:
                results[scenario_id] = {"scenario_id": scenario_id, "passed": False,
                                        "error": "No oracle for scenario"}

        passed_count = sum(1 for r in results.values() if r.get("passed", False))
        total = len(results)

        return {
            "results": results,
            "hash_ledger_checked": published_hashes is not None,
            "summary": {
                "passed": passed_count,
                "total": total,
                "rate": passed_count / total if total > 0 else 0
            }
        }


if __name__ == "__main__":
    import argparse

    base_dir = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--commitments", required=True, help="Path to commitments JSON")
    parser.add_argument("--hashes", default=None,
                        help="Path to the commitment-hash ledger published before the oracle was opened")
    parser.add_argument("--oracles", default=str(base_dir / "fixtures" / "sealed_oracles.json"))
    parser.add_argument("--output", default="results/evaluation.json")
    args = parser.parse_args()

    commitments = json.loads(Path(args.commitments).read_text())
    published = json.loads(Path(args.hashes).read_text()) if args.hashes else None
    evaluator = OracleEvaluator(Path(args.oracles))
    results = evaluator.evaluate_all(commitments, published)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(results, indent=2))

    ledger = "hash ledger verified" if published is not None else "no hash ledger (unbound commitments)"
    print(f"Evaluation complete: {results['summary']['passed']}/{results['summary']['total']} passed ({ledger})")
    for sid, res in results["results"].items():
        if res.get("passed"):
            status = "PASS"
        elif "error" in res:
            status = f"ERROR ({res['error']})"
        else:
            status = "FAIL"
        print(f"  {sid}: {status}")
