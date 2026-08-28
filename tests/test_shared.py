#!/usr/bin/env python3
"""
Tests for shared library modules:
- shared/result_schema.py
- shared/reproducibility.py
- shared/fixtures.py
"""

import json
import random
import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from shared.result_schema import ResultRecord, write_result, read_results, capture_environment, format_command, get_git_commit
from shared import reproducibility
from shared.reproducibility import generate_seed, deterministic_shuffle, set_global_seed, enforce_offline, verify_offline
from shared.anonymize import Anonymizer, redact_record, pseudonym
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
        assert cmd == "make demo DEMO=05 EXPERIMENT=benchmark"
        assert format_command("05", "benchmark") == cmd
        assert format_command("demo-10-scanbound", "scan") == "make demo DEMO=10 EXPERIMENT=scan"
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

    def test_set_global_seed(self):
        set_global_seed(42)
        a = random.random()
        set_global_seed(42)
        assert random.random() == a

    def test_offline_guard_is_enforced_not_assumed(self, monkeypatch):
        import socket
        # Isolate the guard: restore the real socket functions afterwards.
        for name in ("socket", "create_connection", "getaddrinfo", "gethostbyname"):
            monkeypatch.setattr(socket, name, getattr(socket, name))
        monkeypatch.setattr(reproducibility, "_ORIGINAL_SOCKET_ATTRS", {})
        assert verify_offline() is False  # nothing installed yet -> not verified
        enforce_offline()
        assert verify_offline() is True
        with pytest.raises(RuntimeError):
            socket.create_connection(("192.0.2.1", 80), timeout=0.1)
        with pytest.raises(RuntimeError):
            socket.getaddrinfo("example.com", 80)


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


class TestAnonymize:
    """Tests for the offline PII de-identification helpers (shared/anonymize.py)."""

    def test_pseudonym_is_stable_and_distinct(self):
        # Same input -> same tag (records still join); different input -> different tag.
        assert pseudonym("alice", "USER") == pseudonym("alice", "USER")
        assert pseudonym("alice", "USER") != pseudonym("bob", "USER")
        # The category is part of the namespace.
        assert pseudonym("alice", "USER") != pseudonym("alice", "EMAIL")

    def test_pseudonym_stable_across_instances(self):
        a, b = Anonymizer(), Anonymizer()
        assert a.username("alice") == b.username("alice") == pseudonym("alice", "USER")

    def test_reverse_is_local_only(self):
        a = Anonymizer()
        tag = a.username("alice")
        assert a.reverse(tag) == "alice"
        # A fresh Anonymizer never minted the tag, so it cannot reverse it.
        assert Anonymizer().reverse(tag) == tag

    def test_secrets_are_redacted_not_pseudonymized(self):
        text = '{"user": "alice", "token": "DEMO_TOKEN_ABC123", "password": "hunter2"}'
        out = Anonymizer().deidentify(text)
        assert "DEMO_TOKEN_ABC123" not in out.text
        assert "hunter2" not in out.text
        assert out.text.count("[REDACTED]") == 2
        assert out.changes["secret"] == 2

    def test_identifiers_are_pseudonymized(self):
        text = "login from alice@corp.example at 10.0.0.50"
        a = Anonymizer()
        out = a.deidentify(text)
        assert "alice@corp.example" not in out.text
        assert "10.0.0.50" not in out.text
        assert out.changes == {"email": 1, "ipv4": 1}
        # The pseudonyms this Anonymizer minted are recoverable locally.
        email_tag = a.email("alice@corp.example")
        assert a.reverse(email_tag) == "alice@corp.example"

    def test_username_field_pseudonymized_value_stable(self):
        a = Anonymizer()
        first = a.deidentify('{"user": "alice"}')
        second = a.deidentify('{"account": "alice"}')
        # Same person, two field names, one stable pseudonym -> the join survives.
        tag = a.username("alice")
        assert tag in first.text and tag in second.text

    def test_deidentify_is_deterministic(self):
        text = '{"user": "alice", "ip": "10.0.0.50", "token": "DEMO_TOKEN_ABC123"}'
        assert Anonymizer().deidentify(text).text == Anonymizer().deidentify(text).text

    def test_redact_record_is_deny_by_default(self):
        record = {"sha256": "abc123", "detections": 41,
                  "meaningful_name": "Payroll_Q3.xls", "author": "Jane Doe",
                  "submitter_email": "jane@corp.example"}
        out, removed = redact_record(record, allow=["sha256", "detections", "engine_versions"])
        # Allowlisted analytic fields survive; every other (incl. unseen) field is masked.
        assert out["sha256"] == "abc123" and out["detections"] == 41
        assert out["meaningful_name"] == "[PII-REDACTED]"
        assert out["author"] == "[PII-REDACTED]"
        assert out["submitter_email"] == "[PII-REDACTED]"
        assert set(removed) == {"meaningful_name", "author", "submitter_email"}

    def test_report_summary_reads_cleanly(self):
        out = Anonymizer().deidentify('{"user": "alice", "token": "DEMO_TOKEN_ABC123"}')
        assert out.summary() == "1 usernames, 1 secrets"
        assert Anonymizer().deidentify("nothing here").summary() == "no identifiers or secrets found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
