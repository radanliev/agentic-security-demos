# Demo 25: Attestation Verifier

## Learning Objectives

- Explain install-time attestation verification: install a package only when its provenance is attested
- Contrast fail-closed (block 6/10 unattested) with fail-open (warn instead of blocking)
- State clearly that the 4-attested / 6-unattested split is a hand-picked toy, not an ecosystem measurement
- Distinguish this teaching toy from the pending study it illustrates (no data collected there yet)

## Conceptual Explanation

Supply-chain defences check a package's attestation before install. Under fail-closed, every unattested package is blocked; under fail-open, the same packages install with a warning.

This toy uses 10 hand-built packages (4 attested, 6 not):

| Policy | Blocked | Warned | Allowed |
|--------|---------|--------|---------|
| Fail-closed | 6/10 | 0/10 | 4/10 |
| Fail-open | 0/10 | 6/10 | 10/10 |

Note: real probes have seen wide attestation gaps, but THESE numbers are toys — they illustrate verifier behaviour, not the ecosystem.

Boundary: this demo is verifier behaviour at install time under two policies; it is not an attestation-coverage measurement of real registries. Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real packages, registries, attestations, or installs
- No network access (standard library only)
- All packages and verdicts are hand-built toys

## Run It

```bash
cd demo-25-attestation-verifier
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_verify.py        # writes results/attest.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-25-attestation-verifier/INSTRUCTIONS.md).
