# Demo 39: Incident Taxonomy

<p align="center">
  <img src="https://img.shields.io/badge/Teaching%20demo-Synthetic%20only-blue?style=flat-square" alt="Teaching demo">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Network-Offline%20only-success?style=flat-square" alt="Offline only">
</p>

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants.

## Learning Objectives

- Explain what a practitioner incident taxonomy is (patterns mapped to controls)
- Tally 10 synthetic incidents into 4 attack patterns with prompt-injection on top at 4/10
- Show a static 10-item control catalogue with 7/10 entries supported
- State a tie-break rule and defend why counts alone do not settle a tie
- Reproduce a reference run byte-identically and benchmark a perturbed run against it
- Distinguish this practitioner guidance toy from any research claim

## Conceptual Explanation

Practitioners turn incident reports into counts: which pattern recurs, and
which controls already cover it? On 10 hand-built incident sketches:

| Pattern | Count |
|---------|-------|
| prompt-injection | 4/10 (top) |
| tool-misuse | 3/10 |
| data-exfiltration | 2/10 |
| privilege-escalation | 1/10 |

The static control catalogue (input sanitisation, allowlists, provenance
labelling, human approval, egress filtering, memory gating, audit logging)
supports 7/10 entries; cross-agent attestation, hardware-backed identity and
formal verification are marked unsupported. The lesson is deliberately thin:
counts guide where to look first, nothing more.

### Why the tie-break matters

Move one sketch (`inc10` → `tool-misuse`, see INSTRUCTIONS Step 5) and the
top two patterns tie at 4/10 — yet the reported top stays
`prompt-injection`. The tally resolves ties deterministically
(alphabetically-first maximum), pinned by `test_tie_break_is_deterministic`.
A practitioner table that omits its tie-break rule reports a verdict its
counts do not determine.

### What makes the reference run a benchmark

`results/taxonomy.json` from the pristine fixture is the benchmark: every
later run is diffed against it (`diff` in INSTRUCTIONS Steps 6–7), and the
19-test suite pins each number it contains. Change one fixture row and the
suite names exactly which properties moved. That is the whole mechanism —
reference, perturb, compare — at toy scale.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real incidents, victims, or credentials
- No network access (standard library only)
- All incidents, patterns and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real incidents

See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 39 (fixed; no randomness used) |
| Commit | Git SHA or `local` |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=39` |
| Tests | `19 passed` (`python3 -m pytest tests/ -v`) |
| Reference | `results/taxonomy.json` (byte-identical across runs) |

## Research Connection

This demo distils a research problem into a runnable exercise. All scenarios, numbers and verdicts are synthetic; they describe no real incidents or venues.

Provenance: distilled from `demo-39-ai-incidents-practitioner-taxonomy-spmag` (private research repo), which targets ACM FAccT 2027 with an incident-grounded practitioner taxonomy: agentic-AI failure patterns coded from AI incident and vulnerability reports, mapped to MITRE ATLAS techniques and to OWASP control inventories, under the focus areas *evaluations and evaluation practices* and *experiences and interactions*.
It shares no topic with Demo 38 (assurance coding): this demo is practitioner
guidance from incident counts; Demo 38 codes public assurance claims.
Different sources, methods, and claims.

### Key Concepts from the Research

- **Inclusion rule**: which incidents count is decided before counting starts — the demo's fixture *is* its inclusion rule, frozen and pinned by tests
- **Double-coding and adjudication**: two coders, one codebook, disagreements resolved on the record — the demo's Step-5 experiment shows why recoding one row moves the table
- **Mapping with explicit gaps**: every incident maps to a technique or carries a `no-mapping` reason — the demo's vanished `privilege-escalation` row is the toy version of a coverage gap
- **Evidence behind controls**: a recommended control cites its incidents or is labelled `no-incident-evidence` — the demo's 7/10 verdict is the toy version of that table

## Difference from the Research Benchmark

| Aspect | Research study | This demo (benchmark) |
|--------|----------------|------------------------|
| Data | Practitioner incident corpus (frozen snapshot, coded rows) | 10 hand-built sketches |
| Method | Double-coded pattern extraction with ATLAS mapping and adjudication | Single fixed tally, deterministic tie-break |
| Reference | Frozen corpus + hashed registration; silent change is a breach | `results/taxonomy.json` reference copy; `diff` + 19 tests |
| Claims | Guidance with registered coverage rules, not effect sizes | **No claims** — mechanism illustration only |
| Artefact | Taxonomy + mapping + evidence tables for practitioners | Two tiny tally functions |
