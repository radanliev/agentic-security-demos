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
| Command | `make demo DEMO=02` |

## Difference from Private Research

The private project uses real staged bundles, production AIBOMs, and cluster admission controllers. This demo uses local JSON fixtures and a standalone policy evaluator.
