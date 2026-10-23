# Demo 32: Reproducibility Audit

## Learning Objectives

- Explain what a reproducibility audit checks (code, data, and whether the claim reproduces)
- Audit ten synthetic papers: 6/10 share code+data, 4/10 reproduce
- Verify the invariant that reproducing implies sharing code+data
- Distinguish auditing the field from making new attack claims

## Conceptual Explanation

Surveys of agent security report many defences with few shared artefacts. This toy audits ten hand-built papers across four channels (content, tool, memory, multiagent).

| Check | Result |
|-------|--------|
| Code+data | 6/10 |
| Reproduces | 4/10 |
| Invariant | every reproducing paper shares code+data |

Per-channel reproduction: content 2/3, tool 1/3, memory 1/2, multiagent 0/2.

Boundary: this demo is an audit of the field with no new attack claims; it is not a survey of protocols (Demo 33). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real papers, benchmarks, models, or credentials
- No network access (standard library only)
- All papers and verdicts are hand-built toys

## Run It

```bash
cd demo-32-reproducibility-audit
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_audit.py         # writes results/sok_audit.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-32-reproducibility-audit/INSTRUCTIONS.md).
