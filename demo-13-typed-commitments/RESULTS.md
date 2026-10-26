# Real-data results (run 2026-10-26)

**Question:** Agreement between two real assessors (NVD analyst vs CNA) on CVSS v3.1 severity for prompt-injection CVEs.

**Headline:** For 33 prompt-injection CVEs with both NVD and CNA CVSS v3.1 scores, the two assessors agree on severity in 36.4% of cases; Cohen's kappa is 0.036 (near-chance agreement).

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
