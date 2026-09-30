#!/usr/bin/env python3
"""Tests for Demo 32: Reproducibility Audit (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_audit import main  # noqa: E402
from audit import invariant_holds, rates  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_audit.py")],
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


def test_six_code_data_four_reproduce():
    """Six of ten share code+data; four of ten reproduce."""
    out = main()
    assert out["total"] == 10
    assert out["code_data"] == 6
    assert out["reproduces"] == 4


def test_channel_breakdown():
    """Per-channel counts match the hand-built fixture."""
    pack = json.loads((DEMO_DIR / "fixtures" / "papers.json").read_text())
    summary = rates(pack["papers"])
    assert summary["by_channel"]["content"] == {"n": 3, "reproduces": 2}
    assert summary["by_channel"]["tool"] == {"n": 3, "reproduces": 1}
    assert summary["by_channel"]["memory"] == {"n": 2, "reproduces": 1}
    assert summary["by_channel"]["multiagent"] == {"n": 2, "reproduces": 0}


def test_reproduce_implies_code_data():
    """Every reproducing paper shares code+data."""
    pack = json.loads((DEMO_DIR / "fixtures" / "papers.json").read_text())
    assert invariant_holds(pack["papers"]) is True
    for paper in pack["papers"]:
        if paper["reproduces"]:
            assert paper["code"] and paper["data"]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "sok_audit.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 32
