# Demo 20: Agent Web Census

## Learning Objectives

- Explain agent-facing web measurement (which sites publish agent directives, which carry injections)
- Tally adoption (either directive flag) and exposure (injection text) over 10 synthetic sites
- Show adoption 4/10 and injections 2/10, both injections on low-popularity sites
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Sites increasingly ship agent directives alongside human pages. A census asks two independent questions: who publishes directives, and whose copy carries injection text. This toy uses 10 hand-built sites: adoption 4/10, exposure 2/10, both exposures on low-popularity sites.

Boundary: this demo is web measurement over page directives; it is not an MCP registry census (Demo 21). Different corpus, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real crawl data, sites, models, or credentials
- No network access (standard library only)
- All sites, directives and verdicts are hand-built toys

## Run It

```bash
cd demo-20-agent-web-census
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_web.py           # writes results/web_census.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-20-agent-web-census/INSTRUCTIONS.md).
