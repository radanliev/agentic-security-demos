# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (PII de-identification, August 2026)
- `shared/anonymize.py`: an offline, deterministic de-identification helper the demos can read in a couple of minutes — `pseudonymize`/`Anonymizer` (stable, locally reversible identifier tags that preserve joins), `redact_secrets` (deny-by-default masking of tokens/passwords/keys), `deidentify` (both, with a report of what changed), and `redact_record` (allowlist field redaction). 9 new tests.
- **demo-09 InterceptBound**: an observation log. The guarded agent may observe intercepted traffic, but every note it writes is de-identified first — identities become stable pseudonyms, secrets are redacted — while the baseline records it in the clear. Fixtures gained a synthetic contact e-mail; 5 new tests (39 → 44).
- **demo-08 InclusionTrap**: content the guarded agent is allowed to keep (a config with a secret, an in-scope user list) is de-identified before it is logged — usernames/e-mails pseudonymised (ids preserved, so records still join), secrets redacted — while the vulnerable agent leaks the raw `/etc/passwd` and user list. New `safe_002` read scenario, enriched synthetic `/etc/passwd` and `users.json`; 4 new tests (26 → 30).
- **demo-07 TriageTrap**: an allowlist redaction on the shared triage record — only analytic fields (hashes, verdict, score) travel in the clear; submitter, owner, file name and addresses are masked (deny-by-default), mirroring the RAID triage proxy's VirusTotal allowlist. The score and verdict are unchanged (de-identification is about the shared record). Fixtures gained synthetic submitter/owner PII; 4 new tests (26 → 30).
- All new PII is synthetic; `make verify-safety` still passes and no demo touches the network. Test suite 294 → 316.

### Fixed (course audit, August 2026)
- Every demo now *implements* the mechanism its slides and guides describe, instead of asserting it:
  - demo-01: answer keys removed from `scenarios.json`; commitments are hash-published and a post-hoc edit is reported as `commitment_hash_mismatch`; the baseline cheats only through the oracle file; oracle errors are reported, not silently failed.
  - demo-02: `validate_aibom.py --scenario/--runtime` exits 0/1/2 by compliance (drift really fails the gate); waivers require a named approver, a waivable scope and an issued/expires window within `max_duration_hours`; drift is computed (runtime ∖ declared) and reported separately from compliance; tool lists are expanded per tool.
  - demo-03: leakage is a computed 3-gram overlap against a training corpus; stability, failure-classification and reproducibility checks can fail; ceiling effect is a share of scores at ceiling; the headline-vs-clean comparison is computed (baseline 0.88 → 0.85, verified 0.81 → 0.84).
  - demo-04: baseline / provenance-aware / scope-bound are three genuinely different configurations of one mediator; scope is checked on the tool's named argument; the parser extracts real targets; `safe_send_005` shows a legitimate action flowing; the matrix generator compares all 21 decisions.
  - demo-05: the release gate requires one signed receipt per step from an authorised signer and compares it field-by-field with the chain rebuilt from the trace (`receipt_mismatch_*`, `unauthorized_signer_*`, `no_signed_receipts`, `step_numbering_mismatch`); the self-referential Merkle check was removed from the gate; `sign_receipt()` helper; benchmark measures real timings.
  - demo-06: the parser assigns `network_response` provenance itself; one decision rule decides who acts; scope is explained and re-checked on targets named by executed instructions; DNS/TLS fixtures are in scope so the documented narrative is what runs.
  - demo-07: the score is the Bayesian posterior from the sandbox's own rates (`sandbox_false_positive` added); free text can hold a record for review but never moves the score or releases it; `verdict` is evidence only with sandbox provenance; the baseline believes notes.
  - demo-08: scope is decided on the canonical path before any read; blocked results never carry content; a simulated `Host` records every capability call, so "reading ≠ executing" is a checked property; `lfi_004` (in-scope injection) added; URL includes have their own allowlist.
  - demo-09: the shutdown command is on the wire (the fixture annotation is never read); named content detectors; per-action taint ceilings; the provenance rule blocks laundered labels; a bounded, zeroing ephemeral buffer; uniform scope results; destinations checked; `frame_007`/`frame_008` added.
  - demo-10: checks are validated before execution (blocked checks never run); the AST screen parses every payload; every failing screen is reported; the action policy is consulted for every finding (MEDIUM reported, HIGH held); taint comes from the finding text; `check_006` (out of scope) and `check_007` (credential) added.
- Result records are computed (git commit, environment, pass/fail with exit 1 on mismatch) instead of hard-coded `"result": "pass"`.
- `shared`: `format_command` produces a runnable `make demo DEMO=NN`; one `capture_environment`; `enforce_offline()` installs a socket guard and `verify_offline()` reports whether it is active (it previously returned `True` unconditionally).
- `make verify-safety` and CI also scan runtime modules (`demo-*/student/`, `shared/`) for network imports; the CI credential scan no longer matches its own workflow file; `make demo` failures now fail the CI reproducibility job (`pipefail`).
- Test suites rewritten so that each mechanism has a failing-input test (154 → 294 tests); every lab guide and demo page re-run against the code, expected outputs replaced with real output, `cd ../..` → `cd ..`, test counts corrected.

### Added
- Professional repository structure with issue templates, PR template, dependabot
- CODEOWNERS for automatic review assignment
- pyproject.toml with full project metadata
- pre-commit configuration with ruff, mypy, safety checks
- Enhanced CI workflow with safety verification
- CITATION.cff for academic citation
- FUNDING.yml for sponsorship
- SUPPORT.md for user guidance

### Changed
- Updated README with badges, keywords, comprehensive documentation
- Improved CONTRIBUTING.md with detailed guidelines
- Enhanced SECURITY.md with vulnerability reporting
- Updated CODE_OF_CONDUCT.md

### Security
- All demos verified for zero network access
- Credential scanning in CI
- External URL detection in tests

## [0.1.0] - 2024-08-23

### Added
- Initial release with 10 teaching demos:
  - demo-01-blind-verification: Blind commitment & oracle evaluation
  - demo-02-supply-chain-aibom: AIBOM drift detection & policy gates
  - demo-03-eval-invariants: Evaluation invariants (5 checks)
  - demo-04-authoritybound: Authority confinement & confused deputy
  - demo-05-eviassure: Cryptographic evidence pipelines
  - demo-06-reconscope: Network recon with provenance tracking
  - demo-07-triagetrap: Safe malware triage (synthetic only)
  - demo-08-inclusiontrap: File inclusion & scope boundaries
  - demo-09-interceptbound: Traffic interception & taint tracking
  - demo-10-scanbound: Vulnerability assessment scope control

- Root Makefile with unified commands
- Shared utilities (result schema, reproducibility, fixtures)
- GitHub Actions CI (offline tests only)
- Safety verification (no network, no credentials, no malware)
- Standardized JSON result schema across all demos
- Deterministic tests with seed=42
- Beginner/standard/extension exercises per demo

### Safety
- Zero network access in all tests
- No real credentials, API keys, or private data
- Synthetic fixtures only
- Standardized result schema with reproducibility metadata

---

## Version History Format

Each release follows:
```
## [X.Y.Z] - YYYY-MM-DD

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
```