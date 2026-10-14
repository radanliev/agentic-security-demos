import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from seal import digest, score, seal  # noqa: E402


def test_hit_and_miss():
    hit = seal("c", "auth.token_check")
    assert score(hit, "auth.token_check", "auth.token_check") == "hit"
    miss = seal("c", "logging.redact")
    assert score(miss, "logging.redact", "auth.token_check") == "miss"


def test_edit_after_seal_is_mismatch():
    link = seal("c", "auth.token_check")
    assert score(link, "logging.redact", "logging.redact") == "commitment_hash_mismatch"


def test_chain_links_differ():
    a = seal("a", "auth.token_check")
    b = seal("b", "auth.token_check", prev=a["seal"])
    assert a["seal"] != b["seal"]
    assert b["prev"] == a["seal"]
    assert len(digest("x")) == 64


def test_demo_writes_three_verdicts():
    subprocess.check_call([sys.executable, "student/run_seal.py"], cwd=ROOT)
    rows = json.loads((ROOT / "results" / "seals.json").read_text())
    assert [r["verdict"] for r in rows] == ["hit", "miss", "commitment_hash_mismatch"]
