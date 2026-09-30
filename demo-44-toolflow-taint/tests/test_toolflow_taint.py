#!/usr/bin/env python3
"""Tests for Demo 44: Toolflow Taint (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_taint import main  # noqa: E402
from taint import unlabelled_to_sensitive  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_taint.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_flows() -> list:
    """Load the synthetic flow edges."""
    pack = json.loads((DEMO_DIR / "fixtures" / "edges.json").read_text())
    return pack["flows"]


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_unlabelled_sensitive_count():
    """Five of eight flows reach sensitive sinks without labels."""
    out = main()
    assert out["n_unlabelled_sensitive"] == 5
    assert out["n"] == 8


def test_tainted_flow_ids_pinned():
    """Exactly flow1-flow5 are unlabelled into sensitive sinks."""
    assert unlabelled_to_sensitive(fixture_flows()) == [
        "flow1", "flow2", "flow3", "flow4", "flow5",
    ]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "taint.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 44


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("taint.py", "run_taint.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
