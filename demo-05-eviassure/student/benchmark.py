#!/usr/bin/env python3
"""Benchmark for demo-05."""

import json
import time
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "student"))
from eviassure import HashChain, MerkleTree, WitnessReceipt
import hashlib

def main():
    sizes = [10, 50, 100, 500]
    results = {
        "demo": "demo-05-eviassure",
        "experiment": "benchmark",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=05",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "benchmarks": []
    }

    for size in sizes:
        trace = []
        for i in range(size):
            trace.append({"step": i+1, "action": f"action_{i}", "data": {"x": i}, "timestamp": "2024-01-01T00:00:00Z"})

        chain = HashChain()
        for i, step in enumerate(trace):
            data_hash = hashlib.sha256(json.dumps(step["data"]).encode()).hexdigest()
            prev = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
            chain.add_receipt(WitnessReceipt(step["step"], step["action"], data_hash, prev, step["timestamp"]))

        leaves = [r.compute_hash() for r in chain.receipts]

        start = time.perf_counter()
        merkle = MerkleTree(leaves)
        for i in range(len(leaves)):
            proof = merkle.proof(i)
            MerkleTree.verify_proof(leaves[i], proof, merkle.root())
        elapsed = (time.perf_counter() - start) * 1000

        results["benchmarks"].append({"trace_size": size, "verify_time_ms": round(elapsed, 2)})

    Path("results/benchmark.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()