#!/usr/bin/env python3
"""Tests for Demo 43: Terms Coding (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_terms import main  # noqa: E402
from terms import tally  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_terms.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_platforms() -> list:
    """Load the synthetic platform records."""
    pack = json.loads((DEMO_DIR / "fixtures" / "platforms.json").read_text())
    return pack["platforms"]


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_disclaim_five_of_eight():
    """Five of eight platforms disclaim autonomy."""
    res = tally(fixture_platforms())
    assert res["counts"]["disclaims_autonomy"] == 5


def test_monitoring_and_consent_pinned():
    """Monitoring holds 4/8 and delegation consent 3/8."""
    res = tally(fixture_platforms())
    assert res["counts"]["requires_monitoring"] == 4
    assert res["counts"]["consent_for_delegation"] == 3


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "terms.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 43


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("terms.py", "run_terms.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
