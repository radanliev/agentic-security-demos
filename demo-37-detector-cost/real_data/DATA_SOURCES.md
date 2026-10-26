# Data sources (Demo 37, real public data)

| Dataset | URL | Licence | Revision (HF sha) | Retrieved | Rows |
|---|---|---|---|---|---|
| deepset/prompt-injections (train + test) | https://huggingface.co/datasets/deepset/prompt-injections | Apache-2.0 (dataset card) | 4f61ecb038e9c3fb77e21034b22511b523772cdd | 26 Oct 2026 | 546 + 116 = 662 |

Retrieved with `python3 fetch.py deepset/prompt-injections <split> deepset_<split>.jsonl` (Hugging Face datasets-server rows API). Labels are the dataset authors' own (1 = injection). The corpus mixes English and German prompts. Nothing here is synthetic; the original `fixtures/` remain the labelled synthetic teaching set.
