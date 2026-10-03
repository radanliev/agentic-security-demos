#!/usr/bin/env python3
"""Tests for Demo 37: Detector Cost (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_cost import main, score  # noqa: E402
from detectors import lenient, strict  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")

FP_COST = 10
FN_COST = 25


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_cost.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_pack() -> dict:
    """Load the synthetic fixture pack."""
    return json.loads((DEMO_DIR / "fixtures" / "inputs.json").read_text())


def fixture_inputs() -> list:
    """Load the synthetic input list."""
    return fixture_pack()["inputs"]


class TestFixtureIntegrity:
    """The fixture is the benchmark: ten prompts, fixed costs, fixed seed."""

    def test_fixture_has_ten_inputs(self):
        """Ten hand-built prompts, no more, no fewer."""
        assert len(fixture_inputs()) == 10

    def test_fixture_ids_unique(self):
        """Every prompt carries a unique id."""
        ids = [item["id"] for item in fixture_inputs()]
        assert len(set(ids)) == 10

    def test_fixture_balance_4_injected_6_benign(self):
        """Four injected prompts against six benign ones."""
        items = fixture_inputs()
        assert sum(1 for i in items if i["injected"]) == 4
        assert sum(1 for i in items if not i["injected"]) == 6

    def test_fixture_costs_and_seed(self):
        """FP costs 10, FN costs 25, seed is fixed at 37."""
        pack = fixture_pack()
        assert pack["fp_cost"] == FP_COST
        assert pack["fn_cost"] == FN_COST
        assert pack["seed"] == 37

    def test_fixture_items_have_required_keys(self):
        """Each prompt has an id, a label flag and text."""
        for item in fixture_inputs():
            assert set(item) >= {"id", "injected", "text"}
            assert isinstance(item["text"], str) and item["text"]


class TestDeterminism:
    """Same inputs give the same outputs, every time."""

    def test_eval_is_deterministic(self):
        """Two runs print identical output."""
        first = run_demo()
        second = run_demo()
        assert first.returncode == 0 and second.returncode == 0
        assert first.stdout == second.stdout

    def test_score_is_pure(self):
        """Scoring twice gives the same tallies (no hidden state)."""
        items = fixture_inputs()
        assert score(items, strict) == score(items, strict)
        assert score(items, lenient) == score(items, lenient)

    def test_expected_stdout_verbatim(self):
        """The printed table matches the documented checkpoint exactly."""
        out = run_demo().stdout
        assert "fp_cost 10  fn_cost 25" in out
        assert "strict    4/4  2/6  0/4  20" in out
        assert "lenient   2/4  0/6  2/4  50" in out
        assert "winner: strict (cost 20 < 50)." in out


class TestStrictDetector:
    """Strict flags the substring 'ignor': all 4 injected, 2/6 false alarms."""

    def test_strict_detector_numbers(self):
        """Strict flags all 4 injected at the price of 2/6 false positives."""
        res = score(fixture_inputs(), strict)
        assert (res["tp"], res["fn"]) == (4, 0)
        assert (res["fp"], res["tn"]) == (2, 4)

    def test_strict_catches_paraphrase(self):
        """Paraphrased injections without the exact phrase are still caught."""
        items = {i["id"]: i for i in fixture_inputs()}
        assert strict(items["i3"]["text"]) is True
        assert strict(items["i4"]["text"]) is True

    def test_strict_flags_tricky_benign(self):
        """The two tricky benign prompts (harmless 'ignore') false-alarm."""
        items = {i["id"]: i for i in fixture_inputs()}
        assert strict(items["b1"]["text"]) is True
        assert strict(items["b2"]["text"]) is True


class TestLenientDetector:
    """Lenient needs the exact phrase: 2/4 caught, zero false alarms."""

    def test_lenient_detector_numbers(self):
        """Lenient catches 2/4 with zero false positives."""
        res = score(fixture_inputs(), lenient)
        assert (res["tp"], res["fn"]) == (2, 2)
        assert (res["fp"], res["tn"]) == (0, 6)

    def test_lenient_catches_exact_phrase_only(self):
        """Only the two exact-phrase injections fire; paraphrases do not."""
        items = {i["id"]: i for i in fixture_inputs()}
        assert lenient(items["i1"]["text"]) is True
        assert lenient(items["i2"]["text"]) is True
        assert lenient(items["i3"]["text"]) is False
        assert lenient(items["i4"]["text"]) is False


class TestCostPricing:
    """FP=10, FN=25 prices strict at 20 vs lenient at 50: strict wins."""

    def test_strict_cost_arithmetic(self):
        """Strict: 2 false alarms at 10 plus 0 misses at 25 = 20."""
        res = score(fixture_inputs(), strict)
        assert res["fp"] * FP_COST + res["fn"] * FN_COST == 20

    def test_lenient_cost_arithmetic(self):
        """Lenient: 0 false alarms at 10 plus 2 misses at 25 = 50."""
        res = score(fixture_inputs(), lenient)
        assert res["fp"] * FP_COST + res["fn"] * FN_COST == 50

    def test_cost_pricing_picks_strict(self):
        """FP=10, FN=25 prices strict at 20 vs lenient at 50: strict wins."""
        out = main()
        assert out["strict"]["cost"] == 20
        assert out["lenient"]["cost"] == 50
        assert out["winner"] == "strict"


class TestCostFlip:
    """Costs pick the winner: cheap misses flip the ranking to lenient."""

    def test_cost_flip_when_fn_cheap(self):
        """At FN=5, strict still costs 20 while lenient drops to 10."""
        items = fixture_inputs()
        strict_cost = score(items, strict)["fp"] * 10 + score(items, strict)["fn"] * 5
        lenient_cost = score(items, lenient)["fp"] * 10 + score(items, lenient)["fn"] * 5
        assert (strict_cost, lenient_cost) == (20, 10)
        assert ("lenient" if lenient_cost < strict_cost else "strict") == "lenient"


class TestResultsArtefact:
    """The benchmark artefact on disk matches memory and keeps its schema."""

    def test_results_file_matches_memory(self):
        """Results on disk equal the in-memory evaluation."""
        out = main()
        on_disk = json.loads((DEMO_DIR / "results" / "detector_cost.json").read_text())
        assert on_disk == out
        assert on_disk["notes"] == "Synthetic teaching fixture"
        assert on_disk["seed"] == 37

    def test_results_schema(self):
        """Fixed keys, fixed seed, both detectors, costs and winner present."""
        out = main()
        assert set(out) >= {"demo", "experiment", "seed", "fp_cost", "fn_cost",
                            "strict", "lenient", "winner", "notes"}
        assert out["demo"] == "demo-37-detector-cost"
        assert out["experiment"] == "detector-cost"
        assert out["seed"] == 37
        assert (out["fp_cost"], out["fn_cost"]) == (10, 25)
        for name in ("strict", "lenient"):
            assert set(out[name]) >= {"tp", "fp", "fn", "tn", "cost"}


class TestHygiene:
    """Student modules are offline stdlib-only toys."""

    def test_stdlib_only(self):
        """Student modules use no network imports."""
        for module in ("detectors.py", "run_cost.py"):
            src = (DEMO_DIR / "student" / module).read_text()
            for marker in FORBIDDEN_IMPORTS:
                assert marker not in src, f"{module} uses forbidden import ({marker})"

    def test_seed_fixed(self):
        """Seed 37 is fixed in fixture and results (no randomness)."""
        assert fixture_pack()["seed"] == 37
        assert main()["seed"] == 37
