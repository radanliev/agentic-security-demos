# Demo 02: Supply-Chain and AIBOM Drift

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../docs/course/lab-02-supply-chain-aibom.md)

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
- One static fixture (`fixtures/aibom.json`); nothing is downloaded or generated
- The fixture pins `evaluation_time` (2025-01-14T12:00Z) so waiver validity is reproducible; `validate_aibom.py --now now` uses the real clock

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
## Research Connection

This demo distils a research problem into a runnable, course-neutral exercise. All scenarios, numbers and verdicts are synthetic; they describe no real publication or venue.

### Defect Family & Scenario Mapping

| Demo Scenario | Drift Type | Security Hazard | Drift? | Policy Gate Decision |
|---|---|---|---|---|
| `compliant-001` | Baseline Alignment | No drift — declared matches runtime | no | **ALLOW (PASS)** |
| `drifted-002` | Capability Escalation | Undeclared `scanner` tool added at runtime | yes | **BLOCK** (`exec:tools:scanner` explicitly denied) |
| `invalid-waiver-003` | Unapproved Scope Waiver | Unapproved `exec:shell:*` waiver for a scope that is not waivable | yes | **REJECT WAIVER (Block)** |
| `valid-waiver-004` | Approved Scoped Waiver | Approved, 24-hour waiver for `scanner` | yes | **ACCEPT WAIVER (Allow)** — drift is still reported |

### Core Primitives Demonstrated

1. **Declared vs. Observed Invariants**: the AIBOM's `agent_capabilities` is the declaration; every runtime capability outside it is reported as drift (`undeclared_capabilities`), independently of whether policy permits it. Composite tool lists (`exec:tools:parser,validator`) are matched per tool, so a runtime with *fewer* tools than declared is not drift.
2. **Fail-Closed Default Deny**: capabilities not explicitly permitted by the policy or by a valid waiver are blocked. Decision order: explicit allow → valid waiver → explicit deny → default deny. (A specific allow such as `net:http:api.internal/*` therefore beats the broad `net:http:*` deny because it is checked first, not because it is more specific.)
3. **Time-Bounded, Approved Waivers**: a waiver is honoured only if it is approved *and names an approver*, its scope is in `waiver_rules.allowed_scopes`, it is in force at evaluation time, and `expires − issued ≤ max_duration_hours`. Approval is a recorded field, not a cryptographic signature (signatures are Demo 05's topic). A waiver lifts a deny; it does not remove the drift from the report.

Not checked by this demo: the `components` list and its hashes (component-level verification is covered in Demo 05), and path normalisation of resource scopes (`read:files:/workspace/../etc/passwd` matches `read:files:/workspace/*` — see the Extension exercise).

## Difference from Private Research Benchmark

| Aspect | Reference research prototype | This demo |
|--------|------------------------------|-----------------------------|
| Enforcement | Kubernetes Admission Controller & eBPF | Standalone Python Policy Gate |
| Inventory | Full cyclonedx/SPDX AIBOM with model weights | Synthetic JSON component declaration |
| Waivers | Multi-signature hardware key approval | Structured waiver records with a recorded approver (no signature) |
| CI/CD | Real GitHub Actions / GitLab CI runner gates | Local validation script (`validate_aibom.py --scenario ID` / `--runtime observed.json`; exit 0 compliant, 1 non-compliant, 2 error) |
