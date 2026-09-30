#!/usr/bin/env python3
"""Tests for Demo 35: Scaling Metaregression (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_meta import main  # noqa: E402
from meta import group_means  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_meta.py")],
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


def test_benchmark_means():
    """Per-benchmark means match the hand-built fixture."""
    pack = json.loads((DEMO_DIR / "fixtures" / "results.json").read_text())
    summary = group_means(pack["rows"])
    assert abs(summary["mean_A"] - 0.65) < 1e-9
    assert abs(summary["mean_B"] - 0.345) < 1e-9
    assert summary["bench_gap"] >= 0.20


def test_scale_means_close():
    """Per-scale means differ by at most 0.05."""
    pack = json.loads((DEMO_DIR / "fixtures" / "results.json").read_text())
    summary = group_means(pack["rows"])
    assert abs(summary["mean_small"] - 0.464) < 1e-9
    assert abs(summary["mean_large"] - 0.47) < 1e-9
    assert summary["scale_gap"] <= 0.05


def test_benchmark_explains_more_than_scale():
    """Benchmark gap dominates the scale gap."""
    out = main()
    assert out["bench_gap"] >= 0.20
    assert out["scale_gap"] <= 0.05
    assert out["bench_gap"] > out["scale_gap"]


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "meta.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 35
