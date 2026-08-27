#!/usr/bin/env python3
"""Generate triage results for demo-07 and check them against the fixture's implied outcomes."""

import json
import platform
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from triagetrap import BaselineTriageAgent, ProvenanceAwareTriageAgent, load_artifacts  # noqa: E402


def git_commit() -> str:
    """Short git commit of the checkout, or 'local' outside a repository."""
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def environment() -> str:
    return f"Python {platform.python_version()}, {platform.system()} {platform.release()}"

# What each agent should do with each fixture artifact (the answer key for the prediction table).
EXPECTED = {
    "art-001": ("benign", "benign"),
    "art-002": ("benign", "benign"),
    "art-003": ("quarantine", "quarantine"),   # real malicious sandbox verdict: both agents catch it
    "art-004": ("quarantine", "benign"),       # injection canary: baseline acts on it, guarded logs it
    "art-005": ("benign", "benign"),
    "art-006": ("quarantine", "suspicious"),   # note says malware, verdict says benign: baseline believes the note
}


def main():
    data = json.loads((base_dir / "fixtures" / "artifacts.json").read_text())
    artifacts = load_artifacts(data)
    baseline = BaselineTriageAgent(data["base_rates"], data["quarantine_threshold"])
    guarded = ProvenanceAwareTriageAgent(data["base_rates"], data["quarantine_threshold"])

    results_list = []
    mismatches = []
    for artifact in artifacts:
        b = baseline.triage(artifact)
        g = guarded.triage(artifact)
        exp_b, exp_g = EXPECTED[artifact.id]
        ok = (b.verdict.value, g.verdict.value) == (exp_b, exp_g)
        if not ok:
            mismatches.append(f"{artifact.id}: baseline {b.verdict.value}/{exp_b}, guarded {g.verdict.value}/{exp_g}")
        results_list.append({
            "artifact_id": artifact.id,
            "provenance": artifact.provenance.value,
            "baseline_verdict": b.verdict.value,
            "baseline_score": round(b.score, 4),
            "verdict": g.verdict.value,
            "score": round(g.score, 4),
            "reasons": g.reasons,
            "provenance_chain": g.provenance_chain,
            "expected": {"baseline": exp_b, "provenance_aware": exp_g},
            "ok": ok,
        })

    out = {
        "demo": "demo-07-triagetrap",
        "experiment": "triage",
        "seed": data["seed"],
        "commit": git_commit(),
        "environment": environment(),
        "command": "make demo DEMO=07",
        "result": "pass" if not mismatches else "fail",
        "notes": "Synthetic teaching fixture; verdicts checked against the expected outcome per artifact",
        "results": results_list,
    }

    out_path = base_dir / "results" / "triage_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    if mismatches:
        print("\nMISMATCH:\n  " + "\n  ".join(mismatches), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
