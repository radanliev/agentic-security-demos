# Demo 05: Evidence-Backed Release Assurance (EVIAssure)

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-05-eviassure.md)

## Learning Objectives

- Build cryptographically verifiable evidence pipelines
- Implement sequence-bound witness receipts
- Create hash chains and Merkle trees for integrity
- Verify inclusion proofs
- Design fail-closed release gates
- Detect tampering and omission

## Conceptual Explanation

**Evidence-backed release assurance** uses cryptographic evidence to support release decisions. Instead of trusting "it passed tests," you verify a tamper-evident chain of evidence:

1. **Witness receipts**: Signed attestations of each step
2. **Hash chaining**: Each receipt includes hash of previous (sequence-bound)
3. **Merkle tree**: Efficient inclusion proofs for large evidence sets
4. **Release gate**: Verifies complete, unmodified evidence before release

This demo implements a minimal pipeline with synthetic agent traces.

## Safety Notice

⚠️ **Teaching demonstration only.**
- Demo keys generated at runtime (labeled `DEMO_KEY_*`)
- **Not production signing keys** — do not use for real releases
- No private keys, certificates, or real PKI
- Synthetic traces only

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ (requires `cryptography`) |
| Command | `make demo DEMO=05` |

## Conference Paper Alignment (Paper 5: USENIX Security)

This demo is the educational companion to **Conference Paper 5** (`demo-5-evidence-release-assurance-usenix`):
> **EVIAssure: Cryptographic Evidence Assurance for Autonomous Multi-Agent Systems Under Malicious Release Gates** (USENIX Security)

### Threat Model & Verification Guarantees

| Attack Vector | Attacker Capability | EVIAssure Defense Primitive | Verification Result |
|---|---|---|---|
| **Event Modification** | Attacker tampers with intermediate test/scan score | SHA-256 Witness Hash Chain & Signatures | **FAIL**: Mismatched leaf hash and invalid Ed25519 signature |
| **Event Omission** | Attacker drops security scan step to bypass check | Sequence-bound Previous Hashes & Closing Counts | **FAIL**: Step count mismatch ($5 \neq 6$) |
| **Closing Count Spoofing** | Attacker fabricates final summary counter | Final Hash Continuity & Signed Receipt Chain | **FAIL**: `closing_count_mismatch` |
| **Selective Inclusion** | Attacker claims step executed without presenting full trace | Merkle Tree Audit Path ($O(\log N)$ Inclusion Proof) | **VALID / INVALID**: Mathematical root equivalence |

### Core Primitives Demonstrated

1. **WitnessReceipt**: Structured attestations bound by step index, action, data payload hash, previous hash, and ISO-8601 timestamp.
2. **Sequential Hash Chain**: Formally prevents reordering, insertion, and truncation of execution steps.
3. **Merkle Inclusion Trees**: Generates compact logarithmic inclusion proofs for selective verification.
4. **Release Gate**: Recomputes hash chains, checks cryptographic signatures against trusted release keys, and verifies closing counts before authorizing artifact deployment.

## Difference from Private Research Benchmark

| Aspect | Research Framework (Paper 5) | This Teaching Demo (Demo 05) |
|--------|------------------------------|-----------------------------|
| Cryptography | Production Hardware HSM & KMS signing | Ephemeral Ed25519 in-memory demo keys |
| Scale | Continuous pipeline traces ($N=10^5$ events) | 6-step synthetic deployment trace |
| Ledger | Distributed append-only transparency log (Rekor/Sigstore) | Local JSON receipt records |
