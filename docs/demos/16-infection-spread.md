# Demo 16: Infection Spread

## Learning Objectives

- Explain epidemic spread over agent graphs (R0 as p times mean degree)
- Simulate deterministic breadth-first spread from node 0 on four six-node topologies
- Show uncontained spread reaches 6/6 everywhere while chain containment holds at 2/6
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

In multi-agent settings a single injected agent can infect its neighbours, who infect theirs: each agent treats the previous agent's output as trusted context. The per-edge probability `p` (here descriptive, 0.9) times the mean degree gives R0; deterministic simulation floods every reachable node.

This toy uses 4 hand-built six-node topologies (chain, star, mesh, tree):

| Topology | R0 | Uncontained | Contained |
|----------|----|-------------|-----------|
| chain | 1.50 | 6/6 | 2/6 (4 edges blocked) |
| star | 1.50 | 6/6 | n/a |
| mesh | 2.70 | 6/6 | n/a |
| tree | 1.50 | 6/6 | n/a |

Chain containment blocks edges 1–2, 2–3, 3–4, 4–5, isolating nodes 2..5 so only nodes 0 and 1 are infected. R0(chain) = 0.9 × 1.67 = 1.5 > 1, yet containment still holds — structure beats the average.

Boundary: this toy is graph-spread mechanics on hand-built topologies; it is not a measurement on real multi-agent frameworks and makes no outbreak-size claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real agent networks, incidents, models, or credentials
- No network access (standard library only)
- All graphs, spreads and verdicts are hand-built toys

## Run It

```bash
cd demo-16-infection-spread
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_spread.py        # writes results/spread.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-16-infection-spread/INSTRUCTIONS.md).
