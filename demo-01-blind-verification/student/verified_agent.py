#!/usr/bin/env python3
"""
Verified Agent - Blind Commitment Workflow

This agent commits to a fix WITHOUT seeing the oracle.
It only sees the task description, the ticket context and the codebase
snippet in fixtures/scenarios.json, and it publishes a SHA-256 hash of each
commitment BEFORE the oracle is opened, so the commitment cannot be revised
afterwards without detection.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any


def commitment_hash(commitment: str) -> str:
    """Full 256-bit SHA-256 hex digest of the commitment text."""
    return hashlib.sha256(commitment.encode("utf-8")).hexdigest()


class VerifiedAgent:
    """Agent that makes blind commitments."""

    def __init__(self, scenarios_path: Path):
        self.scenarios = json.loads(scenarios_path.read_text())["scenarios"]
        # NOTE: Does NOT load oracles

    def analyze_task(self, scenario: Dict[str, Any]) -> str:
        """
        Analyze the task and produce a commitment.
        In a real system, this would use an LLM or rule-based analyzer.
        For teaching, we implement simple pattern matching on the ticket text
        (task + context). The toy agent knows three fix patterns; anything else
        yields an explicit "unable to determine" commitment rather than a guess.
        """
        text = (scenario["task"] + " " + scenario["context"]).lower()
        codebase = scenario["codebase"]["files"]

        # Pattern 1: missing authorization check
        if "authorization" in text:
            return "if user_id != current_user.id:\n    raise AuthorizationError()\n"

        # Pattern 2: vulnerable dependency -> pin the patched version
        if "cve" in text or "dependency" in text:
            for fname, content in codebase.items():
                if "requirements" in fname:
                    for line in content.strip().split("\n"):
                        if line.startswith("requests=="):
                            # Simulate updating to the patched version
                            return "requests==2.31.0\n"
            return "# Unable to determine fix blindly\n"

        # Pattern 3: poisoned config -> restore the poisoned line from backup
        if "poisoned" in text or "corrupted" in text or "backup" in text:
            for fname, content in codebase.items():
                if "backup" in fname or ".bak" in fname:
                    for line in content.split("\n"):
                        if "password" in line:
                            return line.strip() + "\n"
            return "# Unable to determine fix blindly\n"

        # Default: the agent does not know this fix pattern. It says so instead
        # of guessing. (restored-004 needs the code to be read, which this
        # text-only heuristic does not do -- see Exercise 1.1.)
        return "# Unable to determine fix blindly\n"

    def solve(self, scenario_id: str) -> Dict[str, Any]:
        """Solve a scenario blindly."""
        scenario = next(s for s in self.scenarios if s["id"] == scenario_id)

        # Produce commitment WITHOUT seeing oracle
        commitment = self.analyze_task(scenario)

        # Create binding cryptographic commitment hash (full 256-bit SHA-256)
        full_hash = commitment_hash(commitment)

        return {
            "scenario_id": scenario_id,
            "commitment": commitment,
            "commitment_hash": full_hash,
            "short_hash": full_hash[:16],
            "method": "blind_heuristic",
            "blind": True
        }


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    scenarios_path = base_dir / "fixtures" / "scenarios.json"

    agent = VerifiedAgent(scenarios_path)

    commitments = {}
    hashes = {}
    for scenario in agent.scenarios:
        result = agent.solve(scenario["id"])
        commitments[scenario["id"]] = result["commitment"]
        hashes[scenario["id"]] = result["commitment_hash"]
        print(f"{scenario['id']}: {result['commitment'].strip()} (sha256: {result['commitment_hash']})")

    # Save commitments for oracle evaluation, and PUBLISH the hashes separately.
    # The evaluator checks every commitment against this ledger before opening
    # the oracle; editing a commitment after this point is detected.
    (base_dir / "commitments_verified.json").write_text(json.dumps(commitments, indent=2))
    (base_dir / "commitment_hashes_verified.json").write_text(json.dumps(hashes, indent=2))
    print("Published commitment hashes to commitment_hashes_verified.json")
