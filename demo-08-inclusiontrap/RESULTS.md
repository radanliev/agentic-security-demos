# Real-data results (run 2026-10-26)

**Question:** Prevalence of path traversal (CWE-22) and PHP file inclusion (CWE-98) in NVD and KEV.

**Headline:** NVD tags 6,325 CVEs with CWE-22 and 44 with CWE-98. KEV holds 82 CWE-22 entries (27 known ransomware use) and 2 CWE-98 entries (both added in 2026).

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
