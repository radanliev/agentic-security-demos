# DATA_PACK — `demo-11-degenerate-reporting-raid`

**Venue:** RAID 2027  
**Core claim:** Degenerate reporting in IPI defence evaluation: ASR alone is attained by do-nothing policies; evaluations must report the complementary half.  
**Gap:** R1 confirmatory adaptive loop paused (OpenRouter free tier exhausted). Boundary detector + P3 exploratory pilots already done — paper can advance WITHOUT confirmatory R1.  
**Generated:** 2026-09-20 10:30 CEST (Europe/Skopje)  
**British English; third person for paper-facing notes.**

## Rationale

External data/API use should strengthen falsifiability, related work, or cheap offline baselines — not replace the paper’s primary sealed empirics.

## Recommended datasets / APIs

### 3nesdeniz/agentic-prompt-injection-boundary-pairs

- **Why this demo:** Already used for secondary detector (TPR 0.95 @ FPR≈0) — cite and freeze.
- **Suggested analysis (no live OpenRouter):** No new runs required; ship metrics JSON + sticky exploratory labels.
- **Expected paper artefact:** Detector appendix (done).

- **Pull (document only; run on Mac when ready):**
```bash
hf download 3nesdeniz/agentic-prompt-injection-boundary-pairs --repo-type dataset --local-dir artifacts/external_data/agentic-prompt-injection-boundary-pairs
```

### EleutherAI/sycophancy

- **Why this demo:** Degenerate “looks helpful / reports success” behaviour analogue for reporting thesis.
- **Suggested analysis (no live OpenRouter):** Qualitative related-work: sycophancy as cousin of ASR-only reporting.
- **Expected paper artefact:** Related-work subsection.

- **Pull (document only; run on Mac when ready):**
```bash
hf download EleutherAI/sycophancy --repo-type dataset --local-dir artifacts/external_data/sycophancy
```

### allenai/reward-bench

- **Why this demo:** Reward/eval gaming parallel to do-nothing ASR perfection.
- **Suggested analysis (no live OpenRouter):** Map “chat hard” / adversarial preference slices to degenerate metrics argument.
- **Expected paper artefact:** Reporting-standard analogy table.

- **Pull (document only; run on Mac when ready):**
```bash
hf download allenai/reward-bench --repo-type dataset --local-dir artifacts/external_data/reward-bench
```

### nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1

- **Why this demo:** IPI tool-trace corpus for offline reporting-metric recomputation.
- **Suggested analysis (no live OpenRouter):** Recompute ASR vs task-progress on frozen traces — no OpenRouter.
- **Expected paper artefact:** Frozen-trace metric dual-reporting figure.

- **Pull (document only; run on Mac when ready):**
```bash
hf download nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1 --repo-type dataset --local-dir artifacts/external_data/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1
```

## Schema notes

Inspect with `hub_repo_details` / dataset preview before coding. Prefer parquet/JSONL slices <50MB for smoke tests.

## What NOT to claim

- Do not present exploratory external baselines as the paper’s confirmatory primary result.
- Do not claim API probes or Mac `.env` access from the box-scoped intel pass.

- Do not claim confirmatory R1; see `DEMO11_QUALITY_WITHOUT_R1.md`.

## Estimated effort

| Task | Size |
|------|------|
| Download + schema smoke | S–M |
| Offline analysis + table | M |
| Manuscript integration | S |

## Related offline quality receipts (2026-09-20)

- `docs/round16/QUALITY_WITHOUT_R1_RECEIPT.md` — manuscript quality path while confirmatory R1 is parked
- `docs/round16/DUAL_METRIC_FROZEN_TRACE_NOTE.md` — use existing P3 benign×hijack dual metric; no OpenRouter
