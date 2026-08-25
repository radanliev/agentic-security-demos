# Demo 02: Supply-Chain and AIBOM Drift

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-02-supply-chain-aibom.md)

## Learning Objectives

- Understand AI Bill of Materials (AIBOM) and component inventory concepts
- Detect when agent permissions drift from declared capabilities
- Implement fail-closed policy gates
- Design waiver mechanisms with expiration and justification
- Create GitHub Actions-compatible validation scripts

## Conceptual Explanation

An **AIBOM (AI Bill of Materials)** declares what components, models, tools, and permissions an agentic system uses. **Drift** occurs when the running system exceeds or deviates from this declaration — e.g., an agent gains access to a new tool, a dependency is updated without review, or a privilege is escalated.

This demo teaches:
1. **Declared inventory**: What the system claims to use
2. **Runtime observation**: What the system actually uses
3. **Policy gate**: Automated check that blocks drift
4. **Waiver process**: Controlled, time-limited exceptions

## Safety Notice

⚠️ **Teaching demonstration only.**
- Synthetic package names (e.g., `secure-parser-123`)
- No real dependencies, registries, or credentials
- Local validation only — no cluster required
- All fixtures generated at setup

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
## Conference Paper Alignment (Paper 2: IEEE S&P Workshop / Supply Chain)

This demo is the educational companion to **Conference Paper 2** (`demo-2-agentic-supply-chain-aibom-drift`):
> **Agentic Supply Chain Assurance: Continuous AIBOM Verification & Runtime Capability Drift Detection**

### Defect Family & Scenario Mapping

| Demo Scenario | Drift Type | Security Hazard | Policy Gate Decision |
|---|---|---|---|
| `compliant-001` | Baseline Alignment | No drift — declared matches runtime | **ALLOW (PASS)** |
| `drifted-002` | Capability Escalation | Undeclared `scanner` tool added at runtime | **BLOCK (Drift Detected)** |
| `invalid-waiver-003` | Unapproved Scope Waiver | Unsigned / unapproved `exec:shell:*` waiver | **REJECT WAIVER (Block)** |
| `valid-waiver-004` | Approved Scoped Waiver | Approved, time-bounded waiver for `scanner` | **ACCEPT WAIVER (Allow)** |

### Core Primitives Demonstrated

1. **Declared vs. Observed Invariants**: A system's AI Bill of Materials (AIBOM) acts as an immutable contract; runtime capability introspection flags any drift.
2. **Fail-Closed Default Deny**: Capabilities not explicitly permitted in declared policy or approved waivers are blocked automatically.
3. **Cryptographic / Time-Bounded Waivers**: Emergency access requires explicit scope bounds, valid cryptographic/approval status, and unexpired ISO-8601 timestamps.

## Difference from Private Research Benchmark

| Aspect | Research Framework (Paper 2) | This Teaching Demo (Demo 02) |
|--------|------------------------------|-----------------------------|
| Enforcement | Kubernetes Admission Controller & eBPF | Standalone Python Policy Gate |
| Inventory | Full cyclonedx/SPDX AIBOM with model weights | Synthetic JSON component declaration |
| Waivers | Multi-signature hardware key approval | Structured in-memory waiver records |
| CI/CD | Real GitHub Actions / GitLab CI runner gates | Local validation script (`validate_aibom.py`) |
