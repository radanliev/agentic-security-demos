# RESULTS — EMBER CPU triage baseline (2026-09-20)

**Generated:** 2026-09-20 10:28 CEST (Europe/Skopje)  
**Claim level:** exploratory external CPU baseline — **not** confirmatory primary paper empirics.  
**SEPARATION:** malware PE-feature triage only; no demo-11 IPI / Nemotron / boundary-pairs; no OpenRouter.  
**Hub:** `cw1521/ember2018-malware` (EMBER 2018 feature mirror; Elastic/Anderson & Roth lineage).  
**Run ID:** `ember-baseline-slim-2026-09-20`  
**Metrics file:** `artifacts/ember_baseline/metrics.json`

## Data pull and size limits

Full Hub layout is ~400 train + ~100 test JSONL shards (~65–72 MB each → **multi-tens-of-GB**). This run used a **documented slim sample**:

| File | Size | Role |
|------|------|------|
| `ember2018_train_50.jsonl` | 68.3 MB | Train (mixed 0/1; skip −1) |
| `ember2018_train_100.jsonl` | 68.9 MB | Train (mixed 0/1; skip −1) |
| `ember2018_test_1.jsonl` | 67.9 MB | Test |
| `ember2018_train_1.jsonl` | 65.5 MB | On disk only — early-year **all-benign**; **not used in fit** |

- **External data tree:** ~271 MB (`artifacts/external_data/ember2018-malware`) + 2.8 MB families catalog.  
- **Feature dim:** 2381.  
- **Train kept:** 2971 (1615 malware / 1356 benign); skipped 1029 unlabeled (−1).  
- **Test kept:** 2000 (998 / 1002).  
- Unlabeled policy: drop `label`/`y` ∈ {−1}.

Optional: `Jordan123234/malware-families-catalog` → 2903 families, 2.8 MB parquet (taxonomy only; not used in the binary classifier).

## Models (CPU)

| Model | Accuracy | F1 | ROC-AUC | AP | Fit (s) |
|-------|----------|----|---------|----|---------|
| Logistic regression | 0.778 | 0.773 | 0.833 | 0.832 | 3.6 |
| Random forest (200 trees) | 0.846 | 0.841 | 0.911 | 0.899 | 0.8 |
| HistGradientBoosting | 0.847 | 0.842 | **0.934** | 0.929 | 7.5 |
| XGBoost (`hist`, CPU) | **0.868** | **0.865** | 0.933 | 0.929 | 7.1 |

**Best by ROC-AUC:** `hist_gradient_boosting` (AUC 0.934).  
**Best by accuracy/F1:** `xgboost` (0.868 / 0.865).  
**Total wall time:** ~21.6 s (load + four fits) on box CPU.

## Reproduce

```bash
# from repo root (venv with scikit-learn, xgboost, pandas, pyarrow, huggingface_hub)
python scripts/run_ember_baseline.py
```

Pull commands (slim; do **not** `hf download` the whole repo without disk planning):

```bash
hf download cw1521/ember2018-malware data/ember2018_train_50.jsonl \
  --repo-type dataset --local-dir artifacts/external_data/ember2018-malware
hf download cw1521/ember2018-malware data/ember2018_train_100.jsonl \
  --repo-type dataset --local-dir artifacts/external_data/ember2018-malware
hf download cw1521/ember2018-malware data/ember2018_test_1.jsonl \
  --repo-type dataset --local-dir artifacts/external_data/ember2018-malware
hf download Jordan123234/malware-families-catalog malware_families.parquet \
  --repo-type dataset --local-dir artifacts/external_data/malware-families-catalog
```

## What not to claim

- Not a full EMBER 2018 replication (millions of rows / official train–test protocol).  
- Not agent/LLM triage performance.  
- Not demo-11 reporting or IPI results.

## Sync / Mac status

Synced 2026-09-20 ~10:37 CEST to Luke-Skywalker:
`/Users/skywalker/Projects/demo-7-agentic-malware-triage-raid`
(metrics.json, RESULTS, SEPARATION, `scripts/run_ember_baseline.py`; slim Hub shards re-pulled via `hf download`).
Branch target: `intel/ember-baseline`. Claim level remains **exploratory**.
