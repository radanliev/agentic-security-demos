#!/usr/bin/env python3
"""Tests for Demo 29: Provenance Graphs (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import copy
import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_prov import main  # noqa: E402
from provenance import attributable, build_chain, verify  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_prov.py")],
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


def test_attributable_five_of_six():
    """Five of six actions are attributable."""
    out = main()
    assert out["total"] == 6
    assert out["attributable"] == 5


def test_unattributable_is_a5():
    """The orphan a5 (null cause, not root) is the only unattributable id."""
    pack = json.loads((DEMO_DIR / "fixtures" / "actions.json").read_text())
    part = attributable(pack["actions"], pack["root"])
    assert part["unattributable"] == ["a5"]
    assert len(part["attributable"]) == 5


def test_chain_verifies():
    """A fresh chain over untampered records verifies."""
    pack = json.loads((DEMO_DIR / "fixtures" / "actions.json").read_text())
    chain = build_chain(pack["actions"])
    assert verify(pack["actions"], chain) is True


def test_tamper_is_detected():
    """Editing a copy breaks verification."""
    pack = json.loads((DEMO_DIR / "fixtures" / "actions.json").read_text())
    chain = build_chain(pack["actions"])
    tampered = copy.deepcopy(pack["actions"])
    tampered[1]["authority"] = "operator"
    assert verify(tampered, chain) is False
    out = main()
    assert out["tamper_detected"] is True


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "provenance.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 29
