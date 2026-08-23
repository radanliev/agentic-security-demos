# Demo 05: Evidence-Backed Release Assurance (EVIAssure)

## Learning Objectives

- Build cryptographically verifiable evidence pipelines
- Implement sequence-bound witness receipts
- Create hash chains and Merkle trees for integrity
- Verify inclusion proofs
- Design fail-closed release gates
- Detect tampering and omission

## Conceptual Explanation

**Evidence-backed release assurance** uses cryptographic evidence to support release decisions. Instead of trusting "it passed tests," you verify a tamper-evident chain of evidence.

### The Pipeline

```
Step 1: init          →  WitnessReceipt(hash=H1, prev=genesis)
Step 2: load_config   →  WitnessReceipt(hash=H2, prev=H1)
Step 3: run_tests     →  WitnessReceipt(hash=H3, prev=H2)
Step 4: security_scan →  WitnessReceipt(hash=H4, prev=H3)
Step 5: build_artifact→  WitnessReceipt(hash=H5, prev=H4)
Step 6: sign_release  →  WitnessReceipt(hash=H6, prev=H5)
                              ↓
                       Merkle Tree Root
                              ↓
                       Signed Evidence Package
                              ↓
                       Fail-Closed Release Gate
```

## Safety Notice

⚠️ **Teaching demonstration only.**
- Demo keys generated at runtime (`DEMO_KEY_*`)
- **Not production signing keys** — do not use for real releases
- No private keys, certificates, or real PKI
- Synthetic traces only

## Running the Demo

```bash
make demo DEMO=05
```

### Expected Output

```
1. Verifying complete trace... PASS
2. Testing tamper detection... FAIL (hash_chain_failed)
3. Testing omission detection... FAIL (closing_count_mismatch)
4. Testing malformed closing count... FAIL (closing_count_mismatch)
5. Testing Merkle proof... VALID
6. Testing release gate... PASS
7. Testing incomplete evidence... FAIL (no_signed_receipts)
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **WitnessReceipt** | Sequence-bound attestation |
| **HashChain** | Genesis → H1 → H2 → ... → Hn |
| **MerkleTree** | Efficient inclusion proofs |
| **DemoKeyManager** | Generates `DEMO_KEY_*` (NOT FOR PRODUCTION) |
| **ReleaseGate** | Fail-closed verification |

## Verification Checks

| Check | Detects |
|-------|---------|
| Hash chain integrity | Tampered events |
| Closing counts | Omitted events |
| Merkle inclusion proofs | Valid membership |
| Signature verification | Authentic receipts |
| Complete evidence | Missing signatures |

## Benchmark

| Trace Size | Verify Time (ms) |
|------------|------------------|
| 10 | 0.04 |
| 50 | 0.18 |
| 100 | 0.40 |
| 500 | 2.49 |

## Exercises

### Beginner
1. **Trace size benchmark** — Benchmark size vs verification time

### Standard
2. **Omission detection** — Detect specific omission patterns

### Extension
3. **Key rotation** — Implement key rotation in evidence chain
4. **Partial verification** — Verify subset of trace (checkpointing)

## Key Files

| File | Purpose |
|------|---------|
| `fixtures/trace.json` | Synthetic 6-step release trace |
| `student/eviassure.py` | Receipts, chains, Merkle, keys, gate |
| `student/benchmark.py` | Trace size vs time benchmark |
| `tests/test_eviassure.py` | 14 tests |

---

*Next: [Demo 06: ReconScope](../demos/06-reconscope.md)*