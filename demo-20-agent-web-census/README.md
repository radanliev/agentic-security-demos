# Demo 20: Agent Web Census

> **New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain agent-facing web measurement (which sites publish agent directives, which carry injections)
- Tally adoption (either directive flag) and exposure (injection text) over 10 synthetic sites
- Show adoption 4/10 and injections 2/10, both injections on low-popularity sites
- Distinguish this teaching toy from the preregistered WWW study it illustrates (no data collected there yet)

## Conceptual Explanation

Sites increasingly ship agent directives alongside human pages. A census asks two
independent questions: who publishes directives, and whose copy carries
injection text.

This toy uses 10 hand-built sites:

| Site | Popularity | Adopted | Exposed |
|------|------------|---------|---------|
| s01 | high | yes | no |
| s02 | high | yes | no |
| s03 | medium | yes | no |
| s04 | low | yes | yes |
| s05 | low | no | yes |
| s06-s10 | mixed | no | no |

Adoption: 4/10. Exposure: 2/10, both on low-popularity sites.

## Safety Notice

WARNING: **This is a teaching demonstration using synthetic fixtures only.**
- No real crawl data, sites, models, or credentials
- No network access (standard library only)
- All sites, directives and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about the real web

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 20 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `python3 student/run_web.py` |

## Research Connection

This demo illustrates the design question of a preregistered study on the
agent-facing web (targeting WWW 2027, Common Crawl corpus). That study has
**collected no confirmatory data**; every quantity there is `[RESULT PENDING]`.
Nothing here describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-20-agent-facing-web-commoncrawl-www` (private research repo).
Boundary: this demo is web measurement over page directives; it is not an MCP
registry census (Demo 21). Different corpus, data, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Common Crawl agent-facing sample (pending) | 10 hand-built sites |
| Method | Large-scale directive and injection census | Two boolean tallies |
| Claims | Falsifiable prevalence hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Census measurement pipeline | Two tiny helper functions |
