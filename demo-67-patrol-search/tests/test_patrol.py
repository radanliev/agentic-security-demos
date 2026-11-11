import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from patrol import exhaustive, greedy, uncovered

def test_hub_covers_three_paths():
    chosen, score = exhaustive(["s", "t", "u", "v"], [["s", "t"], ["s", "u"], ["s", "v"]], 1)
    assert chosen == ["s"]
    assert score == 0

def test_empty_paths_are_fully_covered():
    chosen, score = exhaustive(["a", "b", "c"], [], 2)
    assert score == 0
    assert len(chosen) == 2

def test_greedy_not_worse_than_all_uncovered():
    nodes = ["a", "b", "c", "d"]
    paths = [["a", "b"], ["c", "d"], ["a", "c"]]
    _, ex = exhaustive(nodes, paths, 2)
    _, gr = greedy(nodes, paths, 2)
    assert ex <= gr

def test_uncovered_counts_disjoint_paths():
    assert uncovered([["a", "b"], ["c"]], ["a"]) == 1

def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_patrol.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    payload = json.loads((ROOT / "results" / "patrol.json").read_text())
    assert len(payload["rows"]) == 8
    assert payload["k"] == 2
