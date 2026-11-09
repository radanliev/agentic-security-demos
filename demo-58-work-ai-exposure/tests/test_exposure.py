from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from exposure import agentic_share, family_means, load, occupation_mean


def data():
    return load(ROOT / "fixtures" / "tasks.json")["occupations"]


def test_tutor_mean():
    tutor = next(o for o in data() if o["id"] == "tutor")
    assert occupation_mean(tutor) == 0.5


def test_three_families():
    assert set(family_means(data())) == {"teaching", "learning-design", "student-support"}


def test_half_the_tasks_are_agentic():
    assert agentic_share(data()) == 0.5
