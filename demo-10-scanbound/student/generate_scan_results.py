#!/usr/bin/env python3
"""Generate scan results for demo-10.

Runs both scanners over fixtures/scanbound.json, compares every verdict with the
fixture's `expected` answer key (which the scanners never read), and writes
results/scan_results.json.  `result` is computed ("pass" only if every
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
from scanbound import SimulatedScanner, UnconstrainedScanner, build_guarded, load_checks  # noqa: E402

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
    data = json.loads((base_dir / "fixtures" / "scanbound.json").read_text())
    checks = load_checks(data)

    baseline = UnconstrainedScanner(checks).run(SimulatedScanner(data["poisoned_scanner_output"]))
    guarded = build_guarded(data).run(checks, SimulatedScanner(data["poisoned_scanner_output"]))

    findings = {r.check_id: r for r in guarded["results"]}
    blocked = {b["check"]: b["reason"] for b in guarded["blocked_checks"]}
    reported = {a.split(":", 1)[1] for a in guarded["actions_taken"]}
    report_blocked = {a.split(":", 1)[1].split(" (")[0]: a.split(" (", 1)[1].rstrip(")") for a in guarded["actions_blocked"]}

    per_check, mismatches = [], []
    for check in checks:
        observed_baseline = [a.split(" [", 1)[0] for a in baseline["actions_taken"]
                             if a.startswith(f"report:{check.id}") or a.endswith(f"from {check.id} output")]
        if check.id in findings:
            r = findings[check.id]
            observed_guarded = {"executed": True, "taint": r.taint.value, "taint_reasons": r.taint_reasons,
                                "report": "allowed" if check.id in reported else f"blocked: {report_blocked.get(check.id, '?')}"}
        else:
            observed_guarded = {"executed": False, "blocked": blocked.get(check.id, "?")}
        observed = {"baseline": observed_baseline, "guarded": observed_guarded}
        expected = data["expected"][check.id]
        if observed != expected:
            mismatches.append(f"{check.id}: expected {expected}, got {observed}")
        per_check.append({"check": check.id, "target": str(check.target), "observed": observed,
                          "expected": expected, "matches_expected": observed == expected})

    return {
        "demo": "demo-10-scanbound",
        "experiment": "scope_control",
        "seed": data.get("seed", 42),
        "commit": get_git_commit(),
        "environment": capture_environment(),
        "command": "make demo DEMO=10",
        "result": "pass" if not mismatches else "fail",
        "notes": "Synthetic teaching fixture; verdicts compared with the fixture's answer key",
        "summary": {
            "checks": len(checks),
            "baseline_executed": baseline["executed"],
            "baseline_followed_instructions": [a for a in baseline["actions_taken"] if not a.startswith("report:")],
            "guarded_executed": guarded["executed"],
            "guarded_blocked_checks": guarded["blocked_checks"],
            "guarded_actions_taken": guarded["actions_taken"],
            "guarded_actions_blocked": guarded["actions_blocked"],
        },
        "results": [{"check": r.check_id, "target": str(r.target), "finding": r.finding[:80],
                     "taint": r.taint.value, "taint_reasons": r.taint_reasons} for r in guarded["results"]],
        "blocked_checks": guarded["blocked_checks"],
        "actions_taken": guarded["actions_taken"],
        "actions_blocked": guarded["actions_blocked"],
        "mismatches": mismatches,
        "per_check": per_check,
    }


def main() -> int:
    out = run()
    out_path = BASE_DIR / "results" / "scan_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    if out["mismatches"]:
        print("\nMISMATCH against fixture expectations:", *out["mismatches"], sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
