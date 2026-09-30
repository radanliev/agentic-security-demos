#!/usr/bin/env python3
"""Tests for Demo 25: Attestation Verifier (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_verify import main  # noqa: E402
from verifier import decide  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the verifier as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_verify.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def load_packages() -> list:
    pack = json.loads((DEMO_DIR / "fixtures" / "packages.json").read_text())
    return pack["packages"]


def test_run_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_fail_closed_blocks_six_of_ten():
    """Fail-closed blocks all 6 unattested packages (6/10 blocked)."""
    packages = load_packages()
    decisions = [decide(p, "fail-closed") for p in packages]
    assert decisions.count("block") == 6
    assert decisions.count("allow") == 4


def test_fail_open_warns_instead():
    """Fail-open warns on the same 6 instead of blocking."""
    packages = load_packages()
    decisions = [decide(p, "fail-open") for p in packages]
    assert decisions.count("block") == 0
    assert decisions.count("allow-with-warning") == 6
    assert decisions.count("allow") == 4


def test_decide_spot_checks():
    """Attested always allows; default policy is fail-closed."""
    assert decide({"id": "a", "attested": True}) == "allow"
    assert decide({"id": "b", "attested": False}) == "block"
    assert decide({"id": "b", "attested": False}, "fail-open") == "allow-with-warning"


def test_results_file_matches_memory():
    """Results on disk equal the in-memory verification."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "attest.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 25
