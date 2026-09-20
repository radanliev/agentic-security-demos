# External data

Hugging Face pulls for demo-4 offline diagnostics.

- `agentdojo-trajectories/` — **banking subset** of `sungjuncho/agentdojo-trajectories` (both pipelines). See `SUBSET_NOTES.md`.
- `Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1/` — full `train.jsonl` from `nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1`.

Do not commit secrets. Prefer gitignoring large raw pulls if the Mac repo policy requires it; commit derived tables under `docs/data_opportunities/`.

Regenerate summaries: `python scripts/external_data/summarise_offline.py --root .`
