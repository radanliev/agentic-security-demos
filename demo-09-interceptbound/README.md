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

## Conference Paper Alignment (Paper 9: ESORICS)

This demo is the educational companion to **Conference Paper 9** (`demo-9-agentic-mitm-esorics`):
> **InterceptBound: Taint-Tracked Ephemeral Buffers for Man-in-the-Middle Network Interception in Autonomous Defense Agents** (ESORICS)

### Traffic Ingestion & Taint Propagation

| Frame ID | Protocol & Endpoints | Payload Content | Taint Level | Action Guard Decision |
|---|---|---|---|---|
| `frame_001` | HTTP (`192.168.1.10` $\rightarrow$ `192.168.1.100`) | Sensitive Session Token | `HIGH` | **BLOCKED**: `store_token` rejected (taint level too high) |
| `frame_002` | HTTP (`192.168.1.10` $\rightarrow$ `192.168.1.100`) | Injected prompt in HTTP body | `HIGH` | **BLOCKED**: `process_injection` & `store_token` blocked |
| `frame_003` | DNS (`192.168.1.1` $\rightarrow$ `192.168.1.100`) | Injected command in DNS answer | `HIGH` | **BLOCKED**: Injected DNS record discarded |
| `frame_005` | Custom TCP (`192.168.1.30` $\rightarrow$ `192.168.1.100`) | System shutdown request | `HIGH` | **BLOCKED**: `execute_shutdown` prohibited |

### Core Security Invariants

1. **Strict Taint Propagation**: All parsed attributes from intercepted network packets inherit `Provenance.INTERCEPTED_NETWORK` and `TaintLevel.HIGH`.
2. **Ephemeral Secure Buffers**: Intercepted payloads are stored in memory-only volatile buffers with zeroization on deletion to prevent leakage across tasks.
3. **Privileged Action Confinement**: Sensitive operations (e.g. `store_credential`, `system_shutdown`) refuse execution when supplied with high-taint arguments.

## Difference from Private Research Benchmark

| Aspect | Research Benchmark (Paper 9) | This Teaching Demo (Demo 09) |
|--------|------------------------------|-----------------------------|
| Network Harness | DPDK high-speed packet capture & TLS proxy | Synthetic in-memory JSON traffic frame list |
| Memory Management | Linux memfd with secure zeroization | Python `EphemeralBuffer` with dictionary deletion |
| Scale | Multi-gigabit live traffic streams | 6 representative network frames |
