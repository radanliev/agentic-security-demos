#!/usr/bin/env python3
"""Tests for Demo 16: Infection Spread (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_spread import main  # noqa: E402
from epidemic import degrees_of, r0, simulate  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_spread.py")],
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


def test_uncontained_spread_reaches_all():
    """Every topology infects 6/6 without containment."""
    out = main()
    for topo in ("chain", "star", "mesh", "tree"):
        assert out["infected"][topo] == 6


def test_chain_containment_holds_at_two():
    """Blocking 4 chain edges holds the chain at 2/6."""
    out = main()
    assert out["contained"]["chain"] == 2
    pack = json.loads((DEMO_DIR / "fixtures" / "graphs.json").read_text())
    assert len(pack["containment"]["chain_blocked_edges"]) == 4


def test_chain_r0_above_one():
    """R0(chain) = 0.9 * mean-degree 1.67 ~= 1.5 > 1."""
    out = main()
    assert abs(out["r0"]["chain"] - 1.5) < 0.01
    assert out["r0"]["chain"] > 1.0
    pack = json.loads((DEMO_DIR / "fixtures" / "graphs.json").read_text())
    chain = pack["topologies"]["chain"]
    degrees = degrees_of(chain["nodes"], chain["edges"])
    assert abs(r0(0.9, degrees) - 1.5) < 0.01


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "spread.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 16
