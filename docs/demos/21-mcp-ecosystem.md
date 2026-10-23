# Demo 21: MCP Ecosystem Census

## Learning Objectives

- Explain what tool poisoning is (a tool description carrying instructions to the model, not the user)
- Define a rug pull (a version update that silently adds capabilities or rewrites the description)
- Run a miniature census: poisoning prevalence, version drift, capability bundling, maintainer concentration
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

The Model Context Protocol registry lists tens of thousands of tool servers. This toy models twelve synthetic servers: 4/12 poisoned descriptions (concentrated on low-download servers), 3/11 version pairs with material drift, shell servers bundling network access 4/4, and top-4 servers held by 2 maintainers. Server `srv-06` is the lesson in one row: a poisoned description plus a version that adds network and file-write while rewriting its text — a rug pull a user would not re-approve.

Boundary: this demo is a registry census over manifests; it is not statistical gating over action scores (Demo 14). Different data and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real registry data, packages, maintainers, or downloads
- No network access (standard library only)
- All servers, descriptions and verdicts are hand-built toys

## Run It

```bash
cd demo-21-mcp-ecosystem
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_census.py        # writes results/census.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-21-mcp-ecosystem/INSTRUCTIONS.md).
