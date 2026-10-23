# Demo 43: Terms Coding

## Learning Objectives

- Explain what platform-terms coding is (reading accountability out of terms of service)
- Code 8 synthetic platform terms against 3 clauses: disclaim 5/8, monitoring 4/8, consent 3/8
- Show the accountability gradient (disclaimers common, delegation consent rare)
- Distinguish this teaching toy from the pending content analysis it illustrates

## Conceptual Explanation

Terms of service allocate responsibility between platform and deployer. Coding 8 hand-built platform records against 3 accountability clauses: disclaims_autonomy 5/8, requires_monitoring 4/8, consent_for_delegation 3/8. The lesson is the gradient: platforms disclaim autonomy more often than they demand monitoring, and delegation consent is rarest — the accountability burden slides downhill to the deployer.

Boundary: this demo codes accountability TERMS; Demo 38 codes assurance claims against obligations. Different sources, methods, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real platforms, terms of service, or credentials
- No network access (standard library only)
- All platforms, clauses and verdicts are hand-built toys

## Run It

```bash
cd demo-43-terms-coding
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_terms.py         # writes results/terms.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-43-terms-coding/INSTRUCTIONS.md).
