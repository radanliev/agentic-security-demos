#!/usr/bin/env python3
"""Tests for Demo 30: Default Configs (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_defaults import main  # noqa: E402
from checker import is_insecure  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_defaults.py")],
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


def test_six_of_ten_insecure():
    """Six of ten stacks are insecure."""
    out = main()
    assert out["total"] == 10
    assert out["insecure"] == 6
    assert out["insecure_ids"] == ["s01", "s03", "s04", "s05", "s07", "s09"]


def test_three_pinned_vulns():
    """Three of ten stacks carry a pinned vuln (all insecure)."""
    out = main()
    assert out["pinned"] == 3
    assert out["pinned_ids"] == ["s04", "s07", "s09"]


def test_reasons_match_rule():
    """Spot-check the rule on one exposed and one secure stack."""
    pack = json.loads((DEMO_DIR / "fixtures" / "stacks.json").read_text())
    by_id = {s["id"]: s for s in pack["stacks"]}
    assert is_insecure(by_id["s01"]) == ["public-without-auth"]
    assert is_insecure(by_id["s02"]) == []
    assert sorted(is_insecure(by_id["s07"])) == ["pinned-vuln", "public-without-auth"]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "defaults.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 30
