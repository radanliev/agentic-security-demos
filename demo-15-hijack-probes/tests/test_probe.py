#!/usr/bin/env python3
"""Tests for Demo 15: Hijack Probes (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_probe import THRESHOLD, main  # noqa: E402
from probe import Probe  # noqa: E402

FORBIDDEN_IN_PROBE = ("hijacked", "oracle")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_probe.py")],
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


def test_threshold_is_pinned():
    """Fixed threshold is 0.55 and the probe uses >= semantics."""
    assert THRESHOLD == 0.55
    probe = Probe(0.55)
    assert probe.decide(0.55) is True
    assert probe.decide(0.50) is False
    assert probe.decide(0.60) is True


def test_catches_three_of_four():
    """Probe catches h1/h2/h3 and misses borderline h4."""
    out = main()
    assert out["catches"] == 3
    assert out["n_hijacked"] == 4
    assert out["missed_ids"] == ["h4"]


def test_no_false_positives():
    """No clean episode is flagged."""
    out = main()
    assert out["false_positives"] == 0
    assert out["n_clean"] == 4


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "probe_eval.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 15
