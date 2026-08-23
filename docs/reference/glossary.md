# Glossary

## A

**AIBOM** — AI Bill of Materials. A declared inventory of components, models, tools, and permissions an agentic system uses.

**Agentic AI** — AI systems that can autonomously take actions, use tools, and make decisions without human-in-the-loop for each step.

**AST (Abstract Syntax Tree)** — Tree representation of source code structure, used for static analysis.

**Authority Confinement** — Restricting an agent's ability to exercise privileges based on provenance and scope.

## B

**Base Rate** — The prior probability of a condition (e.g., 2% of artifacts are malicious). Critical for avoiding base-rate fallacy.

**Blind Commitment** — An agent produces a fix or action *before* seeing the test oracle or expected output.

**Blind Verification** — Evaluation methodology where agents commit to actions before seeing test conditions.

## C

**Capability Token** — A scoped authorization granting permission to use specific tools or resources (e.g., `read:files:/workspace/*`).

**Confused Deputy** — A privileged component tricked into misusing its authority by untrusted input.

**CVE** — Common Vulnerabilities and Exposures identifier.

## D

**Drift** — When a running system's actual capabilities exceed or deviate from its declared AIBOM.

## E

**Ephemeral Buffer** — Temporary storage with TTL and secure deletion for sensitive intercepted data.

**Evaluation Invariant** — An executable check that validates the evaluation methodology itself (not just the score).

**Evidence-Backed Release** — Release decisions supported by cryptographically verifiable evidence chains.

## F

**Fail-Closed** — Default deny; access requires explicit allowance. Opposite of fail-open.

**False Negative** — A correct commitment/action that fails verification due to strict matching.

**False Positive** — An incorrect commitment/action that passes verification due to weak oracle.

## G

**GitHub Actions** — CI/CD platform used for automated testing and validation.

## H

**Hash Chain** — Sequential hashing where each element includes hash of previous (genesis → H1 → H2 → ...).

## I

**Inclusion Trap** — File inclusion vulnerability where agent treats included content as instructions.

**Indirect Prompt Injection** — Malicious instructions embedded in retrieved content (documents, tool outputs).

**InterceptBound** — Traffic interception with taint tracking and action guards.

## L

**LFI/RFI** — Local/Remote File Inclusion vulnerabilities.

**Leakage** — Test information contaminating training data or agent inputs before commitment.

## M

**Merkle Tree** — Binary hash tree enabling efficient inclusion proofs for large datasets.

**MITM** — Man-in-the-Middle; interception of communications between two parties.

## N

**n-gram** — Contiguous sequence of n items (characters/words) used for similarity detection.

## O

**Oracle** — Hidden test condition or expected output used to evaluate agent commitments.

**Out-of-Scope** — Targets, actions, or capabilities not in declared allowlists.

## P

**PCAP** — Packet Capture format for network traffic metadata.

**Policy Gate** — Automated check that enforces declared policy (fail-closed).

**Poisoned Output** — Scanner/tool output containing injected malicious content.

**Provenance** — The origin/source of data (e.g., `trusted_instruction`, `user_data`, `network_response`).

**Prompt Injection** — Malicious input designed to override agent instructions.

## Q

**Quarantine** — Isolation decision for suspicious artifacts (in demos: moving JSON record, not executing files).

## R

**ReconScope** — Network reconnaissance with provenance tracking and scope enforcement.

**Reproducibility** — Same seed, code, environment → identical results.

## S

**ScanBound** — Vulnerability assessment scope control with taint tracking.

**Scope Enforcement** — Restricting actions to declared allowlists (hosts, ports, paths, capabilities).

**Seed** — Fixed random seed for deterministic execution (default: 42).

## T

**Taint Tracking** — Labeling data by source trust level (LOW/MEDIUM/HIGH) and propagating through pipeline.

**TriageTrap** — Safe malware triage with provenance tracking and base-rate awareness.

## V

**Vulnerability Assessment** — Automated scanning for security weaknesses.

## W

**Waiver** — Time-limited, approved exception to policy (requires approval, has expiration).

**Witness Receipt** — Cryptographically signed attestation of a pipeline step, linked in hash chain.