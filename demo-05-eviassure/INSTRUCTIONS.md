# Demo 05: EVIAssure — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md). Full course lab: [../docs/course/lab-05-eviassure.md](../docs/course/lab-05-eviassure.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the 9-part demo | 3 min | `python3 student/eviassure.py` |
| Run the benchmark | 1 min | `python3 student/benchmark.py` |
| Hand-built chain experiment | 5 min | inline script (Step 4) |
| **Total** | **~15 min** | |

**Safety**: 100% offline. Ed25519 keys are generated in memory per run, never written to disk, and labeled `DEMO_KEY_*` — **never production signing keys**. Synthetic traces only. Requires the `cryptography` package (installed by `make setup`).

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-05-eviassure
```

---

## Step 1 — Read the Fixture and Understand the Trace

```bash
cat fixtures/trace.json
```

**What this does**: Shows a 6-step release trace (init → load_config → run_tests → security_scan → build_artifact → sign_release) and `closing_counts` declaring `total_steps: 6`.

**Before running, note**: `closing_counts` is the *declaration* the chain will be checked against. Deleting a step without editing the count — or editing the count to match a deletion — are two different forgery strategies you'll trigger below.

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected**: `34 passed`. Key tests: hash chain integrity and hash coverage, Merkle inclusion proofs (valid, forged leaf, wrong leaf, swapped positions), demo key signing (including refusal of non-`DEMO_KEY_` ids), the self-consistent forgery *passing* the chain check, the same forgery *failing* the signed gate, omission/count/numbering detection, release blocked on incomplete evidence, unauthorised signer rejected.

```
============================== 34 passed in 0.XXs ==============================
```

---

## Step 3 — Run the Full Demo (9 Sub-Demonstrations)

```bash
python3 student/eviassure.py
```

**What this does**: Runs all nine demonstrations in sequence. Sub-demos 1–4 use only the trace file; 6–9 use the signed evidence package.

**Expected output** (verbatim, minus the hashes):

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

**⚠️ The most important observation in this demo** — read sub-demos 2 and 7 together. In sub-demo 2 the gate reports the *tampered* trace as **PASS**. This is not a bug: `verify_trace` rebuilds the chain from the file's own contents, so a *self-consistent* forged chain verifies. A hash chain proves events are consistent *with each other* — it does not prove they are the events that originally happened. Sub-demo 7 is where tampering is actually detected: the gate rebuilds the chain from the tampered trace and compares each rebuilt receipt, field by field, with the receipt the release key signed. Step 3's `data_hash` no longer matches, and the forger cannot produce a matching signed receipt without the key (sub-demo 9: a signature under the attacker's own key is rejected as an unauthorised signer). Record this in your notes.

---

## Step 4 — Build the Hash Chain by Hand

```bash
python3 - << 'EOF'
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, "student")
from eviassure import HashChain, WitnessReceipt

steps = json.loads(Path("fixtures/trace.json").read_text())["trace"]
chain = HashChain()
for i, s in enumerate(steps):
    dh = hashlib.sha256(json.dumps(s["data"], sort_keys=True).encode()).hexdigest()
    prev = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
    chain.add_receipt(WitnessReceipt(s["step"], s["action"], dh, prev, s["timestamp"]))

print(f"{'#':<3}{'action':<16}{'hash (12)':<15}{'prev (12)'}")
print(f"{'-':<3}{'genesis':<16}{'—':<15}{chain.genesis[:12]}")
for r in chain.receipts:
    print(f"{r.step:<3}{r.action:<16}{r.compute_hash()[:12]:<15}{r.prev_hash[:12]}")

print("\nverify_chain:", chain.verify_chain())
chain.receipts[2].action = "TAMPERED"
print("after tamper:", chain.verify_chain())
EOF
```

**What this does**: Builds the chain receipt-by-receipt, prints the linkage table, then tampers one event.

**Expected**: the table shows **each row's `prev` equals the previous row's hash**; `verify_chain` prints `True`, then `False` after the tamper. One changed field invalidates the chain from that point forward — cheap to verify, expensive to forge.

---

## Step 5 — Merkle Proof Experiment

```bash
python3 - << 'EOF'
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

proof = tree.proof(2)
print("valid proof verifies:", MerkleTree.verify_proof(leaves[2], proof, root),
      "| proof size:", len(proof), "nodes for 6 leaves")

bad = leaves[2][:-1] + ("0" if leaves[2][-1] != "0" else "1")
print("tampered leaf verifies:", MerkleTree.verify_proof(bad, proof, root))
EOF
```

**Expected**:

```
valid proof verifies: True | proof size: 3 nodes for 6 leaves
tampered leaf verifies: False
```

**Lesson**: a proof is just the sibling hashes along the leaf's path (3 nodes for 6 leaves, ~20 for a million — logarithmic). This is why transparency logs can prove individual records without shipping the whole log.

---

## Step 6 — Run the Benchmark

```bash
python3 student/benchmark.py
```

**What this does**: Builds chains of 10/50/100/500 receipts (`chain_build_ms`), then builds the Merkle tree and verifies an inclusion proof for every leaf (`verify_time_ms`). Each size is timed five times and the minimum is reported. `result` is `pass` only if every proof verified.

**Expected output** (JSON; times vary by machine — record yours):

```
{"trace_size": 10,  "chain_build_ms": ~0.1, "verify_time_ms": ~0.1, "proof_length": 4}
{"trace_size": 50,  "chain_build_ms": ~0.4, "verify_time_ms": ~0.5, "proof_length": 6}
{"trace_size": 100, "chain_build_ms": ~0.9, "verify_time_ms": ~1.1, "proof_length": 7}
{"trace_size": 500, "chain_build_ms": ~4,   "verify_time_ms": ~7,   "proof_length": 9}
```

**Record your times** in the reproducibility table — they will differ from another participant's machine, which is itself a reproducibility lesson (timing is environment-dependent; verdicts are not). Note that `proof_length` grows like log2(n) while the total time grows like n·log n, because you verify *every* leaf.

---

## Step 7 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2–6 |
| Tests passed | | `34 passed` |
| Complete trace verdict | | PASS (Step 3.1) |
| Tampered trace, chain check only | | PASS (Step 3.2 — the lesson) |
| Omission verdict | | FAIL, `step_count_mismatch` (Step 3.3) |
| Bad count verdict | | FAIL, `closing_count_mismatch` (Step 3.4) |
| Merkle proof | | VALID, forged leaf INVALID (Step 3.5) |
| Signed evidence | | PASS (Step 3.6) |
| Tampered evidence | | FAIL, `receipt_mismatch_step_3_data_hash` (Step 3.7) |
| Incomplete evidence | | FAIL, `no_signed_receipts` (Step 3.8) |
| Attacker-signed evidence | | FAIL, `unauthorized_signer_DEMO_KEY_ATTACKER` (Step 3.9) |
| Benchmark (500 leaves) | | your ms from Step 6 |
| Result files | | `results/benchmark.json`, `results/evidence_package.json` |

**Reproducibility check**: `rm -rf results/`, re-run Steps 3 and 6. All **verdicts** must be identical; benchmark **times** will differ slightly (that's expected — note the difference).

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=05`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Remove `timestamp` from `compute_hash`; show timestamp edits no longer break the chain; restore | Hash coverage = tamper-evidence scope |
| Standard | External anchor: publish the Merkle root (`verify_trace` returns it) to a separate file; verify against it; defeat the self-consistent forgery from Step 3.2 *without* signatures | The verifier needs an expectation the attacker cannot edit |
| Standard | Delete step 4 AND renumber steps 5–6 AND fix counts — which check catches it? Then run the signed gate with `required_steps=5` | `required_steps=6` is held outside the trace; so are the signed receipts |
| Extension | Key rotation: steps 1–3 signed by key A, 4–6 by key B, with a schedule record | Gate must verify against the *scheduled* key |
| Extension | Partial verification with checkpoints (`verify_prefix`) | What does a partial proof mean downstream? |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: cryptography` | Deps not installed | Repo root: `make setup` |
| `ValueError: Key ID must start with 'DEMO_KEY_'` | You passed a non-demo key id | This is intentional — the demo refuses production-looking key names |
| `34 passed` fails after edits | Exercise changes | `git checkout -- student/ tests/ fixtures/` |
| Signature verification fails on your own package | You edited a receipt after signing, or set `signer_id` *after* signing (it is part of the signed payload) | Sign with `sign_receipt(key_manager, key_id, receipt)`, which does it in the right order |
| Merkle proof returns False unexpectedly | Leaves were modified after tree construction | Rebuild both from the same list |

---

## Safety Reminder

⚠️ **Teaching demonstration only.** `DEMO_KEY_*` keys are generated in memory per run and are **not production signing keys** — do not use them for real releases. No real PKI, certificates, or live traces. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
