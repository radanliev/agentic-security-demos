# Demo 30: Insecure Defaults

## Learning Objectives

- Explain what an insecure default is (public bind without auth, privileged run, pinned vulnerable dependency)
- Apply the three-clause rule to ten synthetic stacks and count 6/10 insecure
- Show pinned vulns account for 3/10 of the sample
- Distinguish deployment config review from vulnerability lifecycle work (Demo 42)

## Conceptual Explanation

Language-model stacks ship with example configs that operators copy. This toy checks ten hand-built stacks with a fixed rule: insecure when publicly bound without auth, or privileged, or pinning a vuln.

| Check | Result |
|-------|--------|
| Insecure | 6/10 (s01, s03, s04, s05, s07, s09) |
| Pinned vuln | 3/10 (s04, s07, s09) |
| Secure | 4/10 |

Stacks `s02`, `s06`, `s08`, `s10` are the secure contrast: no public-without-auth, no privileged flag, no pinned vuln.

Boundary: this demo covers deployment configs only, not vulnerability lifecycle or patch adoption (Demo 42). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real stacks, registries, images, or credentials
- No network access (standard library only) and no live scanning
- All stacks and verdicts are hand-built toys

## Run It

```bash
cd demo-30-default-configs
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_defaults.py      # writes results/defaults.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-30-default-configs/INSTRUCTIONS.md).
