# Demo 58: Work Exposure

## Learning Objectives

- Score synthetic occupational tasks for AI exposure (0–1)
- Aggregate task scores into occupation and task-family means
- Define the agentic-action share: exposure attributable to agentic actions
- Explain why task-level measurement beats occupation-level labels
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A synthetic task inventory for three higher-education roles.

| Level | Means |
|-------|-------|
| Occupations | tutor 0.50 · designer 0.65 · advisor 0.30 |
| Task families | learning-design 0.65 · teaching 0.50 · student-support 0.30 |
| Agentic-action share | 0.50 |

Half of all measured exposure flows through actions an agent could take
autonomously — the number policy actually needs. Occupation-level labels
would have hidden which tasks drive each mean.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real occupations, workers, or labour-market data
- No network access (standard library only)
- All tasks and scores are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real work

## Run It

```bash
cd demo-58-work-ai-exposure
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_exposure.py      # writes results/exposure.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-58-work-ai-exposure/INSTRUCTIONS.md).
