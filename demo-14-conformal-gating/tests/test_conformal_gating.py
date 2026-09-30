#!/usr/bin/env python3
"""Tests for Demo 14: Conformal Action Gating (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_gate import calibrate, evaluate, main  # noqa: E402
from conformal_gate import ConformalGate  # noqa: E402

FORBIDDEN_IN_GATES = ("injected", "oracle")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_gate.py")],
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


def test_calibration_picks_expected_threshold():
    """Alpha 0.30 on the hand-built calib set calibrates to 0.20."""
    pack = json.loads((DEMO_DIR / "fixtures" / "episodes.json").read_text())
    assert calibrate(pack["calibration"], 0.30) == 0.20


def test_same_corpus_holds_nominal_risk():
    """Conformal gate meets its risk budget on same-corpus episodes."""
    out = main()
    assert out["conformal_same"]["risk"] <= out["alpha"]
    assert out["conformal_same"]["risk"] == 0.0
    assert out["conformal_same"]["n_executed"] == 1


def test_shifted_corpus_breaks_guarantee():
    """Same gate fails under shift — the benchmark-shift lesson."""
    out = main()
    assert out["conformal_shifted"]["risk"] == 1.0
    assert out["conformal_shifted"]["risk"] > out["alpha"]


def test_oracle_separation():
    """Gate modules decide from scores only; only the evaluator reads labels."""
    for module in ("conformal_gate.py", "fixed_gate.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IN_GATES:
            assert marker not in src, f"{module} reads the oracle ({marker})"


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "gating_eval.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 14
