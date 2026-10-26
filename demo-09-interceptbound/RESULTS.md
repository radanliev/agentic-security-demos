# Real-data results (run 2026-10-26)

**Question:** Prevalence of improper certificate validation (CWE-295) in NVD and KEV.

**Headline:** NVD tags 1,093 CVEs with CWE-295; only 5 are in KEV and none is ransomware-linked. CWE-300 has zero NVD-tagged CVEs.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
