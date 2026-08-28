#!/usr/bin/env python3
"""Generate evaluation for demo-06: run both agents over every fixture and compare each decision
with what the fixture itself implies (in scope? carries an injection?). Exits 1 on any mismatch."""

import json
import platform
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from reconscope import ProvenanceAwareReconAgent, VulnerableReconAgent, load_fixtures, parse_source  # noqa: E402


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def expected_for(fixture, scope) -> dict:
    """What a correct run must do with this fixture, derived from the fixture and the policy."""
    host, port = parse_source(fixture["source"])
    in_scope = scope.allows(host, port)
    has_injection = bool(fixture.get("injection"))
    return {
        "scope": "allowed" if in_scope else "blocked",
        "injections_detected": 1 if (in_scope and has_injection) else 0,
        "vulnerable": "execute" if (in_scope and has_injection) else "none",
        "provenance_aware": "log" if (in_scope and has_injection) else "none",
    }


def main():
    fixtures, scope = load_fixtures(base_dir)
    vulnerable = VulnerableReconAgent(scope)
    guarded = ProvenanceAwareReconAgent(scope)

    rows, mismatches, details = [], [], []
    for f in fixtures:
        want = expected_for(f, scope)
        v = vulnerable.process(f)
        g = guarded.process(f)
        got = {
            "scope": g["scope"],
            "injections_detected": g["injections_detected"],
            "vulnerable": v["actions"][0]["action"] if v["actions"] else "none",
            "provenance_aware": g["actions"][0]["action"] if g["actions"] else "none",
        }
        row = {"fixture": f["id"], "source": f["source"], "expected": want, "got": got}
        rows.append(row)
        if got != want:
            mismatches.append(f["id"])
        for a in g["actions"]:
            details.append({"source": f["id"], "field": a["source"], "provenance": a["provenance"],
                            "snippet": a["instruction"][:80]})

    blocked = [r["fixture"] for r in rows if r["got"]["scope"] == "blocked"]
    results = {
        "demo": "demo-06-reconscope",
        "experiment": "injection_detection",
        "seed": 42,
        "commit": git_commit(),
        "environment": f"Python {platform.python_version()}, {platform.system()} {platform.release()}",
        "command": "make demo DEMO=06",
        "result": "pass" if not mismatches else "fail",
        "notes": "Synthetic teaching fixture; injection marking uses the fixture's ground-truth strings",
        "total_fixtures": len(fixtures),
        "injections_in_fixtures": sum(1 for f in fixtures if f.get("injection")),
        "blocked_by_scope": blocked,
        "injections_detected": sum(r["got"]["injections_detected"] for r in rows),
        "vulnerable_executed": sum(1 for r in rows if r["got"]["vulnerable"] == "execute"),
        "provenance_aware_executed": sum(1 for r in rows if r["got"]["provenance_aware"] == "execute"),
        "provenance_aware_logged": sum(1 for r in rows if r["got"]["provenance_aware"] == "log"),
        "mismatches": mismatches,
        "injection_details": details,
        "per_fixture": rows,
    }

    out_path = base_dir / "results" / "evaluation.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))

    print(f"{'fixture':12} {'source':20} {'scope':8} {'inj':>3}  {'vulnerable':10} {'provenance-aware':16} ok")
    for r in rows:
        ok = "yes" if r["got"] == r["expected"] else "NO"
        print(f"{r['fixture']:12} {r['source']:20} {r['got']['scope']:8} {r['got']['injections_detected']:>3}  "
              f"{r['got']['vulnerable']:10} {r['got']['provenance_aware']:16} {ok}")
    print(f"\nresult: {results['result']} ({len(rows) - len(mismatches)}/{len(rows)} fixtures behaved as the fixture implies)")
    print(f"written: {out_path.relative_to(base_dir)}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
