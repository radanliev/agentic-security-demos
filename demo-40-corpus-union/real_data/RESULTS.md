# Results: Demo 40 pipeline on four public prompt corpora

Command: `./fetch_all.sh && python3 analyse.py`. Output: `results.json`.

| Stage | Count |
|---|---|
| Ingested records (4 sources) | 3,047 |
| Within-source exact duplicates (after lowercase/strip) | 19 (jackhhao 17, lakera 1, rubend18 1) |
| Unique after SHA-256 dedupe | 2,992 |
| Digests shared across sources | 36, all jackhhao + rubend18 |
| Releasable (permissive) | 2,950 |
| Blocked (unlicensed) | 42 |

Reading. The one cross-source overlap is the interesting finding: 36 of the 78 distinct prompts in the unlicensed rubend18 collection also occur verbatim (after normalisation) in the Apache-2.0 jackhhao corpus. Under the demo's first-seen rule those 36 are released under jackhhao's licence, which a data descriptor should flag as licence provenance that cannot be confirmed from card metadata alone. Exact-hash dedupe misses near duplicates; a near-duplicate pass (for example MinHash) is not yet run.
