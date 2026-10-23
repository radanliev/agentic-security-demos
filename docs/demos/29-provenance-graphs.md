# Demo 29: Provenance Graphs

## Learning Objectives

- Explain what an agent action provenance graph is (nodes are actions, edges are cause links, roots need authority)
- Reconstruct attribution over six synthetic actions and flag the orphan with no cause (`a5`, attribution 5/6)
- Show a sha256 chain over ordered records verifies cleanly but breaks when a copy is tampered
- Distinguish post-incident reconstruction from release assurance (Demo 05)

## Conceptual Explanation

After an incident, investigators rebuild who caused what: each action should point at its cause, back to a trusted root. One orphan with a null cause that is not the root cannot be attributed — here `a5`, so attribution is 5/6.

A separate integrity layer chains the ordered records with sha256. The clean chain verifies; a copy with one edited authority field fails verification.

| Check | Result |
|-------|--------|
| Attributable | 5/6 (unattributable: a5) |
| Chain over clean records | verified |
| Chain over tampered copy | tamper detected |

Boundary: this demo is post-incident reconstruction on hand-built records; it is not release assurance (Demo 05) and not a forensic study of real logs. Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real incidents, logs, models, or credentials
- No network access (standard library only)
- All actions, authorities and hashes are hand-built toys

## Run It

```bash
cd demo-29-provenance-graphs
python3 -m pytest tests/ -v          # 6 tests, <1 min
python3 student/run_prov.py          # writes results/provenance.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-29-provenance-graphs/INSTRUCTIONS.md).
