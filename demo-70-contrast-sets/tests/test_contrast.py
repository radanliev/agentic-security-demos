import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from contrast import emerging, growth_rate, item_support

def test_growth_rate_infinite_when_new():
    assert growth_rate(0.0, 0.5) == float("inf")
    assert growth_rate(0.0, 0.0) == 0.0
    assert growth_rate(0.25, 0.5) == 2.0

def test_support_on_four_bags():
    supp = item_support([["login"], ["login"], ["mail"], ["mail"]])
    assert supp["login"] == 0.5
    assert supp["mail"] == 0.5

def test_emerging_flags_exfil():
    rows, flagged = emerging(
        [["login"], ["login"], ["mail"], ["mail"]],
        [["exfil"], ["exfil"], ["exfil"], ["login"]],
        0.4, 2.0,
    )
    assert "exfil" in flagged
    assert "login" not in flagged

def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_contrast.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert len(json.loads((ROOT / "results" / "contrast.json").read_text())["rows"]) == 8
