# Real-data results (run 2026-10-26)

**Question:** Split-conformal action gate calibrated on one public benchmark and tested under shift to another.

**Headline:** With alpha 0.30 calibrated on 61 malicious calibration items, the gate meets its budget on the same-distribution test (risk 0.300, benign blocked 0.0). Under shift to the jailbreak set it executes only 0.7% of malicious items but blocks 90.2% of benign ones: the guarantee is kept only by losing utility.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
