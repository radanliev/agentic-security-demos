# Real-data results (run 2026-10-26)

**Question:** CVEs whose descriptions mention vulnerability scanners: scanner output and scanners themselves as attack surface.

**Headline:** 154 NVD CVEs mention "vulnerability scanner"; 45 published in 2026. None is in KEV (see results).

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
