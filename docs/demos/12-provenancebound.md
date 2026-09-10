# Demo 12: ProvenanceBound

## Learning Objectives

- Derive provenance from structured invite fields — never from body text or labels
- Detect prompt-injection indicators with deterministic lexical rules and Unicode canonicalization
- Propose outbound actions with a naive verb+endpoint agent (inert, recorded only)
- Enforce provenance-aware deny-by-default authorization that holds even when the detector misses
- Separate oracle labels from observed attempts so block rates are measurements, not restated rules

## Conceptual Explanation

An agent acting on calendar invites must answer *where did this come from* before *what does it say*. ProvenanceBound derives trust from organizer domains and forward chains (fail-closed to untrusted), scans bodies with six explainable lexical rules, proposes actions with a naive verb+endpoint heuristic, and authorizes via a provenance-aware policy: high-risk + untrusted is always blocked, low-risk + untrusted is blocked only when suspicious, trusted is blocked only when suspicious, and no attempt means `not_requested`. The naive baseline proposes identically but trusts everything and allows every attempt.

The demo's key inversion: `cal_008` (third-party paraphrase) is clean to every detector signature, yet the guarded pipeline blocks it on provenance alone — while the baseline allows it. A suspicious flag without an attempt (`cal_004`) is `not_requested`, never blocked.

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No mail sent** — synthetic JSON invites; all actions are recorded strings
- Domains are reserved (`internal.example`, `trusted.example`, `external.invalid`) and never contacted
- No credentials, no mailboxes, no network endpoints

## Run It

```bash
cd demo-12-provenancebound
python3 -m pytest tests/ -v          # 44 tests, ~1 min
python3 student/provenancebound.py   # baseline + guarded pipelines
python3 student/generate_provenance_results.py  # writes results/provenance_results.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-12-provenancebound/INSTRUCTIONS.md). Course lab: [Lab 12](../course/lab-12-provenancebound.md).
