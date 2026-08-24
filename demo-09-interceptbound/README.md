# Demo 09: InterceptBound — Traffic Interception & Taint Tracking

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-09-interceptbound.md)

## Learning Objectives

- Model intercepted/relayed traffic with synthetic frames
- Implement provenance and taint labels on parsed data
- Distinguish observations from instructions in traffic
- Build ephemeral buffers with safe deletion
- Design downstream action guards

## Conceptual Explanation

An agent processing intercepted traffic (e.g., MITM position) sees forged responses. **Taint tracking** labels data by source: `trusted_local`, `user_supplied`, `intercepted_network`. Downstream actions (e.g., "send email", "update database") require untainted provenance.

This demo simulates:
- Synthetic traffic frames (HTTP, DNS, custom protocols)
- Parser that tags every field with provenance
- Ephemeral buffers that auto-clear
- Action guard that blocks tainted values from sensitive ops

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No ARP poisoning, MITM, or credential collection**
- No public interception or third-party traffic
- Fake credentials and local canaries only
- Fully simulated traffic stream

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| Command | `make demo DEMO=09` |
