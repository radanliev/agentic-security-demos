#!/usr/bin/env python3
"""
Tests for Demo 05: EVIAssure

Every test that claims a check "detects" something also proves the check is
necessary: the same input passes when the check is absent.
"""

import hashlib
import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from eviassure import (  # noqa: E402
    DemoKeyManager, HashChain, MerkleTree, ReleaseGate, WitnessReceipt,
    data_hash_of, receipt_payload, sign_receipt,
)

TRACE_PATH = DEMO_DIR / "fixtures" / "trace.json"
RELEASE_KEY = "DEMO_KEY_RELEASE_001"


def load_trace() -> dict:
    return json.loads(TRACE_PATH.read_text())


def write_json(path: Path, data) -> Path:
    path.write_text(json.dumps(data, indent=2))
    return path


@pytest.fixture
def key_manager():
    km = DemoKeyManager()
    km.generate_key(RELEASE_KEY)
    return km


@pytest.fixture
def gate(key_manager):
    return ReleaseGate(key_manager, authorized_signer_ids={RELEASE_KEY})


@pytest.fixture
def signed_receipts(key_manager):
    chain = HashChain.from_trace(load_trace()["trace"])
    return [sign_receipt(key_manager, RELEASE_KEY, r) for r in chain.receipts]


@pytest.fixture
def tampered_trace(tmp_path):
    data = load_trace()
    data["trace"][2]["data"]["passed"] = 99  # was 95
    return write_json(tmp_path / "tampered_trace.json", data)


class TestHashChain:

    def test_chain_links_and_detects_edit(self):
        chain = HashChain.from_trace(load_trace()["trace"])
        assert chain.verify_chain() is True
        for prev, cur in zip(chain.receipts, chain.receipts[1:]):
            assert cur.prev_hash == prev.compute_hash()
        chain.receipts[2].action = "tampered"
        assert chain.verify_chain() is False

    def test_every_field_is_hash_covered(self):
        """Changing any one field of a receipt changes its hash (tamper-evidence scope)."""
        base = WitnessReceipt(3, "run_tests", data_hash_of({"passed": 95}), "0" * 64, "2024-01-15T10:05:00Z")
        for field_name, new_value in [("step", 4), ("action", "x"), ("data_hash", data_hash_of({"passed": 99})),
                                      ("prev_hash", "1" * 64), ("timestamp", "2024-01-15T10:05:01Z")]:
            changed = WitnessReceipt(**{**base.to_dict(), field_name: new_value})
            assert changed.compute_hash() != base.compute_hash(), field_name

    def test_data_hash_is_canonical(self):
        assert data_hash_of({"a": 1, "b": 2}) == data_hash_of({"b": 2, "a": 1})
        assert data_hash_of({"passed": 95}) != data_hash_of({"passed": 99})

    def test_closing_counts(self):
        chain = HashChain.from_trace(load_trace()["trace"])
        closing = chain.get_closing_count()
        assert closing["total_steps"] == 6
        assert closing["final_hash"] == chain.receipts[-1].compute_hash()

    def test_omission_breaks_the_link(self):
        chain = HashChain()
        r1 = WitnessReceipt(1, "act1", "hash1", chain.genesis, "2024-01-01T00:00:00Z")
        chain.add_receipt(r1)
        r2 = WitnessReceipt(2, "act2", "hash2", r1.compute_hash(), "2024-01-01T00:01:00Z")
        chain.add_receipt(r2)
        r3 = WitnessReceipt(3, "act3", "hash3", r2.compute_hash(), "2024-01-01T00:02:00Z")
        chain.add_receipt(r3)

        omitted_chain = HashChain()
        omitted_chain.add_receipt(r1)
        with pytest.raises(ValueError, match="Hash chain break"):
            omitted_chain.add_receipt(r3)


class TestMerkle:

    @pytest.mark.parametrize("n", [1, 2, 3, 6, 7, 8, 16])
    def test_inclusion_proofs_verify_for_every_leaf(self, n):
        leaves = [hashlib.sha256(f"step_{i}".encode()).hexdigest() for i in range(n)]
        tree = MerkleTree(leaves)
        assert len(tree.root()) == 64
        for i in range(n):
            assert MerkleTree.verify_proof(leaves[i], tree.proof(i), tree.root()) is True

    def test_forged_leaf_or_proof_fails(self):
        leaves = [hashlib.sha256(f"step_{i}".encode()).hexdigest() for i in range(6)]
        tree = MerkleTree(leaves)
        proof = tree.proof(2)
        forged_leaf = leaves[2][:-1] + ("0" if leaves[2][-1] != "0" else "1")
        assert MerkleTree.verify_proof(forged_leaf, proof, tree.root()) is False
        assert MerkleTree.verify_proof(leaves[3], proof, tree.root()) is False  # proof is for leaf 2
        bad_proof = [{"level": 0, "sibling": "deadbeef", "position": "right"}]
        assert MerkleTree.verify_proof(leaves[0], bad_proof, tree.root()) is False
        swapped = [{**p, "position": "right" if p["position"] == "left" else "left"} for p in proof]
        assert MerkleTree.verify_proof(leaves[2], swapped, tree.root()) is False

    def test_partial_verification(self):
        """A leaf is verifiable against the root without the other leaves (checkpointing)."""
        leaves = [hashlib.sha256(f"event_{i}".encode()).hexdigest() for i in range(8)]
        tree = MerkleTree(leaves)
        assert MerkleTree.verify_proof(leaves[3], tree.proof(3), tree.root()) is True
        assert len(tree.proof(3)) == 3  # log2(8)


class TestKeys:

    def test_demo_key_signing(self, key_manager):
        key_manager.generate_key("DEMO_KEY_TEST")
        data = b"test message"
        sig = key_manager.sign("DEMO_KEY_TEST", data)
        assert key_manager.verify("DEMO_KEY_TEST", data, sig) is True
        assert key_manager.verify("DEMO_KEY_TEST", b"wrong", sig) is False
        assert key_manager.verify("DEMO_KEY_TEST", data, "not base64!!") is False
        assert key_manager.verify("DEMO_KEY_UNKNOWN", data, sig) is False
        with pytest.raises(ValueError):
            key_manager.generate_key("PROD_KEY")

    def test_keys_are_not_interchangeable(self):
        km = DemoKeyManager()
        km.generate_key("DEMO_KEY_signer_v1")
        km.generate_key("DEMO_KEY_signer_v2")
        data = b"evidence_payload_test"
        sig1 = km.sign("DEMO_KEY_signer_v1", data)
        sig2 = km.sign("DEMO_KEY_signer_v2", data)
        assert km.verify("DEMO_KEY_signer_v1", data, sig1) is True
        assert km.verify("DEMO_KEY_signer_v2", data, sig2) is True
        assert km.verify("DEMO_KEY_signer_v1", data, sig2) is False
        assert km.export_public_key("DEMO_KEY_signer_v1") != km.export_public_key("DEMO_KEY_signer_v2")

    def test_sign_receipt_payload_includes_signer_id(self, key_manager):
        r = WitnessReceipt(1, "init", "h", "0" * 64, "t")
        signed = sign_receipt(key_manager, RELEASE_KEY, r)
        assert signed["signer_id"] == RELEASE_KEY
        assert key_manager.verify(RELEASE_KEY, receipt_payload(signed), signed["signature"])
        # Signing before setting signer_id (the easy mistake) produces a receipt the gate rejects
        d = r.to_dict()
        d["signature"] = key_manager.sign(RELEASE_KEY, receipt_payload(d))
        d["signer_id"] = RELEASE_KEY
        assert key_manager.verify(RELEASE_KEY, receipt_payload(d), d["signature"]) is False


class TestTraceChecks:
    """Checks that need nothing but the trace file: they catch inconsistent forgeries only."""

    def test_complete_trace_passes(self, gate):
        result = gate.verify_trace(TRACE_PATH)
        assert result["passed"] is True
        assert result["steps_verified"] == 6
        assert len(result["merkle_root"]) == 64

    def test_self_consistent_forgery_passes_the_chain_check(self, gate, tampered_trace):
        """The module's central lesson: a consistently rebuilt forgery is invisible to the chain."""
        assert gate.verify_trace(tampered_trace)["passed"] is True

    def test_omitted_step_fails_even_with_fixed_count(self, gate, tmp_path):
        data = load_trace()
        data["trace"].pop(3)
        data["closing_counts"]["total_steps"] = 5
        path = write_json(tmp_path / "omitted.json", data)
        result = gate.verify_trace(path)
        assert result["passed"] is False
        assert result["reason"] == "step_count_mismatch: 5 != 6"
        # Even a verifier that expected 5 steps sees the gap in the numbering (1,2,3,5,6)
        assert gate.verify_trace(path, required_steps=5)["reason"] == "step_numbering_mismatch: index 3 carries step 5"

    def test_renumbered_omission_needs_an_external_expectation(self, gate, signed_receipts, tmp_path):
        """Exercise 5.3: delete step 4, renumber 5-6 to 4-5, fix the count. Nothing inside the
        trace can catch it; the verifier's own step count or the signed receipts can."""
        data = load_trace()
        data["trace"].pop(3)
        for i, step in enumerate(data["trace"]):
            step["step"] = i + 1
        data["closing_counts"]["total_steps"] = 5
        path = write_json(tmp_path / "renumbered.json", data)
        assert gate.verify_trace(path)["reason"] == "step_count_mismatch: 5 != 6"
        assert gate.verify_trace(path, required_steps=5)["passed"] is True
        pkg = write_json(tmp_path / "pkg.json", {"trace_path": str(path), "signed_receipts": signed_receipts})
        assert gate.verify_signed_evidence(pkg, required_steps=5)["reason"] == "signed_receipt_count_mismatch: 6 != 5"

    def test_stale_closing_count_rejected(self, gate, tmp_path):
        data = load_trace()
        data["trace"].pop(3)
        for i, step in enumerate(data["trace"]):
            step["step"] = i + 1  # forger renumbers but forgets the closing declaration
        path = write_json(tmp_path / "stale_count.json", data)
        assert gate.verify_trace(path, required_steps=5)["reason"] == "closing_count_mismatch"

    def test_malformed_closing_count_rejected(self, gate, tmp_path):
        data = load_trace()
        data["closing_counts"]["total_steps"] = 999
        result = gate.verify_trace(write_json(tmp_path / "bad.json", data))
        assert result["passed"] is False
        assert result["reason"] == "closing_count_mismatch"

    def test_step_numbering_checked(self, gate, tmp_path):
        data = load_trace()
        data["trace"][3]["step"], data["trace"][4]["step"] = 5, 4
        result = gate.verify_trace(write_json(tmp_path / "renumbered.json", data))
        assert result["passed"] is False
        assert result["reason"].startswith("step_numbering_mismatch")


class TestSignedGate:
    """The gate binds the trace to a signer: this is where tampering is actually detected."""

    def test_signed_package_passes(self, gate, signed_receipts, tmp_path):
        pkg = write_json(tmp_path / "pkg.json", {"trace_path": str(TRACE_PATH), "signed_receipts": signed_receipts})
        result = gate.verify_signed_evidence(pkg)
        assert result["passed"] is True
        assert result["steps_verified"] == 6

    def test_tampered_trace_with_original_signatures_fails(self, gate, signed_receipts, tampered_trace, tmp_path):
        pkg = write_json(tmp_path / "pkg.json", {"trace_path": str(tampered_trace), "signed_receipts": signed_receipts})
        result = gate.verify_signed_evidence(pkg)
        assert result["passed"] is False
        assert result["reason"] == "receipt_mismatch_step_3_data_hash"

    def test_receipt_edited_to_match_tampered_trace_fails_signature(self, gate, key_manager, signed_receipts,
                                                                   tampered_trace, tmp_path):
        edited = [dict(r) for r in signed_receipts]
        rebuilt = HashChain.from_trace(json.loads(tampered_trace.read_text())["trace"]).receipts
        for d, r in zip(edited, rebuilt):
            d["data_hash"], d["prev_hash"] = r.data_hash, r.prev_hash  # forger fixes the fields, keeps old signatures
        pkg = write_json(tmp_path / "pkg.json", {"trace_path": str(tampered_trace), "signed_receipts": edited})
        assert gate.verify_signed_evidence(pkg)["reason"] == f"signature_verification_failed_{RELEASE_KEY}"

    def test_signature_covers_every_receipt_field(self, gate, key_manager, signed_receipts, tmp_path):
        """Tamper the last step's data (so no later prev_hash changes) and edit only that receipt's
        field: the signature must fail for every signed field, or a forger could edit around it."""
        data = load_trace()
        data["trace"][5]["data"]["key_id"] = "DEMO_KEY_ATTACKER"
        last = write_json(tmp_path / "last_tampered.json", data)
        rebuilt = HashChain.from_trace(data["trace"]).receipts[5]
        for field_name in ("step", "action", "data_hash", "prev_hash", "timestamp", "signer_id"):
            edited = [dict(r) for r in signed_receipts]
            edited[5][field_name] = getattr(rebuilt, field_name) if field_name != "signer_id" else "DEMO_KEY_ATTACKER"
            if field_name == "signer_id":
                key_manager.generate_key("DEMO_KEY_ATTACKER")
                gate = ReleaseGate(key_manager)  # trusts both keys: only the signature can save us
            pkg = write_json(tmp_path / f"edit_{field_name}.json", {"trace_path": str(last), "signed_receipts": edited})
            assert gate.verify_signed_evidence(pkg)["passed"] is False, field_name
            assert "signature_verification_failed" in gate.verify_signed_evidence(pkg)["reason"] or \
                   "receipt_mismatch" in gate.verify_signed_evidence(pkg)["reason"], field_name

    def test_every_receipt_must_be_signed(self, gate, signed_receipts, tmp_path):
        one = write_json(tmp_path / "one.json", {"trace_path": str(TRACE_PATH), "signed_receipts": signed_receipts[:1]})
        assert gate.verify_signed_evidence(one)["reason"] == "signed_receipt_count_mismatch: 1 != 6"
        dup = write_json(tmp_path / "dup.json", {"trace_path": str(TRACE_PATH), "signed_receipts": [signed_receipts[0]] * 6})
        assert gate.verify_signed_evidence(dup)["reason"] == "receipt_mismatch_step_2_step"

    def test_corrupted_signature_fails(self, gate, signed_receipts, tmp_path):
        forged = [dict(r) for r in signed_receipts]
        s = forged[0]["signature"]
        forged[0]["signature"] = ("A" if s[0] != "A" else "B") + s[1:]
        pkg = write_json(tmp_path / "pkg.json", {"trace_path": str(TRACE_PATH), "signed_receipts": forged})
        assert gate.verify_signed_evidence(pkg)["reason"] == f"signature_verification_failed_{RELEASE_KEY}"

    def test_release_blocked_on_incomplete_evidence(self, gate, tmp_path):
        pkg = write_json(tmp_path / "inc.json", {"trace_path": str(TRACE_PATH), "signed_receipts": []})
        result = gate.verify_signed_evidence(pkg)
        assert result["passed"] is False
        assert result["reason"] == "no_signed_receipts"

    def test_unauthorized_signer_rejected(self, key_manager, tampered_trace, tmp_path):
        """A valid signature under a key the gate does not trust is worthless."""
        key_manager.generate_key("DEMO_KEY_ATTACKER")
        strict_gate = ReleaseGate(key_manager, authorized_signer_ids={RELEASE_KEY})
        chain = HashChain.from_trace(json.loads(tampered_trace.read_text())["trace"])
        attacker_signed = [sign_receipt(key_manager, "DEMO_KEY_ATTACKER", r) for r in chain.receipts]
        pkg = write_json(tmp_path / "att.json", {"trace_path": str(tampered_trace), "signed_receipts": attacker_signed})
        result = strict_gate.verify_signed_evidence(pkg)
        assert result["passed"] is False
        assert result["reason"] == "unauthorized_signer_DEMO_KEY_ATTACKER"
        # Without an explicit trust store the gate trusts every key the manager holds
        assert ReleaseGate(key_manager).verify_signed_evidence(pkg)["passed"] is True

    def test_missing_signer_id_rejected(self, gate, signed_receipts, tmp_path):
        anon = [dict(r) for r in signed_receipts]
        anon[0].pop("signer_id")
        pkg = write_json(tmp_path / "anon.json", {"trace_path": str(TRACE_PATH), "signed_receipts": anon})
        assert gate.verify_signed_evidence(pkg)["reason"] == "unauthorized_signer_None"


class TestDemoRun:

    def test_main_prints_honest_verdicts(self, capsys):
        import eviassure
        eviassure.main()
        out = capsys.readouterr().out
        assert "Tampered trace: PASS  Reason: ok" in out          # chain check alone cannot catch it
        assert "Tampered evidence: FAIL  Reason: receipt_mismatch_step_3_data_hash" in out
        assert "Attacker-signed evidence: FAIL  Reason: unauthorized_signer_DEMO_KEY_ATTACKER" in out
        assert "Incomplete evidence: FAIL  Reason: no_signed_receipts" in out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
