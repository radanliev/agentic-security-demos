# Real-data results (run 2026-10-26)

**Question:** Share and vendors of network-edge products among actively exploited vulnerabilities (KEV).

**Headline:** 114 of 1,756 KEV entries (6.5%) match a network-edge keyword heuristic; Cisco (27), Citrix (12) and D-Link (12) lead.

Full output: `results/real_data_results.json`. Reproduce: `bash data/fetch_data.sh && python3 analysis/analyse.py` (needs pandas, pyarrow, scikit-learn for demos 14/15). Sources and licences: `data/DATA_SOURCES.md`.

**Scope note:** these are measurements on real public data that support or contextualise the paper's claims. They are not results of the paper's own experiments and must not be reported as such. The demo's `fixtures/` remain synthetic teaching fixtures.
