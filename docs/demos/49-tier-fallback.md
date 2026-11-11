# Demo 49: Tier Fallback

## Learning Objectives

- Explain why an orchestrator's model tier is part of the security state
- Check authority invariance across a mid-task tier switch (rule R1)
- Detect stale plans that ran after a switch without re-validation (rule R2)
- Detect actions that executed without a monitor decision (rule R3)
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Agents often fall back from a premium model to a cheaper tier mid-task. If
policy decisions and plans were computed on the strong tier, they may no
longer hold on the weak one. This toy replays four hand-built traces and
checks three invariants.

| Trace | Verdict |
|-------|---------|
| compliant_switch | clean (no violations) |
| tier_dependent_decision | R1: decision differs from policy on the fallback tier |
| stale_plan_after_switch | R2: pre-switch plan step ran without re-validation |
| unmediated_fallback | R3: action ran without a monitor decision |

A compliant switch re-validates the plan and re-decides each action on the
new tier; the three failure traces each break exactly one rule.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real models, providers, or credentials
- No network access (standard library only)
- All traces are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real orchestrators

## Run It

```bash
cd demo-49-tier-fallback-authority-invariance
python3 -m pytest tests/ -v          # 7 tests, <1 min
python3 student/run_tiers.py         # writes results/tier_invariance.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-49-tier-fallback-authority-invariance/INSTRUCTIONS.md).
