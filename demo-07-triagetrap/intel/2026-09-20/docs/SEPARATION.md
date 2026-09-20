# SEPARATION — demo-7 vs demo-11

**Reinforced:** 2026-09-20 10:28 CEST (Europe/Skopje)  
**Repo (Mac target):** `/Users/skywalker/Projects/demo-7-agentic-malware-triage-raid`  
**machineId (Mac):** `d32ab1e5-844e-4be9-bbe6-8278028917b7`

## Hard boundary

| This demo (demo-7 RAID malware triage) | Must NOT enter this repo |
|----------------------------------------|---------------------------|
| EMBER-class PE features (`cw1521/ember2018-malware`) | demo-11 IPI / reporting corpora |
| Optional family taxonomy (`Jordan123234/malware-families-catalog`) | `nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1` |
| CPU sklearn / XGBoost triage baselines | `3nesdeniz/agentic-prompt-injection-boundary-pairs` |
| Analyst-assist malware family / label triage | OpenRouter confirmatory LLM loops |

## Why

Demo-7 claims agentic **malware triage**. Demo-11 claims **degenerate reporting** under IPI defence evaluation. Mixing IPI/reporting datasets into demo-7 would collapse venue SEPARATION and invite double-counting of empirics.

## Checklist for every data pull

- [ ] Hub ID is malware-feature or family-taxonomy (not IPI/reporting).
- [ ] No OpenRouter / confirmatory R1 spend attributed to this baseline.
- [ ] Results labelled **exploratory external** unless sealed as primary paper empirics.
- [ ] Citations stay on EMBER / Elastic lineage + HF mirror DOI when used.

## EMBER baseline note (2026-09-20)

See `RESULTS_EMBER_BASELINE_2026-09-20.md` and `artifacts/ember_baseline/metrics.json`. Slim shard sample only; full Hub dump is multi-tens-of-GB.
