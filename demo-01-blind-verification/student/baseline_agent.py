#!/usr/bin/env python3
"""
Baseline Agent - No Blind Verification

This agent sees the test condition before producing a fix: it opens the
sealed oracle file and copies the expected commitment out of it.
It demonstrates why an unblinded score measures oracle leakage, not capability.
"""

import json
from pathlib import Path
from typing import Dict, Any


class BaselineAgent:
    """Agent that cheats by reading the oracle first."""

    def __init__(self, scenarios_path: Path, oracles_path: Path):
        self.scenarios = json.loads(scenarios_path.read_text())["scenarios"]
        # CHEAT: the answer key is loaded into the agent's input surface.
        self.oracles = json.loads(oracles_path.read_text())["sealed_oracles"]

    def solve(self, scenario_id: str) -> Dict[str, Any]:
        """Solve a scenario by copying the expected answer out of the oracle."""
        oracle = self.oracles[scenario_id]
        commitment = oracle["expected_commitment"]

        return {
            "scenario_id": scenario_id,
            "commitment": commitment,
            "method": "baseline_cheat",
            "blind": False
        }


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    scenarios_path = base_dir / "fixtures" / "scenarios.json"
    oracles_path = base_dir / "fixtures" / "sealed_oracles.json"

    agent = BaselineAgent(scenarios_path, oracles_path)

    output = {}
    for scenario in agent.scenarios:
        result = agent.solve(scenario["id"])
        output[scenario["id"]] = result["commitment"]
        print(f"{scenario['id']}: {result['commitment'].strip()}")

    # Save commitments for oracle evaluation
    (base_dir / "commitments_baseline.json").write_text(json.dumps(output, indent=2))
