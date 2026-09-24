#!/usr/bin/env python3
"""Tests for Demo 13: Typed Commitments & Coverage Cues (teaching toy).

All verdicts are properties of six synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from agreement_gate import main  # noqa: E402

FORBIDDEN_IN_AGENTS = ("vulnerable_file", "oracle")


def run_gate() -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(DEMO_DIR / "student" / "agreement_gate.py")],
                          capture_output=True, text=True, cwd=DEMO_DIR)


def test_toy_eval_is_deterministic():
    first = run_gate()
    second = run_gate()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_wrong_cue_defeats_follower():
    out = main()
    wrong = [r for r in out["rows"] if r["cue"] == "wrong"]
    assert len(wrong) == 2
    assert all(not r["follower_correct"] for r in wrong)


def test_true_cue_helps_follower():
    out = main()
    true = [r for r in out["rows"] if r["cue"] == "true"]
    assert len(true) == 2
    assert all(r["follower_correct"] for r in true)


def test_shared_wrong_input_escapes_agreement_gate():
    out = main()
    bad = [r for r in out["rows"] if r["agree"] and not r["follower_correct"]]
    assert len(bad) == 1 and bad[0]["id"] == "cue-wrong-02"


def test_oracle_separation():
    # Only the two assessors are blind. agreement_gate.py is the scorer: like
    # any evaluator it must read the answer key to mark nominations.
    for module in ("cue_follower.py", "independent_heuristic.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IN_AGENTS:
            assert marker not in src, f"{module} reads the oracle ({marker})"


def test_results_file_matches_memory():
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "toy_eval.json").read_text())
    assert on_disk == out
