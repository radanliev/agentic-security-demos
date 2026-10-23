# Demo 33: Protocol Coverage

## Learning Objectives

- Explain protocol coverage mapping (each element has a stated mitigation flag and a known-attack flag)
- Flag gaps where a known attack has no stated mitigation: discovery and streaming (2/6)
- List the four covered elements and why each escapes the gap rule
- Distinguish a survey mapping exercise from formal analysis (Demo 24)

## Conceptual Explanation

Agent protocols name similar elements (discovery, identity, streaming) with uneven mitigations. This toy maps six hand-built elements: a gap is `known_attack and not stated_mitigation`.

| Element | Mitigation | Attack | Gap |
|---------|------------|--------|-----|
| discovery | no | yes | **yes** |
| identity | yes | yes | no |
| authorisation | yes | no | no |
| session | yes | yes | no |
| transport | yes | no | no |
| streaming | no | yes | **yes** |

Gaps: 2/6 (discovery, streaming).

Boundary: this demo is a mapping exercise over fixed protocol elements; it is not a formal protocol analysis (Demo 24). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real protocols, implementations, models, or credentials
- No network access (standard library only)
- All elements and verdicts are hand-built toys

## Run It

```bash
cd demo-33-protocol-coverage
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_coverage.py      # writes results/coverage.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-33-protocol-coverage/INSTRUCTIONS.md).
