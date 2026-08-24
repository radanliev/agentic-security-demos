# Module 5: EVIAssure — Evidence-Backed Release Assurance

**Duration**: 1.5 hours | **Difficulty**: ⭐⭐⭐ | **Prerequisites**: Module 0 (Module 4 helpful)
**Demo directory**: `demo-05-eviassure/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Build** a sequence-bound hash chain of witness receipts (genesis → H1 → … → Hn) and verify its integrity
2. **Construct** a Merkle tree from receipt hashes, generate inclusion proofs, and verify them manually
3. **Detect** tampering (modified event), omission (deleted event), and count forgery (malformed closing count)
4. **Generate** Ed25519 demo signing keys, sign receipts, and verify signatures — and explain why they are *not* production keys
5. **Operate** a fail-closed release gate that blocks on incomplete evidence

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
                    Merkle tree over H1..H6 → root
                              │
                    receipts signed (Ed25519, DEMO key)
                              │
                    ReleaseGate verifies ALL before allowing release
```

Three tamper-detection mechanisms, each catching a different attack:

| Mechanism | Detects | Why it works |
|-----------|---------|--------------|
| **Hash chain** | Any modified event | Editing event k changes its receipt hash, breaking the `prev` link of k+1 |
| **Closing counts** | Deleted events | Declared total must match chain length and step numbering |
| **Merkle inclusion proofs** | Substituted receipts | A proof for leaf i only verifies against the root if leaf i is the *original* |

Plus **signatures**: each receipt is signed, so a forged chain must also forge signatures.

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
cd demo-05-eviassure && python3 student/eviassure.py && cd ../..
```

**What this does**: Runs all seven demonstrations: complete-trace verify, tamper, omission, bad count, Merkle proof, signed evidence, incomplete evidence.

**Why it matters**: This is your map for the whole module. Note which checks pass and fail — then Parts 2–5 re-run each piece individually so you can see the mechanics, not just the verdicts.

**Expected output** (abbreviated):
```
1. Verifying complete trace...    PASS
2. Tampered trace:                (see Part 2)
3. Omitted trace:                 FAIL (step_count_mismatch)
4. Bad closing count:             FAIL (closing_count_mismatch)
5. Merkle proof for step 3:       VALID
6. Signed evidence:               (see Part 4)
7. Incomplete evidence:           FAIL (no_signed_receipts)
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
cd ../..
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
cd ../..
```

**What this does**: Modifies one number in one event — changing a failing test count to look better — and runs the release gate on both versions.

**Why it matters — read the output carefully**:

```
original : True
tampered : {'passed': True, ...}     ◄── ?!
```

The gate **accepts the tampered trace**. Why? Because `verify_trace` *rebuilds* the chain from the file's own contents. A self-consistent forged chain verifies. This is not a bug in the demo — it is the demo's deepest lesson:

> **A hash chain proves events are internally consistent with *each other*. It does not prove they are the events that originally happened.** Binding to reality requires an *externally anchored* value — the signed receipts, or a published Merkle root, or a transparency log. That's what Parts 4–5 add.

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
cd ../..
```

**What this does**: Deletes the security-scan step *and* updates the declared count to 5 — a competent forger.

**Why it matters**: The gate still fails, with `step_count_mismatch: 5 != 6`. Why? Because `verify_trace` has a **hard-coded `required_steps=6`** — an expectation recorded *outside* the trace. The forger controlled the trace file entirely and still failed, because the verifier held an independent expectation. Delete the step *without* editing the count and you'd instead get `closing_count_mismatch`. Two different tripwires for two different forger skill levels.

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
cd ../..
```

**What this does**: Builds the Merkle tree, generates an inclusion proof for one leaf, verifies it (True), verifies a one-character-tampered leaf (False), and prints the log₂ scaling.

**Why it matters**: A proof is just the sibling hashes along the leaf's path — 3 nodes for 6 leaves, ~20 for a million. Verification is O(log n). This is why transparency logs (CT, Sigstore) can prove *individual* records to *individual* auditors without shipping the whole log. Note also: the tampered leaf fails because the recomputed root won't match — the proof binds the leaf to this specific root.

---

## ✍️ Part 4: Signatures and the Fail-Closed Gate

### Step 7: Sign receipts and verify the signed package

```bash
cd demo-05-eviassure && python3 - << 'EOF'
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, "student")
from eviassure import (HashChain, WitnessReceipt, DemoKeyManager,
                       ReleaseGate)

steps = json.loads(Path("fixtures/trace.json").read_text())["trace"]
chain = HashChain()
for i, s in enumerate(steps):
    dh = hashlib.sha256(json.dumps(s["data"], sort_keys=True).encode()).hexdigest()
    prev = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
    chain.add_receipt(WitnessReceipt(s["step"], s["action"], dh, prev, s["timestamp"]))

km = DemoKeyManager()
kid = "DEMO_KEY_RELEASE_001"
km.generate_key(kid)

pkg = {"trace_path": "fixtures/trace.json", "signed_receipts": []}
for r in chain.receipts:
    d = r.to_dict()
    payload = json.dumps({k: v for k, v in d.items() if k != "signature"}, sort_keys=True).encode()
    d["signature"] = km.sign(kid, payload)
    d["signer_id"] = kid
    pkg["signed_receipts"].append(d)

Path("results/evidence_package.json").write_text(json.dumps(pkg, indent=2))
gate = ReleaseGate(km)
print("signed package verifies:", gate.verify_signed_evidence(Path("results/evidence_package.json"))["passed"])

# Now flip one byte of one signature
pkg["signed_receipts"][0]["signature"] = ("A" if pkg["signed_receipts"][0]["signature"][0] != "A" else "B") + pkg["signed_receipts"][0]["signature"][1:]
Path("results/forged_sig.json").write_text(json.dumps(pkg, indent=2))
print("forged signature verifies:", gate.verify_signed_evidence(Path("results/forged_sig.json")))
EOF
cd ../..
```

**What this does**: Signs every receipt with the demo Ed25519 key, saves a complete evidence package, verifies it (True), then corrupts one signature character and re-verifies (False, `signature_verification_failed_…`).

**Why it matters**: This closes the Step 4 gap. The self-consistent forged chain from Part 2 now fails, because its receipts aren't *these* signatures. Chain = internal consistency; signatures = binding to a key holder. Together: only someone holding the key can produce a chain the gate accepts.

**Also note the key discipline**: `generate_key` *refuses* any key id not starting with `DEMO_KEY_` — the demo enforces its own "not for production" labeling. Run `km.generate_key("PROD_KEY")` yourself and read the `ValueError`.

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
cd ../..
```

**What this does**: Submits an evidence package with **zero** signed receipts.

**Why it matters**: Output: `{'passed': False, 'reason': 'no_signed_receipts'}`. The gate treats "no signatures" as a failure, not as "nothing to check." Compare with a naive implementation that loops over an empty list and falls through to `passed: True`. **Empty-input handling is where fail-closed systems are won or lost** — the absence of evidence must be evidence of failure. (Module 4 Exercise 4.5 built the same reflex into the mediator.)

---

## 🧵 Part 5: Tests and Benchmark

### Step 9: Run the suite and the benchmark

```bash
cd demo-05-eviassure && python3 -m pytest tests/ -v && python3 student/benchmark.py && cd ../..
```

**What this does**: Runs all 14 tests, then benchmarks verification time across trace sizes 10/50/100/500.

**Why it matters**: The benchmark output shows verify time growing roughly linearly-ish at these sizes (chain walk is O(n); each Merkle proof is O(log n) but you verify n of them). Note which tests pin the module's key lessons: `test_modified_event_fails` (via the no-signatures path), `test_release_blocked_on_incomplete_evidence`, `test_demo_key_signing` (including the `PROD_KEY` refusal).

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 5.1 — Receipt anatomy.**
Modify `WitnessReceipt.compute_hash` to exclude `timestamp` from the hashed content. Demonstrate: changing a timestamp no longer breaks `verify_chain`. Then restore it. In notes: which fields *must* be hash-covered for the chain to mean anything? (Answer: every field whose alteration should be detected.)

**What this teaches**: Hash coverage defines tamper-evidence scope. Undone by one line — understood forever.

### Standard

**Exercise 5.2 — External anchor.**
Implement `publish_root(chain, anchor_path)`: write the Merkle root + chain length to a file *outside* the trace (simulating a transparency log or signed release note). Then implement `verify_against_anchor(trace_path, anchor_path)` that fails if the recomputed root differs — even for a fully self-consistent forged chain. Prove it defeats the Step 4 attack.

**What this teaches**: The fix for "self-consistent forgery" is always an out-of-band expectation. You implemented the concept from Step 5's "generalization" question.

**Exercise 5.3 — Omission with renumbering.**
Forge a trace where you delete step 4 *and renumber* steps 5–6 to 4–5, updating closing counts to 5. Run `verify_trace` with `required_steps=6` (fails on count) — then with `required_steps=5` (passes?). Document what additional verifier expectation (e.g., known step-action sequence, or the anchor from 5.2) would catch renumbering.

**What this teaches**: Adaptive attackers satisfy each individual check; defense requires *multiple independent* expectations.

### Extension

**Exercise 5.4 — Key rotation.**
Extend the package format: receipts may be signed by `DEMO_KEY_RELEASE_001` for steps 1–3 and `DEMO_KEY_RELEASE_002` for 4–6, with a `key_schedule` record in the package mapping step ranges to key ids. Gate verifies each signature against the *scheduled* key. Test: valid schedule passes; a step-5 receipt signed with key-001 fails.

**What this teaches**: Long-lived systems rotate keys; verification must be schedule-aware, or rotation breaks all old evidence (or worse, any leaked key signs everything forever).

**Exercise 5.5 — Partial verification with checkpoints.**
Implement `verify_prefix(trace_path, upto_step)`: verify only receipts 1..k, returning the intermediate chain hash. Discuss in notes: what does a partial verification *prove*, and how does a downstream consumer combine checkpoint hashes to trust a long pipeline without verifying everything at the end?

**What this teaches**: Incremental transparency — the design behind signed tree heads and checkpoint-based logs.

---

## 📝 Lab Notes Questions

1. State precisely what a hash chain proves and what it does not. Use your Step 4 result (tampered trace passed) as evidence.
2. List every verifier expectation that defeated an attack in this module (hard-coded step count, closing counts, signatures). For each: where must that expectation live so the attacker can't edit it?
3. Why is `DEMO_KEY_*` enforcement in `generate_key` more than cosmetic? What production discipline does it foreshadow?

---

## ✅ Completion Checklist

- [ ] Fixture read; closing-count declaration understood
- [ ] Full demo run; all seven sub-demos observed
- [ ] Hash chain built by hand; linkage table printed; tamper avalanche demonstrated
- [ ] **Step 4 lesson recorded in notes** (self-consistent forgery passes chain check)
- [ ] Omission attack run both ways (count edited / not edited)
- [ ] Merkle proof generated, verified, tamper-failed; log₂ scaling noted
- [ ] Signed package verified; single-byte signature forgery rejected; `PROD_KEY` refused
- [ ] Empty-evidence package rejected (fail-closed)
- [ ] All 14 tests pass; benchmark run
- [ ] At least Beginner + Exercise 5.2 (external anchor) — 5.2 is essential
- [ ] `LAB_NOTES.md` Module 5 block filled (seed 42, commit, `make demo DEMO=05`)

---

**⬅️ Prev: [Module 4](lab-04-authoritybound.md) | ➡️ Next: [Module 6: ReconScope](lab-06-reconscope.md)**
