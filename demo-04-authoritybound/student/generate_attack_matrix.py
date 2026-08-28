#!/usr/bin/env python3
"""Generate the attack matrix for demo-04 (3 agents x 5 scenarios).

The matrix is computed by running every agent; `result` is "pass" only if every
tool decision matches the expectation recorded in the fixture.
"""

import json
import platform
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from authoritybound import AGENTS, FIXTURE_PATH, run_matrix  # noqa: E402


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def main() -> int:
    data = json.loads(FIXTURE_PATH.read_text())
    matrix = run_matrix(data)

    mismatches = []
    decisions = 0
    for s in data["scenarios"]:
        for agent, expected in s["expected"].items():
            actual = matrix[agent][s["id"]]
            for tool, status in expected.items():
                decisions += 1
                if actual.get(tool) != status:
                    mismatches.append(f"{agent}/{s['id']}/{tool}: expected {status}, got {actual.get(tool)}")
            for tool in actual:
                if tool not in expected:
                    mismatches.append(f"{agent}/{s['id']}/{tool}: unexpected tool call")

    # Table: one row per scenario, one column per agent, "tool ✓/✗" cells.
    keys = list(AGENTS)
    width = 24
    print("Attack matrix (✓ executed, ✗ blocked):")
    print(f"  {'scenario':24}" + "".join(f"{k:{width}}" for k in keys))
    for s in data["scenarios"]:
        cells = []
        for k in keys:
            cell = " ".join(f"{tool.split('_')[0]} {'✓' if st == 'executed' else '✗'}"
                            for tool, st in matrix[k][s["id"]].items())
            cells.append(f"{cell:{width}}")
        print(f"  {s['id']:24}" + "".join(cells))
    print()
    verdict = "pass" if not mismatches else "fail"
    print(f"result: {verdict} ({decisions - len(mismatches)}/{decisions} tool decisions match the fixture's expectations)")
    for m in mismatches:
        print(f"  MISMATCH {m}")

    out = {
        "demo": "demo-04-authoritybound",
        "experiment": "attack_matrix",
        "seed": data.get("seed", 42),
        "commit": git_commit(),
        "environment": f"Python {platform.python_version()}, {platform.system()} {platform.release()}",
        "command": "make demo DEMO=04",
        "result": verdict,
        "notes": "Synthetic teaching fixture; result computed by comparing every tool decision with the fixture's expected outcomes",
        "mismatches": mismatches,
        "matrix": matrix,
    }
    out_path = base_dir / "results" / "attack_matrix.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"Saved {out_path.relative_to(base_dir)}")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
