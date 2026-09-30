#!/usr/bin/env python3
"""Tests for Demo 19: Lineage Risk (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_lineage import main  # noqa: E402
from lineage import classify  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_lineage.py")],
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


def test_six_of_eight_risky():
    """Six models are risky with the pinned identities."""
    out = main()
    assert out["n_models"] == 8
    assert out["n_risky"] == 6
    assert out["risky_ids"] == ["B", "a2", "b1", "b2", "c1", "c2"]


def test_risk_splits_by_origin():
    """One origin, two introduced, three inherited."""
    out = main()
    assert out["by_kind"]["origin"] == 1
    assert out["by_kind"]["introduced"] == 2
    assert out["by_kind"]["inherited"] == 3
    assert out["by_kind"]["safe"] == 2


def test_inheritance_without_own_flags():
    """Clean children of risky parents are flagged as inherited."""
    toy = [
        {"id": "P", "parent": None, "pickle": True, "remote_code": False, "license_ok": True},
        {"id": "Q", "parent": "P", "pickle": False, "remote_code": False, "license_ok": True},
    ]
    result = classify(toy)
    assert result["kinds"]["P"] == "origin"
    assert result["kinds"]["Q"] == "inherited"


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "lineage.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 19
