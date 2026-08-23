# Demo 01: Blind Verification

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

## Difference from Private Research Benchmark

| Aspect | Private Research | This Teaching Demo |
|--------|------------------|-------------------|
| Data | Real repositories, PRs, issues | Synthetic support tickets + repo operations |
| Scale | Thousands of tasks | 10-20 synthetic scenarios |
| Oracle | Complex multi-model evaluation | Deterministic patch/output checks |
| Claims | Performance metrics, statistical significance | **No performance claims** — teaching only |
| Leakage control | Cryptographic commitments | Simple file-based sealing |

The private benchmark uses cryptographic commitments, larger task corpora, and statistical analysis. This demo teaches the *concept* with minimal, inspectable code.