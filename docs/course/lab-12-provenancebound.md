# Module 12: ProvenanceBound — Provenance-Aware Calendar Authorization

**Duration**: 1 hour | **Format**: Demo (20 min) + Exercises (25 min) + Policy design (15 min)
**Prerequisites**: Modules 4 (AuthorityBound), 9 (InterceptBound), 10 (ScanBound)
**Demo directory**: `demo-12-provenancebound/`

> Capstone companion: take it after Module 10 (and Module 11 if you audit first). It teaches you to authorize *untrusted content* — including your own agent's proposals — before anything acts on it.

---

## 🎯 Learning Goals

By the end of this module you can:
1. Derive provenance from structure (organizer, forward chain) and explain why text and labels must never drive trust
2. Explain why a detector miss (`cal_008`) must still block when provenance is untrusted and risk is high
3. Show why a detector hit without an attempt (`cal_004`) must not block
4. Detect laundered provenance (organizer mismatch, untrusted forward hop) and state the least-trust rule
5. Write a provenance-aware authorization rule with an explicit unwaivable rung (high-risk untrusted)

## 🧪 Demo Script (20 min, facilitator runs)

Follow [`demo-12-provenancebound/INSTRUCTIONS.md`](../../demo-12-provenancebound/INSTRUCTIONS.md) Steps 0–4 live. Pause at two moments:

1. **After Step 1 (predictions):** poll the room — how many invites will the guarded pipeline allow? Most cohorts guess 3–4. The answer (1) lands harder for having predicted first.
2. **After Step 4 output:** ask *why the baseline allows `cal_008` but the guarded pipeline blocks it, even though both use the same detector.* (Answer: the decision was never the detector's to make — provenance + risk decide, detection is evidence. Thresholds and signatures do not authorize.)

## 📝 Exercises (25 min, students work in pairs)

- **Exercise 12.1** — Add a benign untrusted invite with no verb+endpoint (INSTRUCTIONS Exercises table).
- **Exercise 12.2** — Low-risk lockdown: block all untrusted attempts and price the lost utility.
- **Exercise 12.3** — Harden the detector for the `cal_008` paraphrase without flagging routine scheduling.

Walkthrough with worked answers: [`demo-12-provenancebound/solutions/provenance_walkthrough.md`](../../demo-12-provenancebound/solutions/provenance_walkthrough.md) (release *after* the session).

## 🔗 Links to Earlier Modules

| This module revisits | Connection |
|---|---|
| Module 4 (AuthorityBound) | Provenance = authority, applied to organizer domains and forward chains instead of tool arguments |
| Module 9 (InterceptBound) | Taint-style reasoning (untrusted source poisons downstream) plus a per-action risk ceiling |
| Module 10 (ScanBound) | Scope → validate → execute → taint → policy, recast as provenance → detect → propose → authorize |
| Module 11 (Degenerate Reporting) | Oracle separation: labels never drive attempts, so the block rate is a measurement |
| Final Assessment | Use the provenance-before-content discipline on your own integration practical |

## ✅ Completion Criteria

- `results/provenance_results.json` shows `"result": "pass"` with 8 invites, 1 allowed and 5 blocked
- Step 1 prediction table filled *before* running (not after)
- Exercise 12.2 lockdown implemented with a written utility-cost note
