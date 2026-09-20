# Dual-metric note — frozen artefacts / offline (no OpenRouter)

**Time:** 2026-09-20 ~10:35 CEST (Europe/Skopje)  
**Constraint:** no confirmatory R1; no new OpenRouter calls; no API secrets  
**Status:** planning + S21 dual-metric already in hand; Nemotron roll-out **not** executed on this box pass

---

## A. Already dual-metric (S21 P3 pilots) — use this first

The exploratory budget pilots already report the paper’s complementary pair on a frozen N=24 slice:

| Arm | Benign accuracy (utility / task success) | Hijack rate on malicious (ASR-class) |
|-----|------------------------------------------|--------------------------------------|
| A — raw baseline | 1.00 (12/12) | 50% |
| F — mediated envelope | 1.00 (12/12) | 25% |

**Thesis miniature:** ASR-alone ranking is incomplete; joint reporting separates A from F while benign utility ties.  
**Label:** `EXPLORATORY_BUDGET_PILOT_NOT_CONFIRMATORY_R1` — not Blind-B1 / not confirmatory R1.  
**Sources:** `artifacts/s21_adaptive/p3_pilot_comparison.json` (inbox mirror validated 2026-09-20).

No new model calls required to land this in the manuscript.

---

## B. Boundary detector — complementary benign-cost metric

Secondary §8.1 detector already reports TPR **and** realised FPR / confusion (benign cost = 0/120 FP at operating points).  
Ease disclaimer: nearly linearly separable bag-of-words upper bound — **not** AgentDojo closed-loop difficulty.  
**Source:** `artifacts/s21_boundary_detector/metrics.json`.

---

## C. Nemotron IPI corpus — offline dual-reporting plan (CPU / Mac later)

**Hub:** `nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1`  
**Inspected via HF MCP** (`@Radanliev`), 2026-09-20: config `default` / split `train` ≈ 1.3K rows, ~9.8 MB parquet.

**Schema relevant to dual metrics:**

- User task in `responses_create_params.input` (benign request)
- Injection goal / target tool in `injection.*`
- `verifier_config.type = trace_analysis` (expects agent traces — **not** pre-scored ASR+utility columns)
- Domains include healthcare tool-use; attack categories e.g. `unauthorized_action`, `exfiltration`

**What this pass did *not* do:** download parquet to Mac `artifacts/`, run a local policy, or invent ASR/utility numbers.

**Recommended Mac-only offline procedure (no OpenRouter):**

1. `hf download nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1 --repo-type dataset --local-dir artifacts/external_data/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1`
2. Prefer replaying **existing** sealed AgentDojo / S21 trial dumps for dual metrics before any new LLM spend.
3. If scoring Nemotron: define jointly (a) injection success / ASR vs (b) benign task completion on the user request; report both; label exploratory unless sealed prereg covers it.
4. Do-nothing / refuse-all baselines: expected high “attack fail” with collapsed utility — the reporting punchline.

---

## D. Related-work cousins (literature only; zero API)

- `EleutherAI/sycophancy` — “looks helpful” analogue  
- `allenai/reward-bench` — metric-gaming analogue  

No pulls required for a short related-work sentence.

---

## E. Non-claims

- No confirmatory R1  
- No Groq/Cerebras calls on this pass (Mac keys unreachable)  
- No claim that Nemotron was dual-scored in this cycle  
- SEPARATION: no demo-7 malware / EMBER tables in this manuscript
