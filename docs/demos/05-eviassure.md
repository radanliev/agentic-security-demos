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

**The lesson**: the hash chain alone proves only that a trace is *self-consistent*. A forger who edits a step and rebuilds the chain consistently passes every chain check — sub-demo 2 prints `Tampered trace: PASS` on purpose. Tampering is detected only where the gate holds something the forger cannot edit: the receipts signed by the release key, which the gate compares field by field with the chain it rebuilds from the trace (sub-demo 7).

## Safety Notice

⚠️ **Teaching demonstration only.**
- Demo Ed25519 keys generated in memory at runtime (`DEMO_KEY_*`), never written to disk
- **Not production signing keys** — do not use for real releases
- No persisted private keys, certificates, or real PKI
- Synthetic traces only

## Running the Demo

```bash
make demo DEMO=05
```

### Expected Output

Nine sub-demonstrations (verbatim, minus the banner lines):

```
1. Verifying complete trace (chain check)...
   Complete trace: PASS  Reason: ok

2. Tampering with step 3 (tests passed 95 -> 99), chain check only...
   Tampered trace: PASS  Reason: ok
   (expected: the forged chain is self-consistent, so the chain check alone CANNOT catch it)

3. Omitting step 4 (security_scan) and fixing the count to 5...
   Omitted trace: FAIL  Reason: step_count_mismatch: 5 != 6

4. Forging the closing count (999)...
   Bad closing count: FAIL  Reason: closing_count_mismatch

5. Merkle inclusion proof for step 3...
   Merkle proof for step 3: VALID  (3 sibling hashes for 6 leaves)
   Same proof, one hex digit of the leaf changed: INVALID

6. Signing every receipt with DEMO_KEY_RELEASE_001 and verifying the package...
   Signed evidence: PASS  Reason: ok

7. Tampered trace from step 2 presented with the ORIGINAL signed receipts...
   Tampered evidence: FAIL  Reason: receipt_mismatch_step_3_data_hash
   (the signatures are genuine, but they cover the receipts of the ORIGINAL step 3)

8. Evidence package with no signed receipts...
   Incomplete evidence: FAIL  Reason: no_signed_receipts

9. Tampered trace re-signed by an attacker's own key (DEMO_KEY_ATTACKER)...
   Attacker-signed evidence: FAIL  Reason: unauthorized_signer_DEMO_KEY_ATTACKER
```

`make demo` then runs the benchmark, which prints its JSON (also written to `results/benchmark.json`).

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
| Hash chain integrity | Inconsistent edits (a receipt that no longer links to its predecessor) — not a forgery rebuilt consistently |
| Step count held by the verifier, step numbering, closing counts | Omitted events (`step_count_mismatch`, `step_numbering_mismatch`, `closing_count_mismatch`) |
| Merkle inclusion proofs | Valid membership against a root the verifier already trusts (the gate returns the root; it does not check its own leaves against it) |
| Authorized signer + signature verification | Receipts signed by a key the gate trusts (`unauthorized_signer_*`, `signature_verification_failed_*`) |
| Signed receipt vs rebuilt receipt, field by field | Tampered events (`receipt_mismatch_step_3_data_hash`) |
| Complete evidence | Missing signatures (`no_signed_receipts`, `signed_receipt_count_mismatch`) |

## Benchmark

`chain_build_ms` is the chain rebuild; `verify_time_ms` is building the Merkle tree and verifying an inclusion proof for every leaf. Minimum of 5 runs on one machine — times vary by machine, `proof_length` does not. `result` is `pass` only if every proof verified.

| Trace Size | Chain Build (ms) | Verify Time (ms) | Proof Length |
|------------|------------------|------------------|--------------|
| 10 | 0.08 | 0.08 | 4 |
| 50 | 0.41 | 0.52 | 6 |
| 100 | 0.84 | 1.15 | 7 |
| 500 | 4.27 | 7.32 | 9 |

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
| `tests/test_eviassure.py` | 34 tests |

---

*Next: [Demo 06: ReconScope](../demos/06-reconscope.md)*