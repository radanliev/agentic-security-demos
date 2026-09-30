# Demo 43: Terms Coding

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain what platform-terms coding is (reading accountability out of terms of service)
- Code 8 synthetic platform terms against 3 clauses: disclaim 5/8, monitoring 4/8, consent 3/8
- Show the accountability gradient (disclaimers common, delegation consent rare)
- Distinguish this teaching toy from the pending ACM FAccT content analysis it illustrates

## Conceptual Explanation

Terms of service allocate responsibility between platform and deployer. Coding
8 hand-built platform records against 3 accountability clauses:

| Clause | Count |
|--------|-------|
| disclaims_autonomy | 5/8 |
| requires_monitoring | 4/8 |
| consent_for_delegation | 3/8 |

The lesson is the gradient: platforms disclaim autonomy more often than they
demand monitoring, and delegation consent is rarest — the accountability
burden slides downhill to the deployer.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real platforms, terms of service, or credentials
- No network access (standard library only)
- All platforms, clauses and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real terms

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 43 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=43` |

## Research Connection

This demo illustrates the design question of a content analysis of
agent-platform terms (targeting ACM FAccT 2027). That analysis is
**pending**; every quantity there is `[RESULT PENDING]`. Nothing here
describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-43-agent-platform-terms-accountability-facct` (private research repo).
It shares no topic with Demo 38 (assurance claims): this demo codes
accountability TERMS; Demo 38 codes assurance claims against obligations.
Different sources, methods, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Real platform terms corpus (pending) | 8 hand-built records |
| Method | Coded content analysis | Single fixed tally |
| Claims | Falsifiable accountability hypotheses | **No claims** — mechanism illustration only |
| Artefact | Coding protocol with reliability checks | One tiny tally function |
