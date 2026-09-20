# External data subset notes

**Pulled:** 2026-09-20 (Europe/Skopje)

## sungjuncho/agentdojo-trajectories

- **Full hub layout:** two pipelines (`gemma-4-E4B-it`, `qwen3.5-9B`) × four suites (`banking`, `slack`, `travel`, `workspace`).
- **Subset retained here:** `**/banking/**` for both pipelines only (allow_patterns on `hf download` / `snapshot_download`).
- **Rationale:** banking is the suite used in the demo-4 AgentDojo decidability / denominator discussion; full tree is large (many leaf JSON trajectories). Documented subset keeps smoke analysis on-box without claiming full-hub coverage.
- **Local path:** `artifacts/external_data/agentdojo-trajectories/`

## nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1

- **Subset:** full `train.jsonl` (1,272 rows; ~11.7 MB). No further sampling required.
- **Local path:** `artifacts/external_data/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1/`

## Auth

- Downloads used unauthenticated Hub access on the executor box (public datasets). Mac `.env` / `hf auth` was not reachable from this surface.
