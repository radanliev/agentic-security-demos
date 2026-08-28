#!/usr/bin/env python3
"""Generate intercept results for demo-09.

Runs both agents over fixtures/traffic.json, compares every verdict with the
fixture's `expected` answer key (which the agents never read), checks that the
detector found every planted `injection`, and writes results/intercept_results.json.
`result` is computed ("pass" only if every expectation holds); the process exits
1 on any mismatch so the file can never silently claim a pass.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "student"))
from interceptbound import BaselineAgent, TaintAwareAgent, load_frames  # noqa: E402

try:  # prefer the course-wide helpers when the repository's shared/ package is importable
    sys.path.insert(0, str(BASE_DIR.parent))
    from shared.result_schema import capture_environment, get_git_commit  # type: ignore
except Exception:  # pragma: no cover - fallback for a copied demo folder
    def get_git_commit() -> str:
        try:
            return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=BASE_DIR,
                                           stderr=subprocess.DEVNULL, text=True).strip()
        except Exception:
            return "local"

    def capture_environment() -> str:
        return f"Python {sys.version.split()[0]}, {platform.system()} {platform.release()}"


def run(base_dir: Path = BASE_DIR) -> dict:
    data = json.loads((base_dir / "fixtures" / "traffic.json").read_text())
    frames = load_frames(data)
    baseline = BaselineAgent()
    guarded = TaintAwareAgent(data["scope_policy"], data["ephemeral_buffer"])

    results, mismatches = [], []
    for raw, frame in zip(data["traffic_frames"], frames):
        b = baseline.process(frame)
        g = guarded.process(frame)
        observed = {
            "baseline": [a["action"] for a in b["actions"]],
            "guarded_allowed": [a["action"] for a in g["actions"]],
            "guarded_blocked": [x["action"] for x in g["blocked"]],
        }
        expected = raw["expected"]
        for key in expected:
            if observed[key] != expected[key]:
                mismatches.append(f"{frame.id}.{key}: expected {expected[key]}, got {observed[key]}")
        planted = raw.get("injection")
        detected = [x["field"] for x in g["blocked"] if x["action"] == "process_injection"]
        if planted and g["exit"] == "ok" and not detected:
            mismatches.append(f"{frame.id}: planted injection not detected")
        results.append({
            "frame": frame.id,
            "provenance": frame.provenance.value,
            "taint": frame.taint.value,
            "exit": g["exit"],
            "parsed_fields": g["parsed_fields"],
            "baseline_actions": b["actions"],
            "guarded_actions": g["actions"],
            "guarded_blocked": g["blocked"],
            "expected": expected,
            "matches_expected": all(observed[k] == expected[k] for k in expected),
        })

    stats = guarded.buffer.stats
    return {
        "demo": "demo-09-interceptbound",
        "experiment": "taint_tracking",
        "seed": data.get("seed", 42),
        "commit": get_git_commit(),
        "environment": capture_environment(),
        "command": "make demo DEMO=09",
        "result": "pass" if not mismatches else "fail",
        "notes": "Synthetic teaching fixture; verdicts compared with the fixture's answer key",
        "summary": {
            "frames": len(frames),
            "baseline_actions": sum(len(r["baseline_actions"]) for r in results),
            "guarded_allowed": sum(len(r["guarded_actions"]) for r in results),
            "guarded_blocked": sum(len(r["guarded_blocked"]) for r in results),
            "block_reasons": sorted({x["reason"].split(":")[0] for r in results for x in r["guarded_blocked"]}),
            "buffer": {"live_entries_after_run": len(guarded.buffer), **stats},
        },
        "mismatches": mismatches,
        "results": results,
    }


def main() -> int:
    out = run()
    out_path = BASE_DIR / "results" / "intercept_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    if out["mismatches"]:
        print("\nMISMATCH against fixture expectations:", *out["mismatches"], sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
