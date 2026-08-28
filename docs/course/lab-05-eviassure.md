# Module 5: EVIAssure — Evidence-Backed Release Assurance

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Module 0 (Module 4 helpful)
**Demo directory**: `demo-05-eviassure/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Build** a sequence-bound hash chain of witness receipts (genesis → H1 → … → Hn) and verify its integrity
2. **Construct** a Merkle tree from receipt hashes, generate inclusion proofs, and verify them manually
3. **Detect** tampering (modified event — and see why the hash chain alone cannot), omission (deleted event), and count forgery (malformed closing count)
4. **Generate** Ed25519 demo signing keys, sign receipts, and verify signatures — and explain why they are *not* production keys
5. **Operate** a fail-closed release gate that blocks on incomplete evidence, an unauthorized signer, or a signed receipt that does not match the chain rebuilt from the trace

---

## 📖 Background: Trust, but Verify Cryptographically

A release pipeline produces claims: "tests passed," "no vulns found," "artifact built." Who verifies those claims weren't edited after the fact?

**Evidence-backed assurance** makes the pipeline's history tamper-evident:

```
  STEP          RECEIPT (what's hashed)
  ────          ─────────────────────────────────────────────
  genesis       prev = 000…0
  1  init       receipt = SHA256(step|action|data_hash|prev|ts) ; prev = genesis
  2  config     receipt = SHA256(...)                            ; prev = H1
  3  tests      receipt = SHA256(...)                            ; prev = H2
  4  scan       receipt = SHA256(...)                            ; prev = H3
  5  build      receipt = SHA256(...)                            ; prev = H4
  6  sign       receipt = SHA256(...)                            ; prev = H5
                              │
                    Merkle tree over H1..H6 → root (returned, for anchoring outside the trace)
                              │
                    receipts signed (Ed25519, DEMO key) by an authorized signer
                              │
                    ReleaseGate rebuilds the chain from the trace and releases only if
                    every rebuilt receipt equals the receipt that was signed
```

Three tamper-detection mechanisms, each catching a different attack — and one limit you will hit head-on in Step 4:

| Mechanism | Detects | Why it works |
|-----------|---------|--------------|
| **Hash chain** | An *inconsistent* edit — a receipt that no longer links to its predecessor | Editing event k changes its receipt hash, breaking the `prev` link of k+1. A forger who rebuilds every link after the edit passes this check (Step 4) |
| **Step count, numbering, closing counts** | Deleted events | The verifier holds `required_steps=6` *outside* the trace; steps must be numbered 1..n in order; the declared total must match the chain length |
| **Merkle inclusion proofs** | Substituted receipts — when checked against a root the verifier *already holds* | A proof for leaf i only verifies against the root if leaf i is the *original*. The gate returns the root for external anchoring (Exercise 5.2) instead of checking its own leaves against a root it just computed |

Plus **signed receipts**: the gate requires one receipt per step signed by an authorized key, checks each signature, and compares every signed field with the receipt it rebuilt from the trace. That comparison — not the chain — is what catches a self-consistent forgery.

⚠️ **Safety note**: keys here are `DEMO_KEY_*`, generated per run, never persisted. They demonstrate the *mechanics* of signing. Production release signing requires HSM/KMS-held keys, key rotation, and quorum — none of which a teaching demo should pretend to provide.

---

## 🛠️ Part 1: The Happy Path

### Step 1: Read the trace fixture

```bash
cat demo-05-eviassure/fixtures/trace.json
```

**What this does**: Prints a 6-step release trace (init → load_config → run_tests → security_scan → build_artifact → sign_release), each with data, plus `closing_counts` declaring `total_steps: 6`.

**Why it matters**: `closing_counts` is the *declaration* the chain will be checked against. Deleting a step without editing the count (or editing the count to match the deletion) is exactly the omission attack you'll trigger in Part 3.

---

### Step 2: Run the full demo

```bash
cd demo-05-eviassure && python3 student/eviassure.py && cd ..
```

**What this does**: Runs all nine demonstrations: complete-trace verify, tamper (chain check only), omission, bad count, Merkle proof, signed evidence, tampered trace with the original signatures, incomplete evidence, attacker-signed evidence.

**Why it matters**: This is your map for the whole module. Note which checks pass and fail — then Parts 2–5 re-run each piece individually so you can see the mechanics, not just the verdicts. Sub-demo 2 *passes* on purpose (Part 2 explains why); sub-demos 7 and 9 are where the tamper is actually caught (Part 4).

**Expected output** (verbatim, minus the banner lines):
```
1. Verifying complete trace (chain check)...
   Complete trace: PASS  Reason: ok

2. Tampering with step 3 (tests passed 95 -> 99), chain check only...
   Tampered trace: PASS  Reason: ok
   (expected: the forged chain is self-consistent, so the chain check alone CANNOT catch it)

3. Omitting step 4 (security_scan) and fixing the count to 5...
   Omitted trace: FAIL  Reason: step_count_mismatch: 5 != 6

4. Forging the closing count (999)...
   Bad closing count: FAIL  Reason: closing_count_mismatch

5. Merkle inclusion proof for step 3...
   Merkle proof for step 3: VALID  (3 sibling hashes for 6 leaves)
   Same proof, one hex digit of the leaf changed: INVALID

6. Signing every receipt with DEMO_KEY_RELEASE_001 and verifying the package...
   Signed evidence: PASS  Reason: ok

7. Tampered trace from step 2 presented with the ORIGINAL signed receipts...
   Tampered evidence: FAIL  Reason: receipt_mismatch_step_3_data_hash
   (the signatures are genuine, but they cover the receipts of the ORIGINAL step 3)

8. Evidence package with no signed receipts...
   Incomplete evidence: FAIL  Reason: no_signed_receipts

9. Tampered trace re-signed by an attacker's own key (DEMO_KEY_ATTACKER)...
   Attacker-signed evidence: FAIL  Reason: unauthorized_signer_DEMO_KEY_ATTACKER
```

---

## ⛓️ Part 2: The Hash Chain, By Hand

### Step 3: Build the chain and inspect the linkage

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, "student")
from eviassure import HashChain, WitnessReceipt

steps = json.loads(Path("fixtures/trace.json").read_text())["trace"]
chain = HashChain()

for i, s in enumerate(steps):
    data_hash = hashlib.sha256(json.dumps(s["data"], sort_keys=True).encode()).hexdigest()
    prev = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
    chain.add_receipt(WitnessReceipt(s["step"], s["action"], data_hash, prev, s["timestamp"]))

print(f"{'#':<3}{'action':<16}{'receipt hash (first 12)':<16}{'prev (first 12)'}")
print(f"{'-':<3}{'genesis':<16}{'—':<16}{chain.genesis[:12]}")
for r in chain.receipts:
    print(f"{r.step:<3}{r.action:<16}{r.compute_hash()[:12]:<16}{r.prev_hash[:12]}")

print("\nverify_chain:", chain.verify_chain())
print("closing:", chain.get_closing_count()["total_steps"], "steps, final",
      chain.get_closing_count()["final_hash"][:12])
EOF
cd ..
```

**What this does**: Builds the chain step by step and prints each receipt's hash and its `prev` link.

**Why it matters**: Read the table column-wise: **each row's `prev` equals the previous row's hash.** That's the entire tamper-evidence property. `verify_chain()` walks the chain recomputing hashes; any edit to any event changes its receipt, which then mismatches the next receipt's stored `prev`.

**Now break it** — append to the script above:

```python
chain.receipts[2].action = "run_tests_TAMPERED"
print("after tamper:", chain.verify_chain())
```

It prints `False`. You changed one field on step 3; the chain *and everything after it* becomes unverifiable. This is avalanche behavior — cheap to verify, expensive to forge.

---

### Step 4: Verify tamper detection end-to-end via the gate

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import json
from pathlib import Path
import sys; sys.path.insert(0, "student")
from eviassure import ReleaseGate, DemoKeyManager

km = DemoKeyManager(); km.generate_key("DEMO_KEY_RELEASE_001")
gate = ReleaseGate(km)

t = json.loads(Path("fixtures/trace.json").read_text())
t["trace"][2]["data"]["passed"] = 99        # was 95 — a "better" test result
Path("results/tampered_trace.json").parent.mkdir(exist_ok=True)
Path("results/tampered_trace.json").write_text(json.dumps(t, indent=2))

print("original :", gate.verify_trace(Path("fixtures/trace.json"))["passed"])
print("tampered :", gate.verify_trace(Path("results/tampered_trace.json")))
EOF
cd ..
```

**What this does**: Modifies one number in one event — changing a failing test count to look better — and runs the release gate's chain check (`verify_trace`) on both versions.

**Why it matters — read the output carefully**:

```
original : True
tampered : {'passed': True, 'closing_counts': {...}, 'merkle_root': '1735…', 'steps_verified': 6}     ◄── ?!
```

The gate **accepts the tampered trace**. Why? Because `verify_trace` *rebuilds* the chain from the file's own contents. A self-consistent forged chain verifies. This is not a bug in the demo — it is the demo's deepest lesson (and the test suite pins it: `test_self_consistent_forgery_passes_the_chain_check`):

> **A hash chain proves events are internally consistent with *each other*. It does not prove they are the events that originally happened.** Binding to reality requires an *externally anchored* value — the signed receipts, or a published Merkle root, or a transparency log. That's what Part 4 (signed receipts, compared with the rebuilt chain) and Exercise 5.2 (a published root) add.

Write this sentence in your lab notes. It is the single most important idea in the module.

---

## 🌳 Part 3: Omission, Counts, and Merkle Proofs

### Step 5: Trigger the omission detector

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import json
from pathlib import Path
import sys; sys.path.insert(0, "student")
from eviassure import ReleaseGate, DemoKeyManager

km = DemoKeyManager(); km.generate_key("DEMO_KEY_RELEASE_001")
gate = ReleaseGate(km)

t = json.loads(Path("fixtures/trace.json").read_text())
t["trace"].pop(3)                              # delete security_scan
t["closing_counts"]["total_steps"] = 5         # forger edits the count too
Path("results/omitted_trace.json").write_text(json.dumps(t, indent=2))
print(gate.verify_trace(Path("results/omitted_trace.json")))
EOF
cd ..
```

**What this does**: Deletes the security-scan step *and* updates the declared count to 5 — a competent forger.

**Why it matters**: The gate still fails, with `{'passed': False, 'reason': 'step_count_mismatch: 5 != 6'}`. Why? Because `verify_trace` has a **hard-coded `required_steps=6`** — an expectation recorded *outside* the trace. The forger controlled the trace file entirely and still failed, because the verifier held an independent expectation. Delete the step *without* editing the count (drop the `total_steps` line above) and you get the same `step_count_mismatch: 5 != 6` — the count check runs first. The other tripwires only show once you hand the verifier a matching expectation, `gate.verify_trace(..., required_steps=5)`: the gap in the numbering (1, 2, 3, 5, 6) is caught as `step_numbering_mismatch: index 3 carries step 5`, and a forger who also renumbers the steps but forgets the declaration is caught as `closing_count_mismatch` (`test_stale_closing_count_rejected`). Three tripwires for three forger skill levels — and Exercise 5.3 asks what catches the forger who satisfies all three.

**The generalization**: an omission attack succeeds only when the verifier's expectations live inside the attacker's control boundary. Ask for every integrity system you ever build: *what does the verifier know that the attacker cannot edit?*

---

### Step 6: Merkle proofs — generate, verify, and forge-fail

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, "student")
from eviassure import HashChain, WitnessReceipt, MerkleTree

steps = json.loads(Path("fixtures/trace.json").read_text())["trace"]
chain = HashChain()
for i, s in enumerate(steps):
    dh = hashlib.sha256(json.dumps(s["data"], sort_keys=True).encode()).hexdigest()
    prev = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
    chain.add_receipt(WitnessReceipt(s["step"], s["action"], dh, prev, s["timestamp"]))

leaves = [r.compute_hash() for r in chain.receipts]
tree = MerkleTree(leaves)
root = tree.root()
print("root:", root[:16], "…")

# 1) valid proof for step 3 (index 2)
proof = tree.proof(2)
ok = MerkleTree.verify_proof(leaves[2], proof, root)
print("valid proof verifies:", ok, "| proof size:", len(proof), "nodes for 6 leaves")

# 2) same proof, tampered leaf
bad = leaves[2][:-1] + ("0" if leaves[2][-1] != "0" else "1")
print("tampered leaf verifies:", MerkleTree.verify_proof(bad, proof, root))

# 3) proof size intuition: log2(n)
import math
print("log2(6) ≈", round(math.log2(6), 2), "-> proofs scale logarithmically")
EOF
cd ..
```

**What this does**: Builds the Merkle tree, generates an inclusion proof for one leaf, verifies it (True), verifies a one-character-tampered leaf (False), and prints the log₂ scaling.

**Expected output**:
```
root: fab4c26bc78fbba8 …
valid proof verifies: True | proof size: 3 nodes for 6 leaves
tampered leaf verifies: False
log2(6) ≈ 2.58 -> proofs scale logarithmically
```

**Why it matters**: A proof is just the sibling hashes along the leaf's path — 3 nodes for 6 leaves, ~20 for a million. Verification is O(log n). This is why transparency logs (CT, Sigstore) can prove *individual* records to *individual* auditors without shipping the whole log. Note also: the tampered leaf fails because the recomputed root won't match — the proof binds the leaf to this specific root. That binding only means something when the verifier got the root from somewhere the forger cannot edit. Proving leaves against a root computed from the same file could never fail, which is why the gate does not do it: `verify_trace` computes the root and *returns* it as `merkle_root` (you saw it in Step 4) for you to anchor externally in Exercise 5.2.

---

## ✍️ Part 4: Signatures and the Fail-Closed Gate

### Step 7: Sign receipts and verify the signed package

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, "student")
from eviassure import (HashChain, WitnessReceipt, DemoKeyManager,
                       ReleaseGate, sign_receipt)

steps = json.loads(Path("fixtures/trace.json").read_text())["trace"]
chain = HashChain()
for i, s in enumerate(steps):
    dh = hashlib.sha256(json.dumps(s["data"], sort_keys=True).encode()).hexdigest()
    prev = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
    chain.add_receipt(WitnessReceipt(s["step"], s["action"], dh, prev, s["timestamp"]))

km = DemoKeyManager()
kid = "DEMO_KEY_RELEASE_001"
km.generate_key(kid)
gate = ReleaseGate(km, authorized_signer_ids={kid})   # explicit trust store

# sign_receipt sets signer_id BEFORE signing — it is part of the signed payload
pkg = {"trace_path": "fixtures/trace.json",
       "signed_receipts": [sign_receipt(km, kid, r) for r in chain.receipts]}
Path("results/evidence_package.json").write_text(json.dumps(pkg, indent=2))
print("signed package verifies:", gate.verify_signed_evidence(Path("results/evidence_package.json"))["passed"])

# 1) The self-consistent forgery from Step 4, presented with these genuine signatures
pkg["trace_path"] = "results/tampered_trace.json"
Path("results/tampered_evidence.json").write_text(json.dumps(pkg, indent=2))
print("tampered trace + genuine signatures:", gate.verify_signed_evidence(Path("results/tampered_evidence.json")))
pkg["trace_path"] = "fixtures/trace.json"

# 2) Now flip one byte of one signature
pkg["signed_receipts"][0]["signature"] = ("A" if pkg["signed_receipts"][0]["signature"][0] != "A" else "B") + pkg["signed_receipts"][0]["signature"][1:]
Path("results/forged_sig.json").write_text(json.dumps(pkg, indent=2))
print("forged signature verifies:", gate.verify_signed_evidence(Path("results/forged_sig.json")))

# 3) The forger re-signs the tampered trace with a key of their own
km.generate_key("DEMO_KEY_ATTACKER")
forged_chain = HashChain.from_trace(json.loads(Path("results/tampered_trace.json").read_text())["trace"])
att = {"trace_path": "results/tampered_trace.json",
       "signed_receipts": [sign_receipt(km, "DEMO_KEY_ATTACKER", r) for r in forged_chain.receipts]}
Path("results/attacker_signed.json").write_text(json.dumps(att, indent=2))
print("attacker-signed forgery verifies:", gate.verify_signed_evidence(Path("results/attacker_signed.json")))
EOF
cd ..
```

**What this does**: Signs every receipt with the demo Ed25519 key via `sign_receipt`, saves a complete evidence package, verifies it (True); then presents the tampered trace from Step 4 with those same genuine signatures; then corrupts one signature character; then has the forger re-sign the tampered trace with a key the gate does not trust.

**Expected output**:
```
signed package verifies: True
tampered trace + genuine signatures: {'passed': False, 'reason': 'receipt_mismatch_step_3_data_hash'}
forged signature verifies: {'passed': False, 'reason': 'signature_verification_failed_DEMO_KEY_RELEASE_001'}
attacker-signed forgery verifies: {'passed': False, 'reason': 'unauthorized_signer_DEMO_KEY_ATTACKER'}
```

**Why it matters**: This closes the Step 4 gap. `verify_signed_evidence` rebuilds the chain from whatever trace the package points at, then requires one signed receipt per step, from a signer in `authorized_signer_ids`, with a valid signature, **and** field-by-field equality between the signed receipt and the rebuilt one. The forged trace rebuilds to a different `data_hash` for step 3, so it fails with `receipt_mismatch_step_3_data_hash` — the signatures are genuine, but they cover the *original* step 3. Chain = internal consistency; signatures = binding to a key holder; the comparison = binding the chain to what the key holder actually signed. Together: only someone holding an authorized key can produce a package the gate accepts. Drop the `authorized_signer_ids` argument and the gate trusts every key the manager holds — the attacker-signed forgery then *passes* (`test_unauthorized_signer_rejected` checks both behaviors). A trust store is not optional.

**One ordering trap**: `signer_id` is inside the signed payload, so it must be set *before* signing — `sign_receipt` does that. Sign first and set it afterwards, and your own package comes back `signature_verification_failed_DEMO_KEY_RELEASE_001` (`test_sign_receipt_payload_includes_signer_id`).

**Also note the key discipline**: `generate_key` *refuses* any key id not starting with `DEMO_KEY_` — the demo enforces its own "not for production" labeling. Run `km.generate_key("PROD_KEY")` yourself and read the `ValueError` (`Key ID must start with 'DEMO_KEY_': PROD_KEY`).

---

### Step 8: Fail-closed on incomplete evidence

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import json, sys
from pathlib import Path
sys.path.insert(0, "student")
from eviassure import ReleaseGate, DemoKeyManager

km = DemoKeyManager(); km.generate_key("DEMO_KEY_RELEASE_001")
gate = ReleaseGate(km)

pkg = {"trace_path": "fixtures/trace.json", "signed_receipts": []}
Path("results/incomplete_evidence.json").write_text(json.dumps(pkg, indent=2))
print(gate.verify_signed_evidence(Path("results/incomplete_evidence.json")))
EOF
cd ..
```

**What this does**: Submits an evidence package with **zero** signed receipts.

**Why it matters**: Output: `{'passed': False, 'reason': 'no_signed_receipts'}`. The gate treats "no signatures" as a failure, not as "nothing to check." Compare with a naive implementation that loops over an empty list and falls through to `passed: True`. **Empty-input handling is where fail-closed systems are won or lost** — the absence of evidence must be evidence of failure. (Module 4 Exercise 4.5 built the same reflex into the mediator.) Partial evidence is treated the same way: one signed receipt for a six-step trace is rejected as `signed_receipt_count_mismatch: 1 != 6` (`test_every_receipt_must_be_signed`).

---

## 🧵 Part 5: Tests and Benchmark

### Step 9: Run the suite and the benchmark

```bash
cd demo-05-eviassure && python3 -m pytest tests/ -v && python3 student/benchmark.py && cd ..
```

**What this does**: Runs all 34 tests, then benchmarks trace sizes 10/50/100/500: `chain_build_ms` is the chain rebuild, `verify_time_ms` is building the Merkle tree and verifying an inclusion proof for *every* leaf. Each size is timed five times and the minimum is printed; `result` is `pass` only if every proof verified (the script exits 1 otherwise).

**Expected output** (tail of the benchmark JSON; times are from one machine — yours will differ, the `proof_length` values will not):
```
============================== 34 passed in 0.28s ==============================
{
  "demo": "demo-05-eviassure",
  ...
  "result": "pass",
  "notes": "Synthetic teaching fixture; min of 5 runs; timings are machine-dependent, verdicts are not",
  "benchmarks": [
    {
      "trace_size": 10,
      "chain_build_ms": 0.08,
      "verify_time_ms": 0.08,
      "proof_length": 4
    },
    {
      "trace_size": 50,
      "chain_build_ms": 0.41,
      "verify_time_ms": 0.52,
      "proof_length": 6
    },
    {
      "trace_size": 100,
      "chain_build_ms": 0.84,
      "verify_time_ms": 1.15,
      "proof_length": 7
    },
    {
      "trace_size": 500,
      "chain_build_ms": 4.27,
      "verify_time_ms": 7.32,
      "proof_length": 9
    }
  ]
}
```

**Why it matters**: `chain_build_ms` grows linearly (the chain walk is O(n)); `verify_time_ms` grows a little faster (each Merkle proof is O(log n) but you verify n of them); `proof_length` grows like log₂ n. Note which tests pin the module's key lessons: `test_self_consistent_forgery_passes_the_chain_check` (Step 4), `test_tampered_trace_with_original_signatures_fails` and `test_unauthorized_signer_rejected` (Step 7), `test_release_blocked_on_incomplete_evidence` (Step 8), `test_demo_key_signing` (including the `PROD_KEY` refusal).

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 5.1 — Receipt anatomy.**
Modify `WitnessReceipt.compute_hash` to exclude `timestamp` from the hashed content. Demonstrate: changing a timestamp no longer breaks `verify_chain` (and exactly one test, `test_every_field_is_hash_covered`, fails — that test is the guard). Then restore it. In notes: which fields *must* be hash-covered for the chain to mean anything? (Answer: every field whose alteration should be detected.)

**What this teaches**: Hash coverage defines tamper-evidence scope. Undone by one line — understood forever.

### Standard

**Exercise 5.2 — External anchor.**
Implement `publish_root(chain, anchor_path)`: write the Merkle root + chain length to a file *outside* the trace (simulating a transparency log or signed release note). `verify_trace` already computes the root and returns it as `merkle_root`. Then implement `verify_against_anchor(trace_path, anchor_path)` that fails if the recomputed root differs — even for a fully self-consistent forged chain. Prove it defeats the Step 4 attack *without* any signatures.

**What this teaches**: The fix for "self-consistent forgery" is always an out-of-band expectation. You implemented the concept from Step 5's "generalization" question.

**Exercise 5.3 — Omission with renumbering.**
Forge a trace where you delete step 4 *and renumber* steps 5–6 to 4–5, updating closing counts to 5. Run `verify_trace` with `required_steps=6` (fails on count) — then with `required_steps=5` (it passes: nothing inside the trace is inconsistent). Document what additional verifier expectation (e.g., known step-action sequence, or the anchor from 5.2) would catch renumbering. Then run the signed gate on the same forgery with the six receipts you signed in Step 7 and `required_steps=5`: `signed_receipt_count_mismatch: 6 != 5` (`test_renumbered_omission_needs_an_external_expectation`).

**What this teaches**: Adaptive attackers satisfy each individual check; defense requires *multiple independent* expectations.

### Extension

**Exercise 5.4 — Key rotation.**
Extend the package format: receipts may be signed by `DEMO_KEY_RELEASE_001` for steps 1–3 and `DEMO_KEY_RELEASE_002` for 4–6, with a `key_schedule` record in the package mapping step ranges to key ids. Gate verifies each signature against the *scheduled* key. `authorized_signer_ids` already restricts *which* keys are trusted; the schedule adds *which key for which steps* — today a step-5 receipt validly signed by key-001 passes a gate that trusts both keys. Test: valid schedule passes; a step-5 receipt signed with key-001 fails.

**What this teaches**: Long-lived systems rotate keys; verification must be schedule-aware, or rotation breaks all old evidence (or worse, any leaked key signs everything forever).

**Exercise 5.5 — Partial verification with checkpoints.**
Implement `verify_prefix(trace_path, upto_step)`: verify only receipts 1..k, returning the intermediate chain hash. Discuss in notes: what does a partial verification *prove*, and how does a downstream consumer combine checkpoint hashes to trust a long pipeline without verifying everything at the end?

**What this teaches**: Incremental transparency — the design behind signed tree heads and checkpoint-based logs.

---

## 📝 Lab Notes Questions

1. State precisely what a hash chain proves and what it does not. Use your Step 4 result (tampered trace passed) as evidence.
2. List every verifier expectation that defeated an attack in this module (hard-coded step count, step numbering, closing counts, the authorized-signer set, the signed receipts compared field by field with the rebuilt chain). For each: where must that expectation live so the attacker can't edit it?
3. Why is `DEMO_KEY_*` enforcement in `generate_key` more than cosmetic? What production discipline does it foreshadow?

---

## ✅ Completion Checklist

- [ ] Fixture read; closing-count declaration understood
- [ ] Full demo run; all nine sub-demos observed
- [ ] Hash chain built by hand; linkage table printed; tamper avalanche demonstrated
- [ ] **Step 4 lesson recorded in notes** (self-consistent forgery passes chain check)
- [ ] Omission attack run both ways (count edited / not edited — same `step_count_mismatch`); numbering and closing-count tripwires seen with `required_steps=5`
- [ ] Merkle proof generated, verified, tamper-failed; log₂ scaling noted
- [ ] Signed package verified; tampered trace with genuine signatures rejected (`receipt_mismatch_step_3_data_hash`); single-byte signature forgery rejected; attacker key rejected as unauthorized; `PROD_KEY` refused
- [ ] Empty-evidence package rejected (fail-closed)
- [ ] All 34 tests pass; benchmark run
- [ ] At least Beginner + Exercise 5.2 (external anchor) — 5.2 is essential
- [ ] `LAB_NOTES.md` Module 5 block filled (seed 42, commit, `make demo DEMO=05`)

---

**⬅️ Prev: [Module 4](lab-04-authoritybound.md) | ➡️ Next: [Module 6: ReconScope](lab-06-reconscope.md)**
