#!/usr/bin/env python3
"""Benchmark for demo-05: chain rebuild + Merkle verification of every leaf vs trace size."""

import json
import platform
import subprocess
import sys
import time
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "student"))
from eviassure import HashChain, MerkleTree  # noqa: E402

REPEATS = 5  # each size is timed REPEATS times; the minimum is reported (least noise)


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base_dir,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "local"


def main():
    sizes = [10, 50, 100, 500]
    benchmarks = []
    all_valid = True

    for size in sizes:
        trace = [{"step": i + 1, "action": f"action_{i}", "data": {"x": i}, "timestamp": "2024-01-01T00:00:00Z"}
                 for i in range(size)]

        chain_ms = []
        verify_ms = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            chain = HashChain.from_trace(trace)
            leaves = [r.compute_hash() for r in chain.receipts]
            t1 = time.perf_counter()
            merkle = MerkleTree(leaves)
            for i, leaf in enumerate(leaves):
                if not MerkleTree.verify_proof(leaf, merkle.proof(i), merkle.root()):
                    all_valid = False
            t2 = time.perf_counter()
            chain_ms.append((t1 - t0) * 1000)
            verify_ms.append((t2 - t1) * 1000)

        benchmarks.append({
            "trace_size": size,
            "chain_build_ms": round(min(chain_ms), 2),
            "verify_time_ms": round(min(verify_ms), 2),
            "proof_length": len(merkle.proof(0)),
        })

    results = {
        "demo": "demo-05-eviassure",
        "experiment": "benchmark",
        "seed": 42,
        "commit": git_commit(),
        "environment": f"Python {platform.python_version()}, {platform.system()} {platform.release()}",
        "command": "make demo DEMO=05",
        "result": "pass" if all_valid else "fail",
        "notes": f"Synthetic teaching fixture; min of {REPEATS} runs; timings are machine-dependent, verdicts are not",
        "benchmarks": benchmarks,
    }

    out_path = base_dir / "results" / "benchmark.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
