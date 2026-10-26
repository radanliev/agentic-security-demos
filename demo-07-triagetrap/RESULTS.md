# Real-data results (run 2026-10-26)

**Question:** Real base rates for triage: ransomware-linked share of KEV, yearly additions and CWE mix.

**Headline:** 361 of 1,756 KEV entries (20.6%) are flagged as known ransomware use; the top CWEs are CWE-20 (119), CWE-78 (113) and CWE-787 (105).

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
