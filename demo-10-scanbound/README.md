# Demo 10: ScanBound — Vulnerability Assessment Scope Control

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-10-scanbound.md)

## Learning Objectives

- Constrain autonomous vulnerability assessment to approved scope
- Validate targets against host/port allowlists
- Parse scanner output with taint tracking
- Reject dangerous checks via AST/structured validation
- Enforce fail-closed downstream action policies

## Conceptual Explanation

An autonomous vulnerability scanner can:
- **Escape scope**: Scan unauthorized hosts/ports
- **Trust poisoned output**: Scanner XML/JSON contains injected commands
- **Execute unsafe checks**: Checks that modify state or exploit vulns

**ScanBound** teaches:
- Explicit target scope (allowlists only)
- DNS/address validation (localhost names only)
- Structured check validation (reject dangerous patterns)
- Taint tracking on scanner output
- Downstream action policy (no exploitation, no credential access)

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No public scanning** — localhost Docker lab or mock services only
- No exploit chains, credential attacks, or stealth techniques
- No bypassing security controls
- Clear separation from real penetration testing

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| Command | `make demo DEMO=10` |
