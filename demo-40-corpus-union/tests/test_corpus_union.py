#!/usr/bin/env python3
"""Tests for Demo 40: Corpus Union (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_corpus import main  # noqa: E402
from corpus import dedupe, normalize, releasable  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_corpus.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_records() -> list:
    """Load the synthetic record list."""
    pack = json.loads((DEMO_DIR / "fixtures" / "records.json").read_text())
    return pack["records"]


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_dedupe_yields_nine_unique():
    """Twelve records collapse to nine unique normalised texts."""
    records = fixture_records()
    assert len(records) == 12
    assert len(dedupe(records)) == 9


def test_normalize_folds_case_and_space():
    """Normalisation lowercases and strips before hashing."""
    assert normalize("  Alpha Widget GUIDE ") == "alpha widget guide"


def test_license_gate_releases_seven():
    """Permissive + by-sa admits 7/9; the noncommercial and unlicensed records block."""
    out = main()
    assert out["n_releasable"] == 7
    assert out["blocked_ids"] == ["r07", "r08"]
    assert len(releasable(fixture_records())) == 7


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "corpus.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 40


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("corpus.py", "run_corpus.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"
