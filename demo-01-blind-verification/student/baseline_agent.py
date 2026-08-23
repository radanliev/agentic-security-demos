#!/usr/bin/env python3
"""
Baseline Agent - No Blind Verification

This agent sees the test condition before producing a fix.
It demonstrates why post-hoc explanations are insufficient.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


class BaselineAgent:
    """Agent that cheats by reading the oracle first."""

    def __init__(self, scenarios_path: Path, oracles_path: Path):
        self.scenarios = json.loads(scenarios_path.read_text())["scenarios"]
        self.oracles = json.loads(oracles_path.read_text())["sealed_oracles"]

    def solve(self, scenario_id: str) -> Dict[str, Any]:
        """Solve a scenario by peeking at the oracle."""
        scenario = next(s for s in self.scenarios if s["id"] == scenario_id)
        oracle = self.oracles[scenario_id]

        # CHEAT: Read the expected fix from oracle
        if oracle["oracle_type"] == "patch":
            expected = oracle["eval_script"].split("'")[1]  # Extract expected string
            commitment = f"+    {expected}\n"
        else:
            expected = oracle["eval_script"].split("==")[1].split("'")[1]
            commitment = expected

        return {
            "scenario_id": scenario_id,
            "commitment": commitment,
            "method": "baseline_cheat",
            "blind": False
        }


if __name__ == "__main__":
    scenarios_path = Path("fixtures/scenarios.json")
    oracles_path = Path("fixtures/sealed_oracles.json")

    agent = BaselineAgent(scenarios_path, oracles_path)

    for scenario in agent.scenarios:
        result = agent.solve(scenario["id"])
        print(f"{scenario['id']}: {result['commitment'].strip()}")

    # Save commitments for oracle evaluation
    output = {r["scenario_id"]: r["commitment"] for r in
              [agent.solve(s["id"]) for s in agent.scenarios]}
    Path("commitments_baseline.json").write_text(json.dumps(output, indent=2))