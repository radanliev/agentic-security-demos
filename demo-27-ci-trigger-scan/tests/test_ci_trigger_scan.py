#!/usr/bin/env python3
"""Tests for Demo 27: CI Trigger Scan (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_scan import main  # noqa: E402
from scanner import is_vulnerable  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the scanner as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_scan.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def load_repos() -> list:
    pack = json.loads((DEMO_DIR / "fixtures" / "repos.json").read_text())
    return pack["repos"]


def test_run_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_three_of_eight_vulnerable():
    """Exactly r1, r2, r3 are vulnerable (3/8)."""
    repos = load_repos()
    flagged = [r["id"] for r in repos if is_vulnerable(r)]
    assert flagged == ["r1", "r2", "r3"]


def test_guards_each_block_one_vector():
    """Review, read-only permission, and private triggers each save one repo."""
    repos = {r["id"]: r for r in load_repos()}
    assert not is_vulnerable(repos["r4"])
    assert not is_vulnerable(repos["r5"])
    assert not is_vulnerable(repos["r6"])
    assert is_vulnerable(repos["r1"])


def test_main_counts_pinned():
    """End-to-end: 3 vulnerable of 8 repos."""
    out = main()
    assert out["n_vulnerable"] == 3
    assert out["n_repos"] == 8
    assert out["flagged"] == ["r1", "r2", "r3"]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory scan."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "ci_scan.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 27
