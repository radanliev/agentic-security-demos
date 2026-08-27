#!/usr/bin/env python3
"""
EVIAssure - Evidence-Backed Release Assurance Pipeline
Sequence-bound receipts, hash chains, Merkle trees, inclusion proofs, signed receipts.

The lesson this file demonstrates:
  * a hash chain proves that a trace is *self-consistent*; it cannot tell a
    genuine trace from a forged one that was rebuilt consistently;
  * binding a trace to what actually happened needs an expectation the forger
    cannot edit — here, receipts signed by an authorised release key that the
    gate compares field-by-field against the chain it rebuilds from the trace.
"""

import base64
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

SIGNED_FIELDS = ("step", "action", "data_hash", "prev_hash", "timestamp")


@dataclass
class WitnessReceipt:
    """Sequence-bound witness receipt."""
    step: int
    action: str
    data_hash: str
    prev_hash: str
    timestamp: str
    signature: Optional[str] = None
    signer_id: Optional[str] = None

    def compute_hash(self) -> str:
        """Compute hash of this receipt (excluding signature and signer)."""
        content = f"{self.step}|{self.action}|{self.data_hash}|{self.prev_hash}|{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> Dict:
        return asdict(self)


def data_hash_of(data) -> str:
    """Canonical hash of a step's data payload (sorted keys, so dict order cannot matter)."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


class HashChain:
    """Hash chain for sequence integrity."""

    def __init__(self):
        self.receipts: List[WitnessReceipt] = []
        self.genesis = "0" * 64

    def add_receipt(self, receipt: WitnessReceipt) -> WitnessReceipt:
        """Add receipt to chain, verifying sequence."""
        if not self.receipts:
            expected_prev = self.genesis
        else:
            expected_prev = self.receipts[-1].compute_hash()

        if receipt.prev_hash != expected_prev:
            raise ValueError(f"Hash chain break: expected {expected_prev}, got {receipt.prev_hash}")

        self.receipts.append(receipt)
        return receipt

    def verify_chain(self) -> bool:
        """Walk the chain: every receipt's prev_hash must equal the recomputed hash of its predecessor."""
        prev = self.genesis
        for r in self.receipts:
            if r.prev_hash != prev:
                return False
            prev = r.compute_hash()
        return True

    def get_closing_count(self) -> Dict:
        """Get closing counts for verification."""
        return {
            "total_steps": len(self.receipts),
            "final_hash": self.receipts[-1].compute_hash() if self.receipts else self.genesis,
            "genesis": self.genesis
        }

    @classmethod
    def from_trace(cls, trace: List[Dict]) -> "HashChain":
        """Rebuild the chain from a trace's steps (the only way a verifier can derive receipts)."""
        chain = cls()
        for i, step in enumerate(trace):
            prev_hash = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
            chain.add_receipt(WitnessReceipt(
                step=step["step"],
                action=step["action"],
                data_hash=data_hash_of(step["data"]),
                prev_hash=prev_hash,
                timestamp=step["timestamp"],
            ))
        return chain


class MerkleTree:
    """Merkle tree for efficient inclusion proofs."""

    def __init__(self, leaves: List[str]):
        if not leaves:
            raise ValueError("MerkleTree needs at least one leaf")
        self.leaves = leaves
        self.tree = self._build_tree(self.leaves)

    def _build_tree(self, leaves: List[str]) -> List[List[str]]:
        tree = [leaves]
        level = leaves
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else left
                combined = hashlib.sha256((left + right).encode()).hexdigest()
                next_level.append(combined)
            tree.append(next_level)
            level = next_level
        return tree

    def root(self) -> str:
        return self.tree[-1][0]

    def proof(self, index: int) -> List[Dict]:
        """Generate inclusion proof for leaf at index."""
        proof = []
        for level in range(len(self.tree) - 1):
            level_nodes = self.tree[level]
            # Determine if index is left (even) or right (odd) child
            is_left = index % 2 == 0
            sibling_idx = index + 1 if is_left else index - 1

            # Handle case where sibling doesn't exist (odd number of nodes, last node pairs with itself)
            if sibling_idx >= len(level_nodes):
                sibling_idx = index  # Pair with itself

            sibling = level_nodes[sibling_idx]
            proof.append({"level": level, "sibling": sibling, "position": "left" if is_left else "right"})
            index //= 2
        return proof

    @staticmethod
    def verify_proof(leaf: str, proof: List[Dict], root: str) -> bool:
        """Verify inclusion proof against a root the verifier already trusts."""
        current = leaf  # leaf is already a hex-encoded hash
        for p in proof:
            sibling = p["sibling"]
            if p["position"] == "left":
                current = hashlib.sha256((current + sibling).encode()).hexdigest()
            else:
                current = hashlib.sha256((sibling + current).encode()).hexdigest()
        return current == root


class DemoKeyManager:
    """Generate and manage demo signing keys (NOT FOR PRODUCTION).

    Keys are Ed25519, generated in memory per run and never written to disk.
    """

    def __init__(self):
        self.keys: Dict[str, ed25519.Ed25519PrivateKey] = {}

    def generate_key(self, key_id: str) -> ed25519.Ed25519PrivateKey:
        """Generate a new demo key."""
        if not key_id.startswith("DEMO_KEY_"):
            raise ValueError(f"Key ID must start with 'DEMO_KEY_': {key_id}")
        private_key = ed25519.Ed25519PrivateKey.generate()
        self.keys[key_id] = private_key
        return private_key

    def sign(self, key_id: str, data: bytes) -> str:
        """Sign data with demo key."""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        signature = self.keys[key_id].sign(data)
        return base64.b64encode(signature).decode()

    def verify(self, key_id: str, data: bytes, signature_b64: str) -> bool:
        """Verify signature with demo key."""
        if key_id not in self.keys:
            return False
        try:
            public_key = self.keys[key_id].public_key()
            signature = base64.b64decode(signature_b64)
            public_key.verify(signature, data)
            return True
        except Exception:
            return False

    def export_public_key(self, key_id: str) -> str:
        """Export public key as base64 (raw 32 bytes)."""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        public_key = self.keys[key_id].public_key()
        raw = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return base64.b64encode(raw).decode()


def receipt_payload(receipt_data: Dict) -> bytes:
    """Canonical bytes that are signed: every field except the signature, keys sorted.

    Signer and verifier MUST use this same function, and signer_id must be set
    before signing (it is part of the signed payload).
    """
    return json.dumps({k: v for k, v in receipt_data.items() if k != "signature"}, sort_keys=True).encode()


def sign_receipt(key_manager: DemoKeyManager, key_id: str, receipt: WitnessReceipt) -> Dict:
    """Return a signed copy of a receipt as a dict ready for an evidence package."""
    d = receipt.to_dict()
    d["signer_id"] = key_id
    d["signature"] = key_manager.sign(key_id, receipt_payload(d))
    return d


class ReleaseGate:
    """Fail-closed release gate with evidence verification and authorized signer checking.

    authorized_signer_ids=None means "every key this DemoKeyManager holds is trusted";
    pass an explicit set to model a real trust store.
    """

    def __init__(self, key_manager: DemoKeyManager, authorized_signer_ids: Optional[Set[str]] = None):
        self.key_manager = key_manager
        self.authorized_signer_ids = set(authorized_signer_ids) if authorized_signer_ids is not None else None

    def _rebuild(self, trace_path: Path, required_steps: int) -> Tuple[Dict, Optional[HashChain]]:
        """Rebuild the chain from a trace file and run the checks that need no external evidence."""
        trace_data = json.loads(trace_path.read_text())
        trace = trace_data["trace"]
        expected_closing = trace_data["closing_counts"]

        # 1. Check step count against an expectation held OUTSIDE the trace
        if len(trace) != required_steps:
            return {"passed": False, "reason": f"step_count_mismatch: {len(trace)} != {required_steps}"}, None

        # 2. Steps must be numbered 1..n in order (sequence-bound)
        for i, step in enumerate(trace):
            if step["step"] != i + 1:
                return {"passed": False, "reason": f"step_numbering_mismatch: index {i} carries step {step['step']}"}, None

        # 3. Rebuild the hash chain; add_receipt raises on any broken prev link
        try:
            chain = HashChain.from_trace(trace)
        except ValueError as e:
            return {"passed": False, "reason": f"hash_chain_failed: {e}"}, None

        # 4. Verify the trace's own closing declaration
        closing = chain.get_closing_count()
        if closing["total_steps"] != expected_closing["total_steps"]:
            return {"passed": False, "reason": "closing_count_mismatch"}, None

        # 5. Merkle root over the receipt hashes. NOTE: proving our own leaves against a
        #    root we just computed from the same file can never fail, so the gate does not
        #    do that. The root is returned so it can be anchored externally (Exercise 5.2).
        merkle = MerkleTree([r.compute_hash() for r in chain.receipts])

        return {
            "passed": True,
            "closing_counts": closing,
            "merkle_root": merkle.root(),
            "steps_verified": len(trace)
        }, chain

    def verify_trace(self, trace_path: Path, required_steps: int = 6) -> Dict:
        """Verify a trace's internal consistency (chain, counts, numbering).

        A trace that was forged consistently PASSES this check: nothing here binds the
        trace to what really happened. Use verify_signed_evidence for that.
        """
        result, _chain = self._rebuild(trace_path, required_steps)
        return result

    def verify_signed_evidence(self, evidence_path: Path, required_steps: int = 6) -> Dict:
        """Verify a signed evidence package: the trace must rebuild into exactly the receipts
        that an authorised signer signed, one per step, with valid signatures."""
        evidence = json.loads(evidence_path.read_text())
        trace_result, chain = self._rebuild(Path(evidence["trace_path"]), required_steps)
        if not trace_result["passed"]:
            return {"passed": False, "reason": trace_result["reason"]}

        signed_receipts = evidence.get("signed_receipts", [])
        if not signed_receipts:
            return {"passed": False, "reason": "no_signed_receipts"}
        if len(signed_receipts) != len(chain.receipts):
            return {"passed": False,
                    "reason": f"signed_receipt_count_mismatch: {len(signed_receipts)} != {len(chain.receipts)}"}

        for rebuilt, receipt_data in zip(chain.receipts, signed_receipts):
            key_id = receipt_data.get("signer_id")

            # Trust boundary check: is signer authorised by the gate?
            if not key_id or (self.authorized_signer_ids is not None and key_id not in self.authorized_signer_ids):
                return {"passed": False, "reason": f"unauthorized_signer_{key_id}"}

            # Cryptographic check: did that key sign exactly this receipt?
            if not self.key_manager.verify(key_id, receipt_payload(receipt_data), receipt_data.get("signature", "")):
                return {"passed": False, "reason": f"signature_verification_failed_{key_id}"}

            # Binding check: the signed receipt must be the receipt the trace rebuilds to
            for field_name in SIGNED_FIELDS:
                if receipt_data.get(field_name) != getattr(rebuilt, field_name):
                    return {"passed": False, "reason": f"receipt_mismatch_step_{rebuilt.step}_{field_name}"}

        return {"passed": True, **trace_result}


def _verdict(result: Dict) -> str:
    return f"{'PASS' if result['passed'] else 'FAIL'}  Reason: {result.get('reason', 'ok')}"


def main():
    print("=== EVIAssure Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    results_dir = base_dir / "results"
    results_dir.mkdir(exist_ok=True)

    # Setup: one release key, generated in memory for this run only
    key_manager = DemoKeyManager()
    key_manager.generate_key("DEMO_KEY_RELEASE_001")
    gate = ReleaseGate(key_manager, authorized_signer_ids={"DEMO_KEY_RELEASE_001"})

    trace_path = base_dir / "fixtures" / "trace.json"
    original = trace_path.read_text()

    def write_variant(name: str, mutate) -> Path:
        data = json.loads(original)
        mutate(data)
        path = results_dir / name
        path.write_text(json.dumps(data, indent=2))
        return path

    print("1. Verifying complete trace (chain check)...")
    print(f"   Complete trace: {_verdict(gate.verify_trace(trace_path))}")

    print("\n2. Tampering with step 3 (tests passed 95 -> 99), chain check only...")
    tampered_path = write_variant("tampered_trace.json", lambda d: d["trace"][2]["data"].__setitem__("passed", 99))
    print(f"   Tampered trace: {_verdict(gate.verify_trace(tampered_path))}")
    print("   (expected: the forged chain is self-consistent, so the chain check alone CANNOT catch it)")

    print("\n3. Omitting step 4 (security_scan) and fixing the count to 5...")
    omitted_path = write_variant("omitted_trace.json",
                                 lambda d: (d["trace"].pop(3), d["closing_counts"].__setitem__("total_steps", 5)))
    print(f"   Omitted trace: {_verdict(gate.verify_trace(omitted_path))}")

    print("\n4. Forging the closing count (999)...")
    bad_count_path = write_variant("bad_count_trace.json", lambda d: d["closing_counts"].__setitem__("total_steps", 999))
    print(f"   Bad closing count: {_verdict(gate.verify_trace(bad_count_path))}")

    print("\n5. Merkle inclusion proof for step 3...")
    chain = HashChain.from_trace(json.loads(original)["trace"])
    leaves = [r.compute_hash() for r in chain.receipts]
    merkle = MerkleTree(leaves)
    proof = merkle.proof(2)  # Step 3
    valid = MerkleTree.verify_proof(leaves[2], proof, merkle.root())
    forged_leaf = leaves[2][:-1] + ("0" if leaves[2][-1] != "0" else "1")
    print(f"   Merkle proof for step 3: {'VALID' if valid else 'INVALID'}  ({len(proof)} sibling hashes for {len(leaves)} leaves)")
    print(f"   Same proof, one hex digit of the leaf changed: {'VALID' if MerkleTree.verify_proof(forged_leaf, proof, merkle.root()) else 'INVALID'}")

    print("\n6. Signing every receipt with DEMO_KEY_RELEASE_001 and verifying the package...")
    signed = [sign_receipt(key_manager, "DEMO_KEY_RELEASE_001", r) for r in chain.receipts]
    evidence_path = results_dir / "evidence_package.json"
    evidence_path.write_text(json.dumps({"trace_path": str(trace_path), "signed_receipts": signed}, indent=2))
    print(f"   Signed evidence: {_verdict(gate.verify_signed_evidence(evidence_path))}")

    print("\n7. Tampered trace from step 2 presented with the ORIGINAL signed receipts...")
    tampered_evidence_path = results_dir / "tampered_evidence.json"
    tampered_evidence_path.write_text(json.dumps({"trace_path": str(tampered_path), "signed_receipts": signed}, indent=2))
    print(f"   Tampered evidence: {_verdict(gate.verify_signed_evidence(tampered_evidence_path))}")
    print("   (the signatures are genuine, but they cover the receipts of the ORIGINAL step 3)")

    print("\n8. Evidence package with no signed receipts...")
    inc_path = results_dir / "incomplete_evidence.json"
    inc_path.write_text(json.dumps({"trace_path": str(trace_path), "signed_receipts": []}, indent=2))
    print(f"   Incomplete evidence: {_verdict(gate.verify_signed_evidence(inc_path))}")

    print("\n9. Tampered trace re-signed by an attacker's own key (DEMO_KEY_ATTACKER)...")
    key_manager.generate_key("DEMO_KEY_ATTACKER")
    attacker_chain = HashChain.from_trace(json.loads(tampered_path.read_text())["trace"])
    attacker_signed = [sign_receipt(key_manager, "DEMO_KEY_ATTACKER", r) for r in attacker_chain.receipts]
    attacker_path = results_dir / "attacker_signed_evidence.json"
    attacker_path.write_text(json.dumps({"trace_path": str(tampered_path), "signed_receipts": attacker_signed}, indent=2))
    print(f"   Attacker-signed evidence: {_verdict(gate.verify_signed_evidence(attacker_path))}")

    print("\n=== Demo Complete ===")
    print("\n⚠️  DEMO KEYS ONLY - generated in memory for this run, not for production use!")


if __name__ == "__main__":
    main()
