# Results: Demo 37 rule detectors on deepset/prompt-injections

Command: `python3 analyse.py` (stdlib only). Output: `results.json`.

| Detector | TP | FP | FN | TN | Recall | FPR | Cost (FP=10, FN=25) |
|---|---|---|---|---|---|---|---|
| strict (`ignor` substring) | 27 | 0 | 236 | 399 | 0.103 | 0.000 | 5,900 |
| lenient (exact "ignore previous instructions") | 0 | 0 | 263 | 399 | 0.000 | 0.000 | 6,575 |

n = 662 prompts, 263 labelled injections.

Reading. On real prompts the synthetic lesson inverts its mechanism: neither rule false-alarms, and the cost gap comes entirely from missed injections. The exact phrase never occurs in this corpus, and the substring rule catches about one injection in ten, partly because many injections are in German or paraphrased. The strict rule is cheaper at every cost ratio swept (FN/FP from 0.25 to 10). These figures describe two toy rules on one public corpus; they say nothing about learned or commercial detectors, which the FAccT paper would need to evaluate separately.
