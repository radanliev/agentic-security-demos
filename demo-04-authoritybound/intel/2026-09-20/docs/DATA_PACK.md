# DATA_PACK — `demo-4-prompt-injection-tool-authority-ieee-sp`

**Venue:** IEEE S&P 2027  
**Core claim:** Evaluation protocol for tool reference monitors: six diagnostics that explain when a reported ASR=0 is harness-decidable rather than defence-earned (AgentDojo + own harness).  
**Gap:** Already uses AgentDojo; can add Nemotron IPI + agentic PI boundary pairs for detector/monitor ablations without OpenRouter spend.  
**Generated:** 2026-09-20 10:30 CEST (Europe/Skopje)  
**British English; third person for paper-facing notes.**

## Rationale

External data/API use should strengthen falsifiability, related work, or cheap offline baselines — not replace the paper’s primary sealed empirics.

## Recommended datasets / APIs

### sungjuncho/agentdojo-trajectories

- **Why this demo:** Directly extends existing AgentDojo evaluation.
- **Suggested analysis (no live OpenRouter):** Apply six diagnostics to trajectory dump; quantify harness-decidable share.
- **Expected paper artefact:** Diagnostic table on public trajectories.

- **Pull (document only; run on Mac when ready):**
```bash
hf download sungjuncho/agentdojo-trajectories --repo-type dataset --local-dir artifacts/external_data/agentdojo-trajectories
```

### nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1

- **Why this demo:** IPI-in-tool-return is the monitor threat model.
- **Suggested analysis (no live OpenRouter):** Partition side-effecting tools; attribute blocks to rules offline where labels exist.
- **Expected paper artefact:** Monitor-diagnostic extension section.

- **Pull (document only; run on Mac when ready):**
```bash
hf download nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1 --repo-type dataset --local-dir artifacts/external_data/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1
```

### 3nesdeniz/agentic-prompt-injection-5k

- **Why this demo:** Paired benign/attack agentic PI for detector baselines beside monitors.
- **Suggested analysis (no live OpenRouter):** Train-free thresholding / simple TF–IDF baseline (as demo-11) — cheap CPU.
- **Expected paper artefact:** Detector vs monitor comparison table.

- **Pull (document only; run on Mac when ready):**
```bash
hf download 3nesdeniz/agentic-prompt-injection-5k --repo-type dataset --local-dir artifacts/external_data/agentic-prompt-injection-5k
```

### 3nesdeniz/agentic-prompt-injection-boundary-pairs

- **Why this demo:** Hard-negative boundary pairs (demo-11 already used sibling).
- **Suggested analysis (no live OpenRouter):** Same secondary detector protocol.
- **Expected paper artefact:** Cross-paper detector appendix (cite demo-11 methods).

- **Pull (document only; run on Mac when ready):**
```bash
hf download 3nesdeniz/agentic-prompt-injection-boundary-pairs --repo-type dataset --local-dir artifacts/external_data/agentic-prompt-injection-boundary-pairs
```

## Schema notes

Inspect with `hub_repo_details` / dataset preview before coding. Prefer parquet/JSONL slices <50MB for smoke tests.

## What NOT to claim

- Do not present exploratory external baselines as the paper’s confirmatory primary result.
- Do not claim API probes or Mac `.env` access from the box-scoped intel pass.

## Estimated effort

| Task | Size |
|------|------|
| Download + schema smoke | S–M |
| Offline analysis + table | M |
| Manuscript integration | S |

