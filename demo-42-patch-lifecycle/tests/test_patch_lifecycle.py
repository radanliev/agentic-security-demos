#!/usr/bin/env python3
"""Tests for Demo 42: Patch Lifecycle (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_cycle import main  # noqa: E402
from lifecycle import blocked, median  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_cycle.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_vulns() -> list:
    """Load the synthetic vulnerability records."""
    pack = json.loads((DEMO_DIR / "fixtures" / "vulns.json").read_text())
    return pack["vulns"]


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_median_adopt_lag_pinned():
    """The hand-picked lags median to exactly 37.5 days."""
    vulns = fixture_vulns()
    lags = [v["adopt_lag_days"] for v in vulns]
    assert lags == [5, 12, 20, 30, 45, 60, 90, 180]
    assert median(lags) == 37.5


def test_blocked_two_of_eight():
    """Two of eight fixes are blocked by version pins."""
    assert blocked(fixture_vulns()) == ["vuln04", "vuln07"]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "lifecycle.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 42


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("lifecycle.py", "run_cycle.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
