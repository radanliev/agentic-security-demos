#!/usr/bin/env python3
"""Tests for Demo 22: Memory Leakage (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_memory import main  # noqa: E402
from memory import erasure_failures, persists_high, resurfaced  # noqa: E402


def run_demo() -> subprocess.CompletedProcess:
    """Run the screen as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_memory.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def load_entries() -> list:
    pack = json.loads((DEMO_DIR / "fixtures" / "memory.json").read_text())
    return pack["entries"]


def test_run_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_persists_high_pins_two():
    """Exactly 2 high-sensitivity entries persist (m1, m2)."""
    assert persists_high(load_entries()) == ["m1", "m2"]


def test_resurfaced_pins_two():
    """Exactly 2 entries resurface across sessions (m3, m4)."""
    assert resurfaced(load_entries()) == ["m3", "m4"]


def test_erasure_fails_one_of_three():
    """3 entries marked deleted, exactly 1 still present (m7)."""
    entries = load_entries()
    assert sum(1 for e in entries if e["deleted"]) == 3
    assert erasure_failures(entries) == ["m7"]


def test_main_counts_pinned():
    """End-to-end counts: 2 high persists, 2 resurfaces, 1/3 erasures fail."""
    out = main()
    assert out["persists_high"] == ["m1", "m2"]
    assert out["resurfaced"] == ["m3", "m4"]
    assert out["erasure_failures"] == ["m7"]
    assert out["n_deleted"] == 3


def test_results_file_matches_memory():
    """Results on disk equal the in-memory screen."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "memory_leak.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 22
