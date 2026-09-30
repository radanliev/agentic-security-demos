#!/usr/bin/env python3
"""Tests for Demo 41: Ten Invariants (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_inv import main  # noqa: E402
from invariants import evaluate  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_inv.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_checks() -> list:
    """Load the synthetic invariant checks."""
    pack = json.loads((DEMO_DIR / "fixtures" / "checks.json").read_text())
    return pack["invariants"]


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_seven_hold_three_violated():
    """The hand-built checklist holds 7/10 and violates 3/10."""
    res = evaluate(fixture_checks())
    assert res["n_holding"] == 7
    assert res["n_violated"] == 3


def test_violated_names_pinned():
    """Exactly provenance-travels, memory-gated and reconstructable fail."""
    res = evaluate(fixture_checks())
    assert sorted(res["violated"]) == [
        "memory-gated",
        "provenance-travels",
        "reconstructable",
    ]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "invariants.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 41


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("invariants.py", "run_inv.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
