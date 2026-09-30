#!/usr/bin/env python3
"""Tests for Demo 39: Incident Taxonomy (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_tax import main  # noqa: E402
from taxonomy import supported_controls, top_pattern  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_tax.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_pack() -> dict:
    """Load the synthetic incident pack."""
    return json.loads((DEMO_DIR / "fixtures" / "incidents.json").read_text())


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_top_pattern_is_prompt_injection():
    """Prompt-injection tops the hand-built tally at 4/10."""
    pack = fixture_pack()
    top = top_pattern(pack["incidents"])
    assert top["pattern"] == "prompt-injection"
    assert top["count"] == 4
    assert top["counts"] == {
        "prompt-injection": 4,
        "tool-misuse": 3,
        "data-exfiltration": 2,
        "privilege-escalation": 1,
    }


def test_supported_controls_seven_of_ten():
    """The static catalogue marks 7/10 controls supported."""
    pack = fixture_pack()
    ctrls = supported_controls(pack["controls"])
    assert ctrls["supported"] == 7
    assert ctrls["n"] == 10


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "taxonomy.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 39


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("taxonomy.py", "run_tax.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
