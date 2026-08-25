#!/usr/bin/env python3
"""
Verified Agent - Blind Commitment Workflow

This agent commits to a fix WITHOUT seeing the oracle.
It only sees the task description and codebase context.
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import Dict, Any, List


class VerifiedAgent:
    """Agent that makes blind commitments."""

    def __init__(self, scenarios_path: Path):
        self.scenarios = json.loads(scenarios_path.read_text())["scenarios"]
        # NOTE: Does NOT load oracles

    def analyze_task(self, scenario: Dict[str, Any]) -> str:
        """
        Analyze the task and produce a commitment.
        In a real system, this would use an LLM or rule-based analyzer.
        For teaching, we implement simple pattern matching.
        """
        task = scenario["task"].lower()
        context = scenario["context"].lower()
        codebase = scenario["codebase"]["files"]

        # Simple heuristic-based fixing (deterministic, no oracle access)
        if "authorization" in task or "authorization" in context:
            return "if user_id != current_user.id:\n    raise AuthorizationError()\n"

        if "cve" in task or "dependency" in task or "update" in task:
            # Look for requirements.txt
            for fname, content in codebase.items():
                if "requirements" in fname:
                    lines = content.strip().split("\n")
                    for line in lines:
                        if "requests==" in line:
                            # Simulate updating to patched version
                            return "requests==2.31.0\n"
            return "requests==2.31.0\n"

        if "poisoned" in task or "corrupted" in task or "backup" in task:
            # Restore from backup
            for fname, content in codebase.items():
                if "backup" in fname or ".bak" in fname:
                    # Extract the password line from backup
                    for line in content.split("\n"):
                        if "password" in line:
                            return line.strip() + "\n"
            return "password: 'secure_backup_value'\n"

        if "mfa" in task or "restored" in task or "re-enabled" in task:
            return "return user.mfa_enabled\n"

        # Default: return a comment indicating uncertainty
        return "# Unable to determine fix blindly\n"

    def solve(self, scenario_id: str) -> Dict[str, Any]:
        """Solve a scenario blindly."""
        scenario = next(s for s in self.scenarios if s["id"] == scenario_id)

        # Produce commitment WITHOUT seeing oracle
        commitment = self.analyze_task(scenario)

        # Create binding cryptographic commitment hash (full 256-bit SHA-256)
        full_hash = hashlib.sha256(commitment.encode()).hexdigest()

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

    for scenario in agent.scenarios:
        result = agent.solve(scenario["id"])
        print(f"{scenario['id']}: {result['commitment'].strip()} (hash: {result['commitment_hash']})")

    # Save commitments for oracle evaluation
    output = {r["scenario_id"]: r["commitment"] for r in
              [agent.solve(s["id"]) for s in agent.scenarios]}
    (base_dir / "commitments_verified.json").write_text(json.dumps(output, indent=2))