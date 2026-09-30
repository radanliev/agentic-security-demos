#!/usr/bin/env python3
"""Tests for Demo 26: Sandbox Probes (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_sandbox import main  # noqa: E402
from sandbox import escape_rate, escaped_probes  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the ladder as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_sandbox.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def load_matrix() -> dict:
    return json.loads((DEMO_DIR / "fixtures" / "matrix.json").read_text())


def test_run_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_escape_rates_pinned():
    """none 8/8, subprocess 3/8, strict 0/8."""
    matrix = load_matrix()
    assert escape_rate(matrix, "none") == (8, 8, 1.0)
    assert escape_rate(matrix, "subprocess")[0:2] == (3, 8)
    assert escape_rate(matrix, "strict") == (0, 8, 0.0)


def test_subprocess_escape_set_pinned():
    """Subprocess leaks exactly net-egress, dns, env-read."""
    matrix = load_matrix()
    assert sorted(escaped_probes(matrix, "subprocess")) == ["dns", "env-read", "net-egress"]
    assert escaped_probes(matrix, "strict") == []
    assert len(escaped_probes(matrix, "none")) == 8


def test_main_rows_pinned():
    """End-to-end rows pin the isolation ladder."""
    out = main()
    assert out["rows"]["none"]["escaped"] == 8
    assert out["rows"]["subprocess"]["escaped"] == 3
    assert out["rows"]["strict"]["escaped"] == 0


def test_results_file_matches_memory():
    """Results on disk equal the in-memory ladder."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "sandbox.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 26
