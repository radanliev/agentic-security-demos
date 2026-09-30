#!/usr/bin/env python3
"""Tests for Demo 34: Visual Injection (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_visual import main  # noqa: E402
from visual import baseline_success, injections, region_defense  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_visual.py")],
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


def test_three_injections_all_acted():
    """Three injections exist and the baseline acts on all of them."""
    pack = json.loads((DEMO_DIR / "fixtures" / "images.json").read_text())
    assert injections(pack["images"]) == ["v01", "v02", "v03"]
    base = baseline_success(pack["images"])
    assert base == {"injections": 3, "acted": 3}
    out = main()
    assert out["baseline_acted"] == 3


def test_region_defense_blocks_all_with_cost_one():
    """Region defense blocks 3/3 injections and 1 benign (cost)."""
    pack = json.loads((DEMO_DIR / "fixtures" / "images.json").read_text())
    defense = region_defense(pack["images"])
    assert defense["blocked_injections"] == ["v01", "v02", "v03"]
    assert defense["blocked_benign"] == ["v07"]
    out = main()
    assert out["blocked_injections"] == 3
    assert out["blocked_benign"] == 1


def test_injections_all_untrusted():
    """All injections sit in the untrusted region."""
    pack = json.loads((DEMO_DIR / "fixtures" / "images.json").read_text())
    for image in pack["images"]:
        if image["typographic"]:
            assert image["region"] == "untrusted"
            assert image["acted"] is True


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "visual.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 34
