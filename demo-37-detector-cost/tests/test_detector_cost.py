#!/usr/bin/env python3
"""Tests for Demo 37: Detector Cost (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_cost import main, score  # noqa: E402
from detectors import lenient, strict  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_cost.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_inputs() -> list:
    """Load the synthetic input list."""
    pack = json.loads((DEMO_DIR / "fixtures" / "inputs.json").read_text())
    return pack["inputs"]


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_strict_detector_numbers():
    """Strict flags all 4 injected at the price of 2/6 false positives."""
    res = score(fixture_inputs(), strict)
    assert (res["tp"], res["fn"]) == (4, 0)
    assert (res["fp"], res["tn"]) == (2, 4)


def test_lenient_detector_numbers():
    """Lenient catches 2/4 with zero false positives."""
    res = score(fixture_inputs(), lenient)
    assert (res["tp"], res["fn"]) == (2, 2)
    assert (res["fp"], res["tn"]) == (0, 6)


def test_cost_pricing_picks_strict():
    """FP=10, FN=25 prices strict at 20 vs lenient at 50: strict wins."""
    out = main()
    assert out["strict"]["cost"] == 20
    assert out["lenient"]["cost"] == 50
    assert out["winner"] == "strict"


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "detector_cost.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 37


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("detectors.py", "run_cost.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
