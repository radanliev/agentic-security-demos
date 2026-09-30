#!/usr/bin/env python3
"""Tests for Demo 36: Card Debt (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_cards import main  # noqa: E402
from cards import missing_safety, popularity_gap  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_cards.py")],
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


def test_seven_of_twelve_missing_safety():
    """Seven of twelve cards miss a safety section."""
    out = main()
    assert out["total"] == 12
    assert out["missing_safety"] == 7
    assert out["missing_ids"] == ["c03", "c05", "c06", "c08", "c09", "c11", "c12"]


def test_popularity_gap():
    """Top-4 miss 1/4 while bottom-8 miss 6/8."""
    pack = json.loads((DEMO_DIR / "fixtures" / "cards.json").read_text())
    gap = popularity_gap(pack["cards"])
    assert gap["top_ids"] == ["c01", "c02", "c03", "c04"]
    assert gap["top_missing"] == ["c03"]
    assert gap["bottom_missing"] == ["c05", "c06", "c08", "c09", "c11", "c12"]
    out = main()
    assert out["top_missing"] == 1
    assert out["bottom_missing"] == 6


def test_missing_helper():
    """Helper flags exactly the cards without safety."""
    pack = json.loads((DEMO_DIR / "fixtures" / "cards.json").read_text())
    assert missing_safety(pack["cards"]) == ["c03", "c05", "c06", "c08", "c09", "c11", "c12"]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "cards.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 36
