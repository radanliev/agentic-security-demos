# Intel pack — demo-07 (2026-09-20)

**Source repo:** `demo-7-agentic-malware-triage-raid` @ `intel/ember-baseline` (`9af5f9d`)  
**Claim level:** exploratory external CPU baseline — **not** confirmatory paper empirics.

## SEPARATION
Malware PE-feature triage only. **No** demo-11 IPI / Nemotron / boundary-pairs / OpenRouter.
See `docs/SEPARATION.md`.

## Metrics (slim shard sample)
See `artifacts/metrics.json` and `docs/RESULTS_EMBER_BASELINE_2026-09-20.md`.
Best ROC-AUC ≈ 0.934 (HistGB); best acc ≈ 0.868 (XGBoost). Full Hub multi-GB shards **not** vendored here.
