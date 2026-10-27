# Real-data results (run 2026-10-26)

**Question:** Degenerate baselines (always-allow, always-block, majority, random, keyword) on a real public benchmark test split.

**Headline:** On the deepset test split (116 items, 60 positive), always-block scores F1 0.682 while always-allow scores accuracy 0.483; every degenerate baseline has balanced accuracy at or near 0.5. Accuracy and F1 alone therefore flatter a do-nothing or block-everything defence.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
