from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from meta import fixed_effect, load


def test_mean_between_min_and_max():
    studies = load(ROOT / "fixtures" / "studies.json")["studies"]
    summary = fixed_effect(studies)
    ys = [s["yi"] for s in studies]
    assert min(ys) < summary["mean"] < max(ys)


def test_precise_study_pulls_the_mean():
    # S4 has vi=0.01, much more precise than S2 (0.09), so the mean should sit nearer 0.40 than 0.50
    studies = load(ROOT / "fixtures" / "studies.json")["studies"]
    summary = fixed_effect(studies)
    assert abs(summary["mean"] - 0.40) < abs(summary["mean"] - 0.50)


def test_q_non_negative():
    studies = load(ROOT / "fixtures" / "studies.json")["studies"]
    assert fixed_effect(studies)["Q"] >= 0
