# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Professional repository structure with issue templates, PR template, dependabot
- CODEOWNERS for automatic review assignment
- pyproject.toml with full project metadata (PEP 621)
- pre-commit configuration with ruff, mypy, safety checks
- Enhanced CI workflow with safety verification
- CITATION.cff for academic citation
- FUNDING.yml for sponsorship
- SUPPORT.md for user guidance
- GitHub Pages documentation site (mkdocs.yml)
- Comprehensive documentation (10 demo guides, reference, contributing, about)
- GitHub Pages deployment workflow
- Community health file (.github/COMMUNITY.md)

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