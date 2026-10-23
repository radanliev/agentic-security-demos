# Demo 13: Typed Commitments

## Learning Objectives

- Explain what a derived coverage cue is (static-analysis pointer, triage ranking, or owners file telling an assessor where to look)
- Show how a shared wrong input makes two assessors fail together, so agreement stays high while both are wrong
- Implement a miniature agreement gate and read its pass/fail table sceptically (3/6 agreed, of which 1 wrong)
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Security pipelines hand LLM assessors a derived artefact telling them where to look, and nobody checks where that artefact came from. Two toy assessors (a cue-follower and a cue-ignoring heuristic) nominate one file each on six hand-built instances; an agreement gate passes instances where they agree:

| Cue level | Follower | Independent | Agreed |
|-----------|----------|-------------|--------|
| none (×2) | 2/2 | 2/2 | 2/2 |
| true (×2) | 2/2 | 0/2 | 0/2 |
| wrong (×2) | 0/2 | 1/2 | 1/2 |
| **total (×6)** | **4/6** | **3/6** | **3/6, of which 1 wrong** |

Instance `cue-wrong-02` is the lesson: both assessors nominate the same wrong file, so the gate passes a wrong answer 1/3 of the time it passes anything. Agreement measures shared input more than shared correctness.

Boundary: this toy demonstrates agreement-gate mechanics with two deterministic rules; it is not a measurement of real assessors and no claims are made about the preregistered study.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real repositories, credentials, or API keys
- No network access (standard library only)
- All instances, cues and verdicts are hand-built toys

## Run It

```bash
cd demo-13-typed-commitments
python3 -m pytest tests/ -v          # 6 tests, <1 min
python3 student/agreement_gate.py    # writes results/toy_eval.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-13-typed-commitments/INSTRUCTIONS.md).
