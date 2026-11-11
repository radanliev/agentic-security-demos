# Demo 50: Budget Delegation

## Learning Objectives

- Model a delegation tree with a shared token/cost budget
- State conservation invariants B1–B5 for spend across delegated nodes
- Show that fan-out caps and unknown-node denials preserve the invariants
- Explain why "requested" spend is not the same as "executed" spend
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A root agent delegates subtasks with attached budgets. This toy executes two
hand-built plans and checks five budget invariants after every step.

| Plan | Requested | Spent | Denials | Invariants |
|------|-----------|-------|---------|------------|
| within_budget | 9,000 | 9,000 | none | B1–B5 all hold |
| fanout_beyond_cap | 4,500 | 2,700 | 2 fan-out cap, 2 unknown node | B1–B5 all hold |

The second plan asks for more than it may spend: the budget broker denies
delegation past the fan-out cap and spends from unregistered nodes, so the
invariants hold precisely because the excess never executes.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real payments, tokens, or credentials
- No network access (standard library only)
- Both plans are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real agents

## Run It

```bash
cd demo-50-budget-bounded-delegation
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_budget.py        # writes results/delegation_budget.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-50-budget-bounded-delegation/INSTRUCTIONS.md).

## Relationship to Demos 24 and 49

Demo 24 checks delegation authority (audience binding, no scope growth);
demo 49 checks authority invariance under tier switches. This demo checks the
third axis — budget conservation across the delegation tree.
