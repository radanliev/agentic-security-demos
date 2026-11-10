import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from covering import accuracy, learn, predict_one

def _data():
    return json.loads((ROOT / "fixtures" / "urls.json").read_text())

def test_learns_at_least_one_rule():
    data = _data()
    rules, default = learn(data["rows"], data["positive_label"])
    assert rules
    assert accuracy(data["rows"], rules, default) >= 0.75

def test_at_feature_fires():
    data = _data()
    rules, default = learn(data["rows"], data["positive_label"])
    assert predict_one({"has_at": 1, "has_ip": 0, "long_url": 0, "has_hyphen": 0}, rules, default) == 1

def test_run_writes_results():
    r = subprocess.run([sys.executable, "student/run_covering.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    payload = json.loads((ROOT / "results" / "covering.json").read_text())
    assert payload["n_rows"] == 8
    assert payload["rules"]
