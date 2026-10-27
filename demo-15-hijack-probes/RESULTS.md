# Real-data results (run 2026-10-26)

**Question:** Fixed-threshold (0.55) text probe in-distribution vs cross-dataset (black-box proxy, not white-box).

**Headline:** A fixed 0.55 threshold catches 131/139 jailbreaks with 0 false positives in-distribution (F1 0.970) but only 4/60 injections cross-dataset (F1 0.125).

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
