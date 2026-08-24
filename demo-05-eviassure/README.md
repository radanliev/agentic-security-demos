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
