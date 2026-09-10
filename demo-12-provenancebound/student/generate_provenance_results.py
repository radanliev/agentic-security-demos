#!/usr/bin/env python3
"""Generate provenance results for demo-12.

Runs both pipelines over fixtures/calendar.json, compares every verdict with the
fixture's `expected` answer key (which the pipelines never read), and writes
results/provenance_results.json.  `result` is computed ("pass" only if every
expectation holds); the process exits 1 on any mismatch.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "student"))
from provenancebound import (  # noqa: E402
    NaiveBaseline,
    ProvenanceBoundGuarded,
    load_cases,
)

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
    data = json.loads((base_dir / "fixtures" / "calendar.json").read_text())
    trusted = tuple(data.get("trusted_domains", ["internal.example", "trusted.example"]))
    cases = load_cases(data)

    baseline = NaiveBaseline().run(cases, trusted)
    guarded = ProvenanceBoundGuarded().run(cases, trusted)
    by_id = {r.case_id: r for r in guarded["results"]}

    per_case, mismatches = [], []
    for case in cases:
        observed_baseline = [
            a for a in baseline["actions_taken"]
            if a in (f"allow:{case.id}", f"not_requested:{case.id}")
        ]
        r = by_id[case.id]
        if r.decision == "allowed":
            observed_guarded = {
                "provenance_trusted": r.provenance.trusted,
                "suspicious": r.detection.suspicious,
                "attempted": r.observation.attempted,
                "decision": "allowed",
            }
        elif r.decision == "blocked":
            observed_guarded = {
                "provenance_trusted": r.provenance.trusted,
                "suspicious": r.detection.suspicious,
                "attempted": r.observation.attempted,
                "decision": f"blocked: {r.reason}",
            }
        else:
            observed_guarded = {
                "provenance_trusted": r.provenance.trusted,
                "suspicious": r.detection.suspicious,
                "attempted": r.observation.attempted,
                "decision": "not_requested",
            }
        observed = {"baseline": observed_baseline, "guarded": observed_guarded}
        expected = data["expected"][case.id]
        if observed != expected:
            mismatches.append(f"{case.id}: expected {expected}, got {observed}")
        per_case.append({"case": case.id, "name": case.name, "observed": observed,
                         "expected": expected, "matches_expected": observed == expected})

    return {
        "demo": "demo-12-provenancebound",
        "experiment": "provenance_authorization",
        "seed": data.get("seed", 42),
        "commit": get_git_commit(),
        "environment": capture_environment(),
        "command": "make demo DEMO=12",
        "result": "pass" if not mismatches else "fail",
        "notes": "Synthetic teaching fixture; verdicts compared with the fixture's answer key",
        "summary": {
            "cases": len(cases),
            "baseline_allowed": [a for a in baseline["actions_taken"] if a.startswith("allow:")],
            "baseline_not_requested": [a for a in baseline["actions_taken"] if a.startswith("not_requested:")],
            "guarded_allowed": guarded["actions_taken"],
            "guarded_blocked": guarded["actions_blocked"],
            "guarded_not_requested": [c.id for c in cases if by_id[c.id].decision == "not_requested"],
        },
        "results": [{"case": r.case_id, "provenance": r.provenance.source,
                     "trusted": r.provenance.trusted, "suspicious": r.detection.suspicious,
                     "indicators": list(r.detection.indicators),
                     "attempted": r.observation.attempted, "decision": r.decision,
                     "reason": r.reason} for r in guarded["results"]],
        "actions_taken": guarded["actions_taken"],
        "actions_blocked": guarded["actions_blocked"],
        "mismatches": mismatches,
        "per_case": per_case,
    }


def main() -> int:
    out = run()
    out_path = BASE_DIR / "results" / "provenance_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    if out["mismatches"]:
        print("\nMISMATCH against fixture expectations:", *out["mismatches"], sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
