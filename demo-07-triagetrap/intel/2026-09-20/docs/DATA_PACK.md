# DATA_PACK — `demo-7-agentic-malware-triage`

**Venue:** RAID (SEPARATION: malware triage ≠ demo-11 reporting)  
**Core claim:** Agentic malware triage: LLM/agent pipelines for family/label triage under analyst-assist constraints.  
**Gap:** SEPARATION from demo-11 mandatory. Needs feature-level malware corpora (EMBER-class), not IPI reporting datasets.  
**Generated:** 2026-09-20 10:30 CEST (Europe/Skopje)  
**British English; third person for paper-facing notes.**

## Rationale

External data/API use should strengthen falsifiability, related work, or cheap offline baselines — not replace the paper’s primary sealed empirics.

## Recommended datasets / APIs

### cw1521/ember2018-malware

- **Why this demo:** EMBER-class PE features — standard malware triage baseline, SEPARATE from demo-11 IPI.
- **Suggested analysis (no live OpenRouter):** Classic gradient-boosted triage replication; compare agent triage rationales offline to feature attributions.
- **Expected paper artefact:** Baseline triage AUC table (CPU).

- **Pull (document only; run on Mac when ready):**
```bash
hf download cw1521/ember2018-malware --repo-type dataset --local-dir artifacts/external_data/ember2018-malware
```

### cw1521/ember2018-malware

- **Why this demo:** Smaller triage-feature mirror if full EMBER too heavy.
- **Suggested analysis (no live OpenRouter):** Same as above on slim features.
- **Expected paper artefact:** Slim-baseline appendix.

- **Pull (document only; run on Mac when ready):**
```bash
hf download cw1521/ember2018-malware --repo-type dataset --local-dir artifacts/external_data/ember-malware-triage-features
```

### Jordan123234/malware-families-catalog

- **Why this demo:** Family taxonomy for agent label normalisation.
- **Suggested analysis (no live OpenRouter):** Map agent outputs to catalog labels; confusion matrix.
- **Expected paper artefact:** Family-normalisation table.

- **Pull (document only; run on Mac when ready):**
```bash
hf download Jordan123234/malware-families-catalog --repo-type dataset --local-dir artifacts/external_data/malware-families-catalog
```

## Schema notes

Inspect with `hub_repo_details` / dataset preview before coding. Prefer parquet/JSONL slices <50MB for smoke tests.

## What NOT to claim

- Do not present exploratory external baselines as the paper’s confirmatory primary result.
- Do not claim API probes or Mac `.env` access from the box-scoped intel pass.

- **SEPARATION:** do not import demo-11 IPI/reporting datasets into this malware-triage paper.

## Estimated effort

| Task | Size |
|------|------|
| Download + schema smoke | S–M |
| Offline analysis + table | M |
| Manuscript integration | S |

