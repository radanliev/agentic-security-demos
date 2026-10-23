# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed (compact status marks, 23 October 2026)
- Root `README` demos table: Status column is now plain text — a colour dot plus the venue abbreviation (replaces the small badge images; normal-size, readable, no dates shown there).
- Root `README` venues table: option cells show the venue abbreviation (→ conference page) and a dates-only line underneath (→ submission portal); status wording, check marks, notes and undated markers removed. Colour-dot meanings are intentionally undocumented.

### Changed (venues table restructure, 23 October 2026)
- Root `README` venues section: one 4-column table (Demo | Option A | Option B | Option C) replacing the 7-column table. Deadline columns merged into each option cell: venue abbreviation links to the conference page, deadline line underneath links to the submission portal (abstract + full-paper dates kept; `TBD` marks unpublished CFPs).
- Years removed from venue names (WWW'27 → WWW etc.). Next-edition backups that became exact duplicates after year removal collapsed to "—" (option B/C of demos 03, 06, 08, 11, 12, 13, 14, 16, 17, 20, 23, 24, 25, 32, 34, 35, 40, 41, 42).
- Colour indicators switched from shields pills to emoji state dots (GitHub strips `<font>`; pills were image-heavy). The four slate bullets and the old legend were dropped.
- Venue links verified (HTTP 200; issre.org and queue.acm.org block curl but resolve in browsers). EuroS&P backups link eurosp2027.ieee-security.org (SIGSAC TC page 404s). New verified links added for dormant backups: AAMAS (ifaamas.org), SaTML (satml.org), DMLR (data.mlr.press), TNNLS, TIP, EMNLP (ACL Anthology), ICSE, FSE (esec-fse.org).

### Added (WWW-set docs coverage, 16 October 2026)
- `docs/demos/` pages for the eight WWW'27 demos (18, 19, 20, 21, 27, 28, 36, 43) plus `mkdocs.yml` nav entries; each page verified against its demo (5 tests, runner command, results file). `docs/index.md` quick-start range corrected from 01–12 to 01–47.
- Verified for the WWW set: 40/40 tests pass, all 8 runners execute cleanly with byte-identical committed results, INSTRUCTIONS expected outputs match, CITATION.cff files valid, no venue names in demo code/fixtures/tests (only historical private-repo names in README provenance lines).

### Changed (venue refresh: Computers & Security removal + CoSe de-duplication, 16 October 2026)
- Root `README`: removed Computers & Security / CoSe from all venue tables (header list, FAccT slate, demos 37/38/46 rows, acknowledgments). The journal's guide for authors confirms an AI/ML moratorium since early 2024, so all agentic-AI demos are out of scope there (0% chance).
- Demo 37 (Detector Cost): Plan B CoSe → IEEE TIFS (♾️ rolling; scope covers intrusion detection, adversarial ML and AI-driven decision-system security), Plan C stays TDSC. Sequential only: FAccT'27 → TIFS → TDSC.
- Demo 38 (Assurance Claims): Plan B stays Journal of Cybersecurity (matches `demo-38-system-card-assurance-claims-joc` provenance; Oxford journal explicitly publishes AI-cybersecurity work), Plan C CoSe → ACM Journal on Responsible Computing (♾️ rolling; scope lists fairness/accountability/transparency plus adversarial ML). Sequential only.
- Demo 46: Plan A AsiaCCS'27 Round 2 (11 Dec 2026, AI Security track), Plan B USENIX SAIS'27 (4 Feb 2027), Plan C IEEE TDSC (♾️ rolling). Replaces Computers & Security due to the journal's AI/ML moratorium and satisfies the soon-deadline requirement without hitting author submission caps.
- FAccT slate header corrected from 4 to 5 papers (demos 31, 37, 38, 39 plus 45); no author cap, slate counts unchanged, so no cap risk.
- Demo 04: removed Plan B / Plan C overlap (both listed CCS'27) — Plan B USENIX Sec'28, Plan C CCS'27 Cycle B.
- Refreshed dates verified 16 Oct 2026: WWW'27 abstract 18 Oct / paper 25 Oct 2026; FAccT'27 abstract 27 Oct / paper 3 Nov 2026; S&P'27 C2 abstract 10 Nov / paper 17 Nov 2026; AsiaCCS'27 R2 11 Dec 2026 (AI Security track; R1 rejects cannot resubmit R2); DSN'27 abstract 25 Nov / paper 2 Dec 2026; PoPETs'27 Iss. 3 30 Nov 2026; USENIX'27 C2 reg. 19 Jan / papers 26 Jan 2027; CSF'27 Winter 28 Jan 2027 (Fall cycle 15 Oct 2026 has passed); ACNS'27 C2 21 Jan 2027; SAIS'27 4 Feb 2027; CCS'27 CFP TBD (expected Cycle A ~mid-Jan, Cycle B ~late Apr 2027). Prioritisation rule applied: Plan A = soonest fitting conference with capacity, backups ordered by soonest-actionable date then estimated success rate (FAccT ~33% '26, S&P ~13–15%, USENIX/CCS ~15–18%, rolling journals).

### Changed (demo 01 venue plan, 15 October 2026)
- Root `README`, demo 01: Plan A Expert Systems with Applications (Elsevier, JCR Q1), Plan B ACM TOSEM (JCR Q1), Plan C Information Processing & Management (Elsevier, JCR Q1); one venue at a time. Demo 47's row no longer refers to demo 01.
- Root `README`, demo 47: Plan B Engineering Applications of AI (Elsevier, JCR Q1) and Plan C Information Sciences (Elsevier, JCR Q1), replacing a journal that no longer considers AI/ML submissions and a JCR Q2 journal.

### Added (demo 46 teaching toy, 15 October 2026)
- **demo-46-embedding-drift**: stdlib cosine-shift toy linked to the private research repo. Overview row moved from skeleton to active. Research repo remains a simulated study.

### Added (demo 47, 15 October 2026)
- **demo-47-blind-seal**: teaching companion for pre-reveal seals. Three synthetic cases (hit, miss, post-seal edit). Standard library only.
- Root `README`: catalogue count 47, overview row, quick-start command, venue row (Plan A USENIX SAIS'27, 4 Feb 2027; Plan B Computers & Security; Plan C JISA, each only after the previous decision).
- Root `Makefile`: `demo-47-blind-seal` in `DEMO_DIRS` and a `demo-47` target.

### Changed (venue notes and anonymity, 13 October 2026)
- Root `README`, demo catalogue: the Venue column is removed, so no row pairs a demo title with a venue. Demo 13's row is renamed to its own title, "Typed Commitments & Coverage Cues".
- Root `README`, venue slates: rows now name demos by number only ("Demo 18"); the topic columns (WWW titles, USENIX angle, FAccT angle, S&P focus) are removed.
- Root `README`, demo 01: venue plan revised (superseded by the 15 October 2026 entry).
- Root `README`, venue notes: the S&P'27 cap (six papers per author per cycle, all registrations desk-rejected above it, enforced 10 Nov 2026) and the WWW'27 cap (seven per author per type) are recorded with links to the official calls; the FAccT'27 load is noted as five papers including demo 45.
- 33 demo READMEs (demos 13-45): target-venue names removed from Learning Objectives and Research Connection text. The studies, data status and boundaries are unchanged.

### Changed (venue notes, 8 October 2026)
- Root `README`, demo 02 (Supply Chain AIBOM Drift): Plan A re-targeted to Empirical Software Engineering (EMSE, Springer; rolling), Plan B IEEE TSE (only after an EMSE decision), Plan C MSR'27 (only after a TSE decision). Previously TOSEM / CCS'27 / EMSE. Backups remain sequential, never simultaneous.

### Changed (venue notes, 3 October 2026)
- Root `README`: venue notes for several teaching demos were revised.
- `demo-26`, `demo-29`, `demo-30` and `demo-33` READMEs: Research Connection wording updated.

### Added (12-demo expansion, September 2026)
- **demo-12-provenancebound**: teaching companion to Conference Paper 12 (`demo-12-provenance-authz-calendar-sacmat`, SACMAT 2027). Provenance-aware authorization for untrusted calendar content: derived provenance (structure-only, fail-closed), lexical detector with Unicode canonicalization, naive verb+endpoint agent (inert, oracle-refusing), provenance-aware deny policy (high-risk untrusted always blocked, even on detector miss `cal_008`). 8 synthetic invites, 44 tests, standard structure (`README`/`INSTRUCTIONS`/`Makefile`/`fixtures`/`results`/`solutions`/`student`/`tests`).
- **demo-11-degenerate-reporting**: aligned to demos 01–10 pattern (removed stray nested `demo-11-degenerate-reporting/` subfolder, added Course Lab Guide link, Tests row in reproducibility metadata, `solutions/` in Step 0 listing, Exercises summary table, Alternative one-command run, Troubleshooting, Safety Reminder).
- Root integration for 12 demos: `README` (12 rows, venues, install extras), root `Makefile` (`DEMO_DIRS` + `demo-11`/`demo-12` targets), `mkdocs.yml` nav, `docs/demos/12-provenancebound.md`, `docs/demos/overview.md`, `docs/course/lab-12-provenancebound.md`, `docs/course/COURSE_GUIDE.md`, `docs/index.md`, `pyproject.toml` keywords, `CITATION.cff`, CI (demo-11/12 jobs + 01–12 reproducibility loop).
- Final assessment Part B practical renamed to `demo-13-memorybound/` (demo-12 slot now taken by ProvenanceBound); submission checklist updated to 12 modules.

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