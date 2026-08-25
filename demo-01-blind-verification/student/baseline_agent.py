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

        # CHEAT: Read the expected fix from hidden oracle / ground truth
        hidden = scenario.get("hidden_oracle", {})
        if hidden.get("type") == "patch" or oracle.get("oracle_type") == "patch":
            expected = hidden.get("expected_fix")
            if not expected:
                if "AuthorizationError" in oracle.get("eval_script", ""):
                    expected = "if user_id != current_user.id:\n    raise AuthorizationError()"
                elif "secure_backup_value" in oracle.get("eval_script", ""):
                    expected = "password: 'secure_backup_value'"
                else:
                    expected = ""
            commitment = f"{expected}\n"
        else:
            expected = hidden.get("expected_output")
            if not expected:
                if "requests==" in oracle.get("eval_script", ""):
                    expected = "requests==2.31.0"
                elif "return user.mfa_enabled" in oracle.get("eval_script", ""):
                    expected = "return user.mfa_enabled"
                else:
                    expected = ""
            commitment = f"{expected}\n"

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

    for scenario in agent.scenarios:
        result = agent.solve(scenario["id"])
        print(f"{scenario['id']}: {result['commitment'].strip()}")

    # Save commitments for oracle evaluation
    output = {r["scenario_id"]: r["commitment"] for r in
              [agent.solve(s["id"]) for s in agent.scenarios]}
    (base_dir / "commitments_baseline.json").write_text(json.dumps(output, indent=2))