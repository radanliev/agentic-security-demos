# Demo 01: Blind Verification

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-01-blind-verification.md)

## Learning Objectives

- Understand why post-hoc explanations are insufficient for agentic AI verification
- Implement a blind-commitment workflow where an agent commits to an action before seeing test conditions
- Design and use executable oracles (patch-level or output-level) for evaluation
- Identify false positives, false negatives, and leakage in verification systems
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

**Blind verification** addresses a fundamental problem in agentic AI evaluation: an agent that sees the test condition can tailor its behavior to pass, rather than demonstrating genuine capability. In a blind commitment workflow:

1. The agent receives a task description
2. The agent **commits** to an action (or produces an artifact) *without* seeing the hidden test oracle
3. The oracle evaluates the commitment against a hidden ground truth
4. The result reveals whether the agent's behavior generalizes

This mirrors **blind peer review** and **pre-registration** in science: you cannot claim success by optimizing for a known test.

### Why Post-Hoc Explanations Fail

An agent that explains "I would have done X" after seeing the test is not verifiable. The commitment must be **binding and prior** to test exposure.

### Oracle Types

- **Patch-level oracle**: Applies the agent's proposed patch to a codebase and runs tests
- **Output-level oracle**: Executes the agent's output and compares against expected behavior
- **Score oracle**: Computes a deterministic metric on the commitment

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real repositories, credentials, or API keys
- No network access
- All test conditions are local synthetic fixtures
- Results are demonstrations, not validated research claims

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 42 (default, configurable) |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=01` |

## Conference Paper Alignment (Paper 1: IEEE SaTML)

This demo is the educational companion to **Conference Paper 1** (`demo-1-blind-verification-agentic-ai`):
> **Blind Verification for Agentic AI: Making Security Assessment Falsifiable Before Reveal** (IEEE SaTML)

### Defect Family & Scenario Mapping

| Demo Scenario | Security Theme | Conference Paper Defect Variant | Failure Mode |
|---|---|---|---|
| `authz-001` | Broken authorization check | `v1-vulnerability` | Authz bypass & role drift |
| `depdrift-002` | Vulnerable dependency CVE | `v2-supply-chain-drift` | Unpinned dependency / AIBOM drift |
| `poisoned-003` | Poisoned config restore | `v3-poisoned-memory` | Unsigned / tampered memory / config |
| `restored-004` | Security control restoration | `v4-controls-applied` | Security control verified / restored |

### Why Baseline Scores 4/4 and Verified Scores 3/4

- **Baseline Agent (Cheating / Post-Hoc)**: Peeks at `fixtures/sealed_oracles.json` before committing. It scores **4/4 (100%)**, demonstrating that post-hoc or unblinded evaluations measure oracle leakage rather than real capability.
- **Verified Agent (Honest / Blind)**: Sees only `fixtures/scenarios.json` and commits *prior* to oracle reveal. It scores **3/4 (75%)** and honestly fails `restored-004` because blind commitment prevents guessing under underspecified conditions.

## Difference from Private Research Benchmark

| Aspect | Research Benchmark (Paper 1) | This Teaching Demo (Demo 01) |
|--------|------------------------------|-----------------------------|
| Data | Real repositories, PRs, issues | Synthetic support tickets + repo operations |
| Scale | Multi-agent finite-run study (N=80) | 4 core synthetic scenarios |
| Oracle | Diff-level patch oracle + executable invariants | Deterministic patch/output checks |
| Claims | Formal statistical power & hypothesis testing | **No performance claims** — educational only |
| Leakage control | Cryptographic SHA-256 seal prior to reveal | File-based sealing & honesty boundary |
