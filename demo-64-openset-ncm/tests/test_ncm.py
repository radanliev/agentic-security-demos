import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from ncm import class_means, predict_forced_nn, predict_ncm

def _data():
    return json.loads((ROOT / "fixtures" / "patterns.json").read_text())

def test_known_class_accepted():
    data = _data()
    result = predict_ncm([1.0, 0.0, 0.0], class_means(data["train"]), data["threshold"])
    assert result["label"] == "A"
    assert result["rejected"] is False

def test_far_point_rejected_by_ncm_not_by_nn():
    data = _data()
    far = [2.0, 2.0, 2.0]
    ncm = predict_ncm(far, class_means(data["train"]), data["threshold"])
    forced = predict_forced_nn(far, data["train"])
    assert ncm["rejected"] is True
    assert ncm["label"] == "unknown"
    assert forced["rejected"] is False
    assert forced["label"] in {"A", "B", "C"}

def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_ncm.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert len(json.loads((ROOT / "results" / "ncm.json").read_text())["rows"]) == 8
