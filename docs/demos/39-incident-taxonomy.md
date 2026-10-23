# Demo 39: Incident Taxonomy

## Learning Objectives

- Explain what a practitioner incident taxonomy is (patterns mapped to controls)
- Tally 10 synthetic incidents into 4 attack patterns with prompt-injection on top at 4/10
- Show a static 10-item control catalogue with 7/10 entries supported
- State a tie-break rule and defend why counts alone do not settle a tie
- Distinguish this practitioner guidance toy from any research claim

## Conceptual Explanation

Practitioners turn incident reports into counts: which pattern recurs, and which controls already cover it? On 10 hand-built incident sketches:

| Pattern | Count |
|---------|-------|
| prompt-injection | 4/10 (top) |
| tool-misuse | 3/10 |
| data-exfiltration | 2/10 |
| privilege-escalation | 1/10 |

The static control catalogue (input sanitisation, allowlists, provenance labelling, human approval, egress filtering, memory gating, audit logging) supports 7/10 entries; cross-agent attestation, hardware-backed identity and formal verification are marked unsupported. The lesson is deliberately thin: counts guide where to look first, nothing more.

### Why the tie-break matters

Move one sketch (`inc10` → `tool-misuse`, see INSTRUCTIONS Step 5) and the top two patterns tie at 4/10 — yet the reported top stays `prompt-injection`. The tally resolves ties deterministically (alphabetically-first maximum), pinned by `test_tie_break_is_deterministic`. A practitioner table that omits its tie-break rule reports a verdict its counts do not determine.

Boundary: this demo is practitioner guidance from hand-built sketches; it is not a research study of real incidents. Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real incidents, vendors, systems, or credentials
- No network access (standard library only)
- All sketches, counts and verdicts are hand-built toys

## Run It

```bash
cd demo-39-incident-taxonomy
python3 -m pytest tests/ -v          # 19 tests, <1 min
python3 student/run_tax.py           # writes results/taxonomy.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-39-incident-taxonomy/INSTRUCTIONS.md).
