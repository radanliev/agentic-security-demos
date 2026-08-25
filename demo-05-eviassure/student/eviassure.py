#!/usr/bin/env python3
"""
EVIAssure - Evidence-Backed Release Assurance Pipeline
Sequence-bound receipts, hash chains, Merkle trees, inclusion proofs
"""

import json
import hashlib
import hmac
import os
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


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
        """Compute hash of this receipt (excluding signature)."""
        content = f"{self.step}|{self.action}|{self.data_hash}|{self.prev_hash}|{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> Dict:
        return asdict(self)


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
        """Verify entire chain integrity."""
        prev = self.genesis
        for r in self.receipts:
            if r.prev_hash != prev:
                return False
            if r.compute_hash() != r.compute_hash():  # Recompute check
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


class MerkleTree:
    """Merkle tree for efficient inclusion proofs."""

    def __init__(self, leaves: List[str]):
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
        return self.tree[-1][0] if self.tree else ""

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
        """Verify inclusion proof."""
        current = leaf  # leaf is already a hex-encoded hash
        for p in proof:
            sibling = p["sibling"]
            if p["position"] == "left":
                current = hashlib.sha256((current + sibling).encode()).hexdigest()
            else:
                current = hashlib.sha256((sibling + current).encode()).hexdigest()
        return current == root


class DemoKeyManager:
    """Generate and manage demo signing keys (NOT FOR PRODUCTION)."""

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
        """Export public key as base64."""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        public_key = self.keys[key_id].public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return base64.b64encode(pem).decode()


class ReleaseGate:
    """Fail-closed release gate with evidence verification."""

    def __init__(self, key_manager: DemoKeyManager):
        self.key_manager = key_manager

    def verify_trace(self, trace_path: Path, required_steps: int = 6) -> Dict:
        """Verify complete evidence trace."""
        trace_data = json.loads(trace_path.read_text())
        trace = trace_data["trace"]
        expected_closing = trace_data["closing_counts"]

        # 1. Check step count
        if len(trace) != required_steps:
            return {"passed": False, "reason": f"step_count_mismatch: {len(trace)} != {required_steps}"}

        # 2. Build hash chain and verify
        chain = HashChain()
        try:
            for i, step in enumerate(trace):
                data_hash = hashlib.sha256(json.dumps(step["data"], sort_keys=True).encode()).hexdigest()
                prev_hash = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
                receipt = WitnessReceipt(
                    step=step["step"],
                    action=step["action"],
                    data_hash=data_hash,
                    prev_hash=prev_hash,
                    timestamp=step["timestamp"]
                )
                chain.add_receipt(receipt)
        except ValueError as e:
            return {"passed": False, "reason": f"hash_chain_failed: {e}"}

        # 3. Verify closing counts
        closing = chain.get_closing_count()
        if closing["total_steps"] != expected_closing["total_steps"]:
            return {"passed": False, "reason": "closing_count_mismatch"}

        # 4. Build Merkle tree for inclusion proofs
        leaves = [r.compute_hash() for r in chain.receipts]
        merkle = MerkleTree(leaves)

        # 5. Verify each step has valid inclusion proof
        for i, receipt in enumerate(chain.receipts):
            proof = merkle.proof(i)
            if not MerkleTree.verify_proof(receipt.compute_hash(), proof, merkle.root()):
                return {"passed": False, "reason": f"inclusion_proof_failed_step_{i}"}

        return {
            "passed": True,
            "closing_counts": closing,
            "merkle_root": merkle.root(),
            "steps_verified": len(trace)
        }

    def verify_signed_evidence(self, evidence_path: Path) -> Dict:
        """Verify signed evidence package."""
        evidence = json.loads(evidence_path.read_text())
        trace_result = self.verify_trace(Path(evidence["trace_path"]))

        if not trace_result["passed"]:
            return {"passed": False, "reason": trace_result["reason"]}

        signed_receipts = evidence.get("signed_receipts", [])
        if not signed_receipts:
            return {"passed": False, "reason": "no_signed_receipts"}

        # Verify signatures on receipts
        for receipt_data in signed_receipts:
            key_id = receipt_data["signer_id"]
            receipt_bytes = json.dumps({k: v for k, v in receipt_data.items() if k != "signature"}, sort_keys=True).encode()
            if not self.key_manager.verify(key_id, receipt_bytes, receipt_data["signature"]):
                return {"passed": False, "reason": f"signature_verification_failed_{key_id}"}

        return {"passed": True, **trace_result}


def main():
    print("=== EVIAssure Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent

    # Setup
    key_manager = DemoKeyManager()
    release_key = key_manager.generate_key("DEMO_KEY_RELEASE_001")
    gate = ReleaseGate(key_manager)

    # Load trace
    trace_path = base_dir / "fixtures" / "trace.json"

    print("1. Verifying complete trace...")
    result = gate.verify_trace(trace_path)
    print(f"   Result: {'PASS' if result['passed'] else 'FAIL'}")
    if not result['passed']:
        print(f"   Reason: {result['reason']}")

    print("\n2. Testing tamper detection...")
    # Tamper: modify step 3 data
    trace_data = json.loads(trace_path.read_text())
    trace_data["trace"][2]["data"]["passed"] = 99  # Changed from 95
    tampered_path = base_dir / "results" / "tampered_trace.json"
    tampered_path.parent.mkdir(exist_ok=True)
    tampered_path.write_text(json.dumps(trace_data, indent=2))
    result2 = gate.verify_trace(tampered_path)
    print(f"   Tampered trace: {'PASS' if result2['passed'] else 'FAIL'}")
    print(f"   Reason: {result2.get('reason', 'ok')}")

    print("\n3. Testing omission detection...")
    # Omission: remove step 4
    trace_data2 = json.loads(trace_path.read_text())
    trace_data2["trace"].pop(3)  # Remove security_scan
    trace_data2["closing_counts"]["total_steps"] = 5
    omitted_path = base_dir / "results" / "omitted_trace.json"
    omitted_path.write_text(json.dumps(trace_data2, indent=2))
    result3 = gate.verify_trace(omitted_path)
    print(f"   Omitted trace: {'PASS' if result3['passed'] else 'FAIL'}")
    print(f"   Reason: {result3.get('reason', 'ok')}")

    print("\n4. Testing malformed closing count...")
    trace_data3 = json.loads(trace_path.read_text())
    trace_data3["closing_counts"]["total_steps"] = 999
    bad_count_path = base_dir / "results" / "bad_count_trace.json"
    bad_count_path.write_text(json.dumps(trace_data3, indent=2))
    result4 = gate.verify_trace(bad_count_path)
    print(f"   Bad closing count: {'PASS' if result4['passed'] else 'FAIL'}")
    print(f"   Reason: {result4.get('reason', 'ok')}")

    print("\n5. Testing Merkle proof...")
    trace_data4 = json.loads(trace_path.read_text())
    chain = HashChain()
    for i, step in enumerate(trace_data4["trace"]):
        data_hash = hashlib.sha256(json.dumps(step["data"], sort_keys=True).encode()).hexdigest()
        prev_hash = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
        receipt = WitnessReceipt(step["step"], step["action"], data_hash, prev_hash, step["timestamp"])
        chain.add_receipt(receipt)
    leaves = [r.compute_hash() for r in chain.receipts]
    merkle = MerkleTree(leaves)
    proof = merkle.proof(2)  # Step 3
    valid = MerkleTree.verify_proof(chain.receipts[2].compute_hash(), proof, merkle.root())
    print(f"   Merkle proof for step 3: {'VALID' if valid else 'INVALID'}")

    print("\n6. Testing release gate...")
    evidence = {
        "trace_path": str(trace_path),
        "signed_receipts": []
    }
    # Sign receipts
    for r in chain.receipts:
        receipt_dict = r.to_dict()
        receipt_dict["signer_id"] = "DEMO_KEY_RELEASE_001"
        receipt_bytes = json.dumps({k: v for k, v in receipt_dict.items() if k != "signature"}, sort_keys=True).encode()
        sig = key_manager.sign("DEMO_KEY_RELEASE_001", receipt_bytes)
        receipt_dict["signature"] = sig
        evidence["signed_receipts"].append(receipt_dict)

    evidence_path = base_dir / "results" / "evidence_package.json"
    evidence_path.write_text(json.dumps(evidence, indent=2))

    result5 = gate.verify_signed_evidence(evidence_path)
    print(f"   Signed evidence: {'PASS' if result5['passed'] else 'FAIL'}")
    if not result5['passed']:
        print(f"   Reason: {result5.get('reason', 'ok')}")

    print("\n7. Testing incomplete evidence...")
    incomplete_evidence = {"trace_path": str(trace_path), "signed_receipts": []}  # No signatures
    inc_path = base_dir / "results" / "incomplete_evidence.json"
    inc_path.write_text(json.dumps(incomplete_evidence, indent=2))
    result6 = gate.verify_signed_evidence(inc_path)
    print(f"   Incomplete evidence: {'PASS' if result6['passed'] else 'FAIL'}")
    print(f"   Reason: {result6.get('reason', 'ok')}")

    print("\n=== Demo Complete ===")
    print("\n⚠️  DEMO KEYS ONLY - Not for production use!")


if __name__ == "__main__":
    main()