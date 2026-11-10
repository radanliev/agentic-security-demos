import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from mapping import recommend

def _alignment():
    return json.loads((ROOT / "fixtures" / "alignments.json").read_text())["alignment"]

def test_single_technique_union():
    result = recommend(["T-phish"], _alignment())
    assert result["controls"] == ["AC-4", "AT-2"]
    assert result["uncovered"] == []

def test_unknown_is_uncovered():
    result = recommend(["T-unknown"], _alignment())
    assert result["unknown"] == ["T-unknown"]
    assert result["controls"] == []

def test_empty_profile():
    result = recommend([], _alignment())
    assert result["controls"] == []
    assert result["covered"] == []

def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_mapping.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert len(json.loads((ROOT / "results" / "mapping.json").read_text())["rows"]) == 8
