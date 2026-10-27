# Real-data results (run 2026-10-26)

**Question:** Injection-class CVEs in calendar software (NVD).

**Headline:** Of 239 NVD hits for "calendar injection", the calendar-filtered subset is dominated by SQL injection (CWE-89) in calendar web applications; this is a weak proxy for agentic calendar injection and is reported as such.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
