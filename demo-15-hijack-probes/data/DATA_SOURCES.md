# Data sources (retrieved 2026-10-26)

All data below is real public data. Nothing here is simulated. The existing fixtures/ remain synthetic teaching fixtures and are labelled as such in the demo README.

| Source | URL | Licence | Local file |
|---|---|---|---|
| jackhhao/jailbreak-classification | https://huggingface.co/datasets/jackhhao/jailbreak-classification | Apache-2.0 | raw/jb_train.parquet, raw/jb_test.parquet |
| deepset/prompt-injections | https://huggingface.co/datasets/deepset/prompt-injections | Apache-2.0 | raw/pi_train.parquet, raw/pi_test.parquet |

Re-fetch with `bash data/fetch_data.sh`. NVD queries are rate-limited (unauthenticated, 6 s spacing). Snapshots may differ from a later re-fetch as the feeds are live.
