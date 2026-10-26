# Real-data results (run 2026-10-26)

**Question:** Train/test leakage and duplicate audit of two public prompt-injection/jailbreak benchmarks.

**Headline:** In deepset/prompt-injections no test item appears in train (exact or normalised). In jackhhao/jailbreak-classification 4 test prompts appear verbatim in train and 13 after normalisation; train has 11 internal exact duplicates.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
