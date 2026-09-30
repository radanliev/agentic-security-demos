#!/usr/bin/env python3
"""Tests for Demo 20: Agent Web Census (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_web import main  # noqa: E402
from census import adopted, exposed  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_web.py")],
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


def test_adoption_is_four_of_ten():
    """Directive adoption is 4/10."""
    out = main()
    assert out["n_sites"] == 10
    assert out["n_adopting"] == 4


def test_injections_are_two_low_popularity():
    """Injections are 2/10, both on low-popularity sites."""
    out = main()
    assert out["n_exposed"] == 2
    assert out["exposed_ids"] == ["s04", "s05"]
    assert out["exposed_popularity"] == ["low", "low"]


def test_helpers_match_definitions():
    """Adoption is either flag; exposure is non-empty injection text."""
    assert adopted({"llms_txt": True, "ai_directive": False}) is True
    assert adopted({"llms_txt": False, "ai_directive": True}) is True
    assert adopted({"llms_txt": False, "ai_directive": False}) is False
    assert exposed({"injection_text": "hello"}) is True
    assert exposed({"injection_text": None}) is False


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "web_census.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 20
