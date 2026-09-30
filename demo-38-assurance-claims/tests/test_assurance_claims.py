#!/usr/bin/env python3
"""Tests for Demo 38: Assurance Claims (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_claims import main  # noqa: E402
from claims import coverage  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_claims.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_pack() -> dict:
    """Load the synthetic card pack."""
    return json.loads((DEMO_DIR / "fixtures" / "cards8.json").read_text())


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_full_coverage_and_weakest():
    """3/8 cards cover every obligation; weakest is third_party at 3/8."""
    pack = fixture_pack()
    cov = coverage(pack["cards"], pack["obligations"])
    assert cov["full_coverage"] == 3
    assert cov["weakest"] == "third_party"
    assert cov["weakest_count"] == 3


def test_per_obligation_counts():
    """Hand-picked per-obligation tallies hold exactly."""
    pack = fixture_pack()
    cov = coverage(pack["cards"], pack["obligations"])
    assert cov["per_obligation"] == {
        "threats": 7,
        "evals": 5,
        "agentic": 4,
        "third_party": 3,
        "mitigations": 7,
    }


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "claims.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 38


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("claims.py", "run_claims.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
