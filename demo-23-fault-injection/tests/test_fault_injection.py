#!/usr/bin/env python3
"""Tests for Demo 23: Fault Injection (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_faults import main  # noqa: E402
from faults import outcome  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the scorecard as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_faults.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def load_faults() -> list:
    pack = json.loads((DEMO_DIR / "fixtures" / "faults.json").read_text())
    return pack["faults"]


def test_run_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_no_retry_distribution_pinned():
    """Without retries: graceful 2/6, cascade 2/6, silent-wrong 1/6, cost-blowup 1/6."""
    faults = load_faults()
    counts = {"graceful": 0, "cascade": 0, "silent-wrong": 0, "cost-blowup": 0}
    for f in faults:
        counts[outcome(f, 0)] += 1
    assert counts == {"graceful": 2, "cascade": 2, "silent-wrong": 1, "cost-blowup": 1}


def test_retry_budget_distribution_pinned():
    """With retry budget 2: graceful 5/6, only the permanent fault cascades."""
    faults = load_faults()
    counts = {"graceful": 0, "cascade": 0, "silent-wrong": 0, "cost-blowup": 0}
    for f in faults:
        counts[outcome(f, 2)] += 1
    assert counts == {"graceful": 5, "cascade": 1, "silent-wrong": 0, "cost-blowup": 0}
    perm = next(f for f in faults if f["type"] == "permanent")
    assert outcome(perm, 2) == "cascade"


def test_outcome_spot_checks():
    """Spot-check the deterministic table entries."""
    assert outcome({"id": "x", "type": "timeout"}, 0) == "cascade"
    assert outcome({"id": "x", "type": "timeout"}, 2) == "graceful"
    assert outcome({"id": "x", "type": "malformed"}, 0) == "silent-wrong"
    assert outcome({"id": "x", "type": "malformed"}, 2) == "graceful"
    assert outcome({"id": "x", "type": "partial-write"}, 0) == "cost-blowup"
    assert outcome({"id": "x", "type": "duplicate"}, 0) == "graceful"


def test_results_file_matches_memory():
    """Results on disk equal the in-memory scorecard."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "faults.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 23
