#!/usr/bin/env python3
"""Independent assessor for Demo 13.

This toy assessor ignores the coverage cue entirely and always applies the
shared heuristic. It never sees the answer key.
"""

from typing import Dict

from heuristic import heuristic_pick


class IndependentHeuristic:
    """Assessor that never looks at the cue."""

    def solve(self, files: Dict[str, str], cue: Dict[str, object]) -> str:  # noqa: ARG002
        """Nominate one filename given file contents (cue ignored)."""
        return heuristic_pick(files)


if __name__ == "__main__":
    import json
    from pathlib import Path

    demo = Path(__file__).resolve().parent.parent
    instances = json.loads((demo / "fixtures" / "instances.json").read_text())["instances"]
    agent = IndependentHeuristic()
    for inst in instances:
        print(f"{inst['id']}: heuristic -> {agent.solve(inst['files'], inst['cue'])}")
