# Demo 44: Toolflow Taint

## Learning Objectives

- Explain what toolflow taint is (unlabelled data reaching a sensitive sink)
- Trace 8 synthetic toolflow edges and find 5/8 unlabelled flows into sensitive sinks
- Name the sensitive sinks (code, shell, file, network, memory) vs the non-sensitive one (next-args)
- Distinguish measured missing labels (this toy) from enforcement policy (Demo 04 AuthorityBound)

## Conceptual Explanation

Agents pipe tool outputs into new actions; without provenance labels, nobody knows which input shaped a dangerous call. On 8 hand-built flow edges:

| Flow | Sink | Labelled? |
|------|------|-----------|
| flow1–flow5 | shell, file, network, memory, code | No (tainted) |
| flow6 | shell | Yes |
| flow7–flow8 | next-args | n/a (non-sensitive sink) |

The lesson: 5/8 flows reach sensitive sinks unlabelled. Counting the missing labels is the measurement; deciding what to block is policy — and policy lives elsewhere (Demo 04 AuthorityBound).

Boundary: this demo measures missing provenance labels on fixed edges; it is not authority enforcement (Demo 04). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real tool traces, systems, or credentials
- No network access (standard library only)
- All flows, sinks and verdicts are hand-built toys

## Run It

```bash
cd demo-44-toolflow-taint
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_taint.py         # writes results/taint.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-44-toolflow-taint/INSTRUCTIONS.md).
