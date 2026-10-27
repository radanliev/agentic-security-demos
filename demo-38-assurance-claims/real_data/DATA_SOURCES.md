# Data sources (Demo 38, real public data)

| Source | URL | Licence | Retrieved | Size |
|---|---|---|---|---|
| Hugging Face Hub model list, `pipeline_tag=text-generation`, sorted by downloads (top 80 queried) | https://huggingface.co/api/models | Hub API; each card carries its own model licence | 26 Oct 2026 | 60 cards kept |
| Each model's `README.md` (model card) | https://huggingface.co/{model}/raw/main/README.md | per-model licence, see card | 26 Oct 2026 | 60 |

Cards shorter than 500 characters or not retrievable (for example gated repositories) were skipped. The model list is a snapshot by download rank on the retrieval date and will drift. Only derived boolean flags (`cards_coded.json`) are committed, not card text. Re-run with `python3 fetch_and_code.py`.
