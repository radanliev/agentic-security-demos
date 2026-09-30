#!/usr/bin/env python3
"""Tests for Demo 24: Delegation Checks (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_authz import main  # noqa: E402
from authz import check  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the checker as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_authz.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def load_chains() -> list:
    pack = json.loads((DEMO_DIR / "fixtures" / "chains.json").read_text())
    return pack["chains"]


def test_run_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_four_chains_clean():
    """Chains c1-c4 pass both properties."""
    chains = {c["id"]: c for c in load_chains()}
    for cid in ("c1", "c2", "c3", "c4"):
        assert check(chains[cid]) == [], f"{cid} should be clean"


def test_two_violations_pinned():
    """c5 violates audience binding; c6 violates no-amplification (2->5)."""
    chains = {c["id"]: c for c in load_chains()}
    v5 = check(chains["c5"])
    assert len(v5) == 1 and "audience-mismatch" in v5[0]
    v6 = check(chains["c6"])
    assert len(v6) == 1 and "scope-amplification" in v6[0]
    assert "2->5" in v6[0]


def test_main_counts_pinned():
    """End-to-end: 4 clean, 2 violations."""
    out = main()
    assert out["n_clean"] == 4
    assert out["n_violations"] == 2
    assert out["n_chains"] == 6


def test_results_file_matches_memory():
    """Results on disk equal the in-memory check."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "authz.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 24
