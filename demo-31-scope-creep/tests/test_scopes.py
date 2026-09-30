#!/usr/bin/env python3
"""Tests for Demo 31: Scope Creep (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_scopes import main  # noqa: E402
from scopes import least_privilege, overprivileged  # noqa: E402

EXPECTED_LEAST = [
    "calendar.read",
    "chat",
    "drive.read",
    "drive.write",
    "files.read",
    "read",
    "repo",
    "write",
]


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_scopes.py")],
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


def test_five_of_eight_overprivileged():
    """Five of eight integrations are over-privileged."""
    out = main()
    assert out["total"] == 8
    assert out["overprivileged"] == 5
    assert out["overprivileged_ids"] == ["i1", "i4", "i5", "i6", "i8"]


def test_least_privilege_union():
    """Least-privilege set is the sorted union of used scopes."""
    pack = json.loads((DEMO_DIR / "fixtures" / "integrations.json").read_text())
    assert least_privilege(pack["integrations"]) == EXPECTED_LEAST
    out = main()
    assert out["least_privilege"] == EXPECTED_LEAST


def test_strict_superset_rule():
    """Equal requested/used is tight; strict superset is over."""
    assert overprivileged({"requested": ["read"], "used": ["read"]}) is False
    assert overprivileged({"requested": ["read", "write"], "used": ["read"]}) is True
    assert overprivileged({"requested": ["read"], "used": ["read", "write"]}) is False


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "scopes.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 31
