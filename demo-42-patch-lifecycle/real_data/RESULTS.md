# Results: fix-to-advisory lag on the Python LLM stack

Commands: `python3 analyse.py && python3 dedupe.py`. Outputs: `advisories.json`, `results.json`.

The headline figures are for alias-deduplicated advisories, where GHSA and PYSEC records for the same issue are counted once:

| Statistic | Value |
|---|---|
| Advisories (12 packages) | 421 |
| With a fixed version and both dates | 341 |
| No fixed version recorded | 72 |
| Median lag, advisory published minus first fixed release upload | 17 days |
| Advisory published before the fix shipped | 56 |
| Advisory 0–7 days after fix | 78 |
| Advisory more than 90 days after fix | 54 |

Raw OSV records before deduplication: 767, median lag 30 days. Duplicated aliases inflate the lag, because PYSEC records are often published later.

Reading. This measures the upstream half of the lifecycle: how long a shipped fix goes without a public advisory. It does not measure the downstream adoption lag modelled in the synthetic fixture (37.5 days). That still needs dependency-graph data, for example deps.dev or GitHub dependents, which has not been collected. The 72 advisories with no fixed version are open exposures worth a separate table. "Published" is the OSV record date, which can trail the GHSA publication.
