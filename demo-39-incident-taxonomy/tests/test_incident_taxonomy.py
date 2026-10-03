#!/usr/bin/env python3
"""Tests for Demo 39: Incident Taxonomy (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
Counts (4/3/2/1 patterns, 7/10 controls) are hand-built into
fixtures/incidents.json; the tests pin them so any edit is visible.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_tax import main  # noqa: E402
from taxonomy import supported_controls, top_pattern  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx",
                     "ssl", "http.client")

ALLOWED_PATTERNS = {"prompt-injection", "tool-misuse",
                    "data-exfiltration", "privilege-escalation"}


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_tax.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_pack() -> dict:
    """Load the synthetic incident pack."""
    return json.loads((DEMO_DIR / "fixtures" / "incidents.json").read_text())


# --- Fixture integrity ---

def test_fixture_has_ten_incidents_with_unique_ids():
    """Ten sketches, ids inc01..inc10, no duplicates."""
    pack = fixture_pack()
    ids = [inc["id"] for inc in pack["incidents"]]
    assert len(ids) == 10
    assert len(set(ids)) == 10
    assert set(ids) == {f"inc{i:02d}" for i in range(1, 11)}


def test_fixture_incident_schema():
    """Every sketch has id, pattern (in the 4-set) and a non-empty atlas list."""
    pack = fixture_pack()
    for inc in pack["incidents"]:
        assert set(inc) >= {"id", "pattern", "atlas"}
        assert inc["pattern"] in ALLOWED_PATTERNS
        assert isinstance(inc["atlas"], list) and inc["atlas"]
        assert all(isinstance(t, str) and t for t in inc["atlas"])


def test_fixture_controls_schema():
    """Ten controls, ids ctl01..ctl10, named, boolean supported flags."""
    pack = fixture_pack()
    ctrls = pack["controls"]
    assert len(ctrls) == 10
    assert [c["id"] for c in ctrls] == [f"ctl{i:02d}" for i in range(1, 11)]
    for c in ctrls:
        assert c["name"] and isinstance(c["name"], str)
        assert isinstance(c["supported"], bool)


def test_fixture_seed_and_note():
    """Seed is 39 and the note marks the pack as a synthetic toy."""
    pack = fixture_pack()
    assert pack["seed"] == 39
    assert "Toy" in pack["note"]


# --- Determinism ---

def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_results_deterministic_across_runs():
    """Two in-memory evaluations return equal dicts."""
    assert main() == main()


def test_results_file_byte_parity():
    """The results file is byte-identical across runs (reproducibility)."""
    main()
    first = (DEMO_DIR / "results" / "taxonomy.json").read_bytes()
    main()
    second = (DEMO_DIR / "results" / "taxonomy.json").read_bytes()
    assert first == second


# --- Pattern counts 4/3/2/1 ---

def test_top_pattern_is_prompt_injection():
    """Prompt-injection tops the hand-built tally at 4/10."""
    pack = fixture_pack()
    top = top_pattern(pack["incidents"])
    assert top["pattern"] == "prompt-injection"
    assert top["count"] == 4
    assert top["counts"] == {
        "prompt-injection": 4,
        "tool-misuse": 3,
        "data-exfiltration": 2,
        "privilege-escalation": 1,
    }


def test_each_pattern_count():
    """Each of the four patterns has its hand-built count."""
    pack = fixture_pack()
    counts = top_pattern(pack["incidents"])["counts"]
    assert counts["prompt-injection"] == 4
    assert counts["tool-misuse"] == 3
    assert counts["data-exfiltration"] == 2
    assert counts["privilege-escalation"] == 1


def test_pattern_counts_sum_to_ten():
    """Counts sum to the fixture size; no sketch lost or double-counted."""
    pack = fixture_pack()
    top = top_pattern(pack["incidents"])
    assert sum(top["counts"].values()) == top["n"] == 10


def test_tie_break_is_deterministic():
    """A 4/4 tie resolves deterministically (alphabetically-first maximum).

    Implementation-defined tie-break, pinned so it cannot silently change:
    prompt-injection precedes tool-misuse alphabetically.
    """
    incidents = ([{"id": f"p{i}", "pattern": "prompt-injection"} for i in range(4)]
                 + [{"id": f"t{i}", "pattern": "tool-misuse"} for i in range(4)]
                 + [{"id": f"d{i}", "pattern": "data-exfiltration"} for i in range(2)])
    top = top_pattern(incidents)
    assert top["counts"]["prompt-injection"] == top["counts"]["tool-misuse"] == 4
    assert top_pattern(incidents)["pattern"] == top["pattern"] == "prompt-injection"


# --- Controls 7/10 ---

def test_supported_controls_seven_of_ten():
    """The static catalogue marks 7/10 controls supported."""
    pack = fixture_pack()
    ctrls = supported_controls(pack["controls"])
    assert ctrls["supported"] == 7
    assert ctrls["n"] == 10


def test_supported_and_unsupported_control_ids():
    """Exactly ctl01..ctl07 supported; ctl08..ctl10 unsupported."""
    pack = fixture_pack()
    ctrls = supported_controls(pack["controls"])
    assert ctrls["supported_ids"] == [f"ctl{i:02d}" for i in range(1, 8)]
    unsupported = [c["id"] for c in pack["controls"] if not c["supported"]]
    assert unsupported == ["ctl08", "ctl09", "ctl10"]


def test_control_ids_unique():
    """Control ids are unique."""
    pack = fixture_pack()
    ids = [c["id"] for c in pack["controls"]]
    assert len(set(ids)) == len(ids) == 10


# --- Parity, seed, output ---

def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "taxonomy.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 39


def test_seed_parity():
    """Fixture seed, results seed and experiment seed agree (39)."""
    pack = fixture_pack()
    out = main()
    assert pack["seed"] == out["seed"] == 39


def test_stdout_reports_tally():
    """Stdout carries the exact tally lines students compare against."""
    proc = run_demo()
    assert proc.returncode == 0, proc.stderr
    assert "incidents 10  controls 10" in proc.stdout
    assert "top pattern: prompt-injection (4/10)" in proc.stdout
    assert "supported controls: 7/10" in proc.stdout


def test_stdlib_only():
    """Student modules use no network imports."""
    for module in ("taxonomy.py", "run_tax.py"):
        src = (DEMO_DIR / "student" / module).read_text()
        for marker in FORBIDDEN_IMPORTS:
            assert marker not in src, f"{module} uses forbidden import ({marker})"


def test_results_schema():
    """Results file follows the standard result schema (nested keys, types)."""
    out = main()
    assert set(out) == {"demo", "experiment", "seed", "top_pattern",
                        "controls", "notes"}
    assert out["demo"] == "demo-39-incident-taxonomy"
    assert out["experiment"] == "incident-tally"
    assert isinstance(out["seed"], int)
    assert set(out["top_pattern"]) == {"pattern", "count", "n", "counts"}
    assert isinstance(out["top_pattern"]["counts"], dict)
    assert set(out["controls"]) == {"n", "supported", "supported_ids"}
    assert isinstance(out["controls"]["supported_ids"], list)
