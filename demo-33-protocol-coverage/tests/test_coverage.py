#!/usr/bin/env python3
"""Tests for Demo 33: Protocol Coverage (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_coverage import main  # noqa: E402
from coverage import covered, gaps  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_coverage.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_two_gaps_discovery_streaming():
    """Exactly discovery and streaming are gaps (2/6)."""
    out = main()
    assert out["total"] == 6
    assert out["gaps"] == 2
    assert out["gap_ids"] == ["discovery", "streaming"]


def test_covered_is_four():
    """The other four elements are covered."""
    pack = json.loads((DEMO_DIR / "fixtures" / "elements.json").read_text())
    assert covered(pack["elements"]) == ["authorisation", "identity", "session", "transport"]
    out = main()
    assert len(out["covered_ids"]) == 4


def test_gap_rule():
    """Gap means attack without mitigation."""
    pack = json.loads((DEMO_DIR / "fixtures" / "elements.json").read_text())
    assert gaps(pack["elements"]) == ["discovery", "streaming"]
    assert gaps([{"id": "x", "stated_mitigation": True, "known_attack": True}]) == []
    assert gaps([{"id": "y", "stated_mitigation": False, "known_attack": False}]) == []


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "coverage.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 33
