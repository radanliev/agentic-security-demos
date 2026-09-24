#!/usr/bin/env python3
"""Cue-following assessor for Demo 13.

This toy assessor trusts the derived coverage cue whenever one is shown:
it nominates the cued file. With no cue it falls back to the shared
heuristic. It never sees the answer key.
"""

from typing import Dict

from heuristic import heuristic_pick


class CueFollower:
    """Assessor that follows the coverage cue when present."""

    def solve(self, files: Dict[str, str], cue: Dict[str, object]) -> str:
        """Nominate one filename given file contents and a cue dict."""
        if cue.get("kind") in ("true", "wrong"):
            return str(cue["points_to"])
        return heuristic_pick(files)


if __name__ == "__main__":
    import json
    from pathlib import Path

    demo = Path(__file__).resolve().parent.parent
    instances = json.loads((demo / "fixtures" / "instances.json").read_text())["instances"]
    agent = CueFollower()
    for inst in instances:
        print(f"{inst['id']}: cue={inst['cue']['kind']} -> {agent.solve(inst['files'], inst['cue'])}")
