# Demo 07: TriageTrap — Safe Malware Triage (Synthetic Only)

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-07-triagetrap.md)

## Learning Objectives

- Track artifact provenance through triage pipeline
- Implement quarantine decisions without executing samples
- Calculate base-rate-aware triage scores
- Detect prompt-like payloads in metadata
- Compare baseline vs. provenance-aware triage agents

## Conceptual Explanation

Agentic malware triage processes artifacts (PCAPs, file metadata, sandbox reports) to make quarantine decisions. **Critical rule**: Never execute unknown code. This demo uses only:
- Synthetic PCAP-like records (JSON)
- Harmless metadata and canary strings
- Fake file hashes
- Simulated sandbox verdicts

**Provenance tracking** ensures every decision traces back to observed data, not injected instructions. **Base-rate awareness** prevents overreacting to rare events.

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No executable malware** — only inert synthetic data
- No instructions for creating or evading malware
- No real sandbox integration
- Quarantine = moving a JSON record, not a file

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| Command | `make demo DEMO=07` |
