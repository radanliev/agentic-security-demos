# Data sources (Demo 42, real public data)

| Source | URL | Licence | Retrieved | Notes |
|---|---|---|---|---|
| OSV vulnerability database, `/v1/query` per PyPI package | https://osv.dev, https://api.osv.dev/v1/query | CC-BY 4.0 (OSV data); individual records carry upstream terms (GHSA: CC-BY 4.0; PYSEC: CC-BY 4.0) | 26 Oct 2026 | 12 packages: langchain, langchain-core, langchain-community, llama-index, llama-index-core, transformers, vllm, gradio, mlflow, litellm, ray, torch |
| PyPI JSON API release upload times | https://pypi.org/pypi/{pkg}/json | PyPI metadata, public | 26 Oct 2026 | used for the fixed-release upload date |

Re-run: `python3 analyse.py && python3 dedupe.py`. Live feeds change daily, so exact counts will drift.
