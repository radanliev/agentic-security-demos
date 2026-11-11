import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from horn import is_inconsistent, min_deletion

def test_simple_inconsistency_needs_one_deletion():
    facts = ["a"]
    clauses = [{"body": ["a"], "head": "b"}, {"body": ["b"], "head": None}]
    assert is_inconsistent(facts, clauses)
    deleted, _ = min_deletion(facts, clauses)
    assert len(deleted) == 1

def test_consistent_theory_needs_no_deletion():
    facts = ["a"]
    clauses = [{"body": ["a"], "head": "b"}, {"body": ["c"], "head": None}]
    assert not is_inconsistent(facts, clauses)
    deleted, bad = min_deletion(facts, clauses)
    assert deleted == []
    assert bad is False

def test_empty_body_constraint_is_inconsistent():
    assert is_inconsistent([], [{"body": [], "head": None}])

def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_horn.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert len(json.loads((ROOT / "results" / "horn.json").read_text())["rows"]) == 8
