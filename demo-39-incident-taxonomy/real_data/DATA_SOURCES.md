# Data sources (Demo 39, real public data)

| Source | URL | Licence | Revision | Retrieved | Size |
|---|---|---|---|---|---|
| AVID, AI Vulnerability Database (`reports/`, excluding `reports/review/`) | https://github.com/avidml/avid-db | MIT | commit 8eda5f4e6f74a3738eb980b795c4f813c6e52ca8 | 26 Oct 2026 | 1,745 report JSON files |

Not vendored. Recreate with `git clone https://github.com/avidml/avid-db /tmp/avid && git -C /tmp/avid checkout 8eda5f4e` and then `python3 analyse.py /tmp/avid`.
