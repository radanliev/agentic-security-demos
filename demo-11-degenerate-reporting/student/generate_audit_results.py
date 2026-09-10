#!/usr/bin/env python3
"""Generate audit results for demo-11 and check them against the fixture's answer key."""

import json
import platform
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from audit_reporting import NaiveReviewer, RigorousAuditor, load_papers, rescore_case_zero  # noqa: E402


def git_commit() -> str:
    """Short git commit of the checkout, or 'local' outside a repository."""
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def environment() -> str:
    return f"Python {platform.python_version()}, {platform.system()} {platform.release()}"


# The answer key for the prediction table (INSTRUCTIONS.md, Step 1).
# Derived in README.md; each verdict is produced by RigorousAuditor.
EXPECTED = {
    "P-01": "PASS",
    "P-02": "FAIL",
    "P-03": "FAIL",
    "P-04": "FAIL",
    "P-05": "FAIL",
    "P-06": "PASS",
    "P-07": "INCONCLUSIVE",
    "P-08": "INCONCLUSIVE",
}
EXPECTED_NAIVE_ACCEPTS = 7  # naive reviewer accepts every paper except P-08


def main():
    papers = load_papers()
    naive = NaiveReviewer()
    auditor = RigorousAuditor()

    results_list = []
    mismatches = []
    naive_accepts = 0
    for paper in papers:
        naive_says = "ACCEPT" if naive.review(paper) else "REJECT"
        naive_accepts += naive_says == "ACCEPT"
        verdict = auditor.audit(paper)
        ok = verdict.verdict == EXPECTED[paper["id"]]
        if not ok:
            mismatches.append(f"{paper['id']}: auditor {verdict.verdict}/{EXPECTED[paper['id']]}")
        results_list.append({
            "paper_id": paper["id"],
            "naive_reviewer": naive_says,
            "audit_verdict": verdict.verdict,
            "reasons": verdict.reasons(),
            "expected": EXPECTED[paper["id"]],
            "ok": ok,
        })
    if naive_accepts != EXPECTED_NAIVE_ACCEPTS:
        mismatches.append(f"naive accepts {naive_accepts}/{EXPECTED_NAIVE_ACCEPTS}")
    results_list.append({
        "paper_id": "NAIVE-SUMMARY",
        "naive_accepts": naive_accepts,
        "expected_naive_accepts": EXPECTED_NAIVE_ACCEPTS,
        "ok": naive_accepts == EXPECTED_NAIVE_ACCEPTS,
    })

    reported, rescored, rows = rescore_case_zero()
    inversion = [p for p, _ in reported] != [p for p, _ in rescored]
    if not inversion:
        mismatches.append("case study zero: expected ranking inversion, got none")
    case_zero = {
        "reported_ranking": [{"policy": p, "score": round(s, 4)} for p, s in reported],
        "rescored_ranking": [{"policy": p, "score": round(s, 4)} for p, s in rescored],
        "ranking_inverts": inversion,
        "rows": rows,
    }

    out = {
        "demo": "demo-11-degenerate-reporting",
        "experiment": "reporting-audit",
        "seed": 42,
        "commit": git_commit(),
        "environment": environment(),
        "command": "make demo DEMO=11",
        "result": "pass" if not mismatches else "fail",
        "notes": "Synthetic teaching fixture; audit verdicts checked against the expected outcome per paper",
        "results": results_list,
        "case_study_zero": case_zero,
    }

    out_path = base_dir / "results" / "audit_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    if mismatches:
        print("\nMISMATCH:\n  " + "\n  ".join(mismatches), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
