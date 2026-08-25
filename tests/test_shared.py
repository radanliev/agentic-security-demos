#!/usr/bin/env python3
"""
Tests for shared library modules:
- shared/result_schema.py
- shared/reproducibility.py
- shared/fixtures.py
"""

import json
import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from shared.result_schema import ResultRecord, write_result, read_results, capture_environment, format_command, get_git_commit
from shared.reproducibility import generate_seed, deterministic_shuffle, set_global_seed, verify_offline
from shared.fixtures import write_fixture, read_fixture, generate_canary, generate_fake_hash, generate_fake_package_name, make_deterministic_dict


class TestResultSchema:
    """Tests for standardized ResultRecord schema."""

    def test_result_record_serialization(self):
        record = ResultRecord(
            demo="demo-01-blind-verification",
            experiment="comparison",
            seed=42,
            commit="local",
            environment="Python 3.11, Test OS",
            command="make demo DEMO=01",
            result="pass",
            notes="Teaching fixture test",
            duration_ms=120,
            metadata={"total_passed": 3}
        )
        json_str = record.to_json()
        assert "demo-01-blind-verification" in json_str
        assert "Teaching fixture test" in json_str

        # Roundtrip deserialization
        loaded = ResultRecord.from_json(json_str)
        assert loaded.demo == record.demo
        assert loaded.seed == 42
        assert loaded.metadata == {"total_passed": 3}

    def test_write_and_read_results(self, tmp_path):
        out_dir = str(tmp_path / "results")
        rec = write_result(
            demo="demo-02-supply-chain-aibom",
            experiment="drift_detection",
            seed=42,
            result="pass",
            notes="Unit test record",
            output_dir=out_dir
        )
        assert Path(out_dir).exists()
        loaded_list = read_results("demo-02-supply-chain-aibom", results_dir=out_dir)
        assert len(loaded_list) == 1
        assert loaded_list[0].experiment == "drift_detection"

    def test_environment_and_command_helpers(self):
        env = capture_environment()
        assert "Python" in env
        cmd = format_command("demo-05-eviassure", "benchmark")
        assert "make demo DEMO=eviassure EXPERIMENT=benchmark" in cmd
        commit = get_git_commit()
        assert isinstance(commit, str) and len(commit) > 0


class TestReproducibility:
    """Tests for reproducibility utilities."""

    def test_generate_seed_deterministic(self):
        s1 = generate_seed("experiment-alpha")
        s2 = generate_seed("experiment-alpha")
        s3 = generate_seed("experiment-beta")
        assert s1 == s2
        assert s1 != s3
        assert isinstance(s1, int)

    def test_deterministic_shuffle(self):
        items = ["a", "b", "c", "d", "e", "f", "g"]
        shuffled1 = deterministic_shuffle(items, seed=42)
        shuffled2 = deterministic_shuffle(items, seed=42)
        shuffled3 = deterministic_shuffle(items, seed=99)
        assert shuffled1 == shuffled2
        assert shuffled1 != items or len(items) <= 1
        assert sorted(shuffled1) == sorted(items)
        assert shuffled1 != shuffled3

    def test_set_global_seed_and_offline(self):
        set_global_seed(42)
        assert verify_offline() is True


class TestFixtures:
    """Tests for fixture generation and reading."""

    def test_write_and_read_fixture(self, tmp_path):
        fpath = tmp_path / "test_fixture.json"
        data = {"components": ["a", "b"], "status": "active"}
        write_fixture(data, fpath, seed=42)

        assert fpath.exists()
        assert "# seed=42" in fpath.read_text()

        loaded = read_fixture(fpath)
        assert loaded == data

    def test_canary_generation(self):
        c1 = generate_canary(prefix="CANARY_TEST", seed=42)
        c2 = generate_canary(prefix="CANARY_TEST", seed=42)
        c3 = generate_canary(prefix="CANARY_TEST", seed=100)
        assert c1 == c2
        assert c1.startswith("CANARY_TEST_")
        assert c1 != c3

    def test_fake_hash_and_package_name(self):
        h1 = generate_fake_hash(seed=42)
        h2 = generate_fake_hash(seed=42)
        assert h1 == h2
        assert len(h1) == 64

        pkg1 = generate_fake_package_name(seed=42)
        pkg2 = generate_fake_package_name(seed=42)
        assert pkg1 == pkg2
        assert "-" in pkg1

    def test_deterministic_dict(self):
        raw = {"zebra": 1, "apple": 2, "mango": 3}
        sorted_d = make_deterministic_dict(raw, seed=42)
        keys = list(sorted_d.keys())
        assert keys == ["apple", "mango", "zebra"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
