# Real-data results (run 2026-10-26)

**Question:** Real-world advisory landscape of prompt-injection CVEs (NVD) and their KEV overlap.

**Headline:** 211 NVD CVEs match "prompt injection" (127 published in 2026, 51 in 2025). None is in KEV. NVD tags zero CVEs with CWE-1427 (prompt injection); the most frequent CWEs are CWE-94 (37) and CWE-77 (29). 116 of 211 carry only CNA (secondary) CVSS scores.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
