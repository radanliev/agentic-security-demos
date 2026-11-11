import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from linkage import jaccard, link, tokens

def _data():
    return json.loads((ROOT / "fixtures" / "advisories.json").read_text())

def test_exact_match_no_disagreement():
    rows = {row["id"]: row for row in link(_data()["source_a"], _data()["source_b"])}
    assert rows["CVE-TOY-0001"]["matched"] is True
    assert rows["CVE-TOY-0001"]["severity_disagree"] is False
    assert rows["CVE-TOY-0001"]["product_disagree"] is False

def test_severity_disagreement():
    rows = {row["id"]: row for row in link(_data()["source_a"], _data()["source_b"])}
    assert rows["CVE-TOY-0002"]["severity_disagree"] is True

def test_unmatched_left_record():
    rows = {row["id"]: row for row in link(_data()["source_a"], _data()["source_b"])}
    assert rows["CVE-TOY-0007"]["matched"] is False

def test_token_jaccard():
    assert tokens("vpn client") == {"vpn", "client"}
    assert jaccard({"vpn", "client"}, {"vpn", "client"}) == 1.0
    assert jaccard({"image", "library"}, {"image", "codec", "library"}) < 1.0

def test_run_writes_results():
    r = subprocess.run([sys.executable, "student/run_linkage.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    payload = json.loads((ROOT / "results" / "linkage.json").read_text())
    assert payload["matched"] == 7
    assert payload["severity_disagree"] == 2
