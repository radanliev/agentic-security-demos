import json, math, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from lipschitz import bounds, frobenius, spectral_norm_2x2

def test_identity_spectral_norm():
    assert spectral_norm_2x2([[1.0, 0.0], [0.0, 1.0]]) == math.sqrt(1.0)

def test_scaled_identity():
    assert spectral_norm_2x2([[2.0, 0.0], [0.0, 2.0]]) == math.sqrt(4.0)

def test_frobenius_dominates_spectral_product():
    result = bounds([[1.0, 2.0], [3.0, 4.0]], [[0.0, 1.0], [-1.0, 0.0]])
    assert result["frobenius_product"] + 1e-12 >= result["spectral_product"]

def test_zero_factor():
    result = bounds([[0.0, 0.0], [0.0, 0.0]], [[4.0, 0.0], [0.0, 3.0]])
    assert result["spectral_product"] == 0.0
    assert frobenius([[0.0, 0.0], [0.0, 0.0]]) == 0.0

def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_lipschitz.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    payload = json.loads((ROOT / "results" / "lipschitz.json").read_text())
    assert len(payload["rows"]) == 8
    assert all(row["frobenius_dominates"] for row in payload["rows"])
