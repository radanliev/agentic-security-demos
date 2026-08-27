#!/usr/bin/env python3
"""Generate inclusion results for demo-08 and check both agents against the fixture's expectations."""

import json
import platform
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from inclusiontrap import GuardedInclusionAgent, VulnerableInclusionAgent, build  # noqa: E402


def git_commit() -> str:
    """Short git commit of the checkout, or 'local' outside a repository."""
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def environment() -> str:
    return f"Python {platform.python_version()}, {platform.system()} {platform.release()}"


def main():
    data = json.loads((base_dir / "fixtures" / "inclusion.json").read_text())
    v_host, v_scope = build(data)
    g_host, g_scope = build(data)
    vulnerable = VulnerableInclusionAgent(v_host, v_scope)
    guarded = GuardedInclusionAgent(g_host, g_scope)

    results = []
    mismatches = []
    for s in data["inclusion_scenarios"]:
        v = vulnerable.process(s)
        g = guarded.process(s)
        exp = s["expected"]
        g_summary = f"{g.action}: {g.reason.split(':')[0].split(' ')[0]}"
        ok = v.action == exp["vulnerable"] and g_summary == exp["guarded"]
        if not ok:
            mismatches.append(f"{s['id']}: vulnerable {v.action}/{exp['vulnerable']}, guarded {g_summary}/{exp['guarded']}")
        results.append({
            "scenario": s["id"],
            "vulnerable_action": v.action,
            "vulnerable_host_calls": v.host_calls,
            "action": g.action,
            "reason": g.reason,
            "provenance": g.provenance.value,
            "host_calls": g.host_calls,
            "expected": exp,
            "ok": ok,
        })

    privileged = g_host.privileged_calls()
    out = {
        "demo": "demo-08-inclusiontrap",
        "experiment": "inclusion_scope",
        "seed": data["seed"],
        "commit": git_commit(),
        "environment": environment(),
        "command": "make demo DEMO=08",
        "result": "pass" if not mismatches and not privileged else "fail",
        "notes": "Synthetic teaching fixture; simulated host; both agents checked against the expected outcome per scenario",
        "guarded_host_call_counts": g_host.counts(),
        "vulnerable_host_call_counts": v_host.counts(),
        "guarded_privileged_calls": [f"{a}({b!r})" for a, b in privileged],
        "results": results,
    }

    out_path = base_dir / "results" / "inclusion_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    if mismatches or privileged:
        print("\nMISMATCH:\n  " + "\n  ".join(mismatches + [f"guarded privileged call: {c}" for c in privileged]), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
