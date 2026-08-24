# Demo 05: EVIAssure — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md). Full course lab: [../docs/course/lab-05-eviassure.md](../../docs/course/lab-05-eviassure.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the 7-part demo | 3 min | `python3 student/eviassure.py` |
| Run the benchmark | 1 min | `python3 student/benchmark.py` |
| Hand-built chain experiment | 5 min | inline script (Step 4) |
| **Total** | **~15 min** | |

**Safety**: 100% offline. Keys are generated per-run and labeled `DEMO_KEY_*` — **never production signing keys**. Synthetic traces only. Requires the `cryptography` package (installed by `make setup`).

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

**Expected**: `14 passed`. Key tests: hash chain integrity, Merkle inclusion proofs, demo key signing (including refusal of non-`DEMO_KEY_` ids), tamper/omission/count detection, release blocked on incomplete evidence.

```
============================== 14 passed in 0.XXs ==============================
```

---

## Step 3 — Run the Full Demo (7 Sub-Demonstrations)

```bash
python3 student/eviassure.py
```

**What this does**: Runs all seven demonstrations in sequence.

**Expected output** (abbreviated):

```
1. Verifying complete trace...    PASS
2. Testing tamper detection...    (see note below)
3. Testing omission detection...  FAIL (step_count_mismatch)
4. Testing malformed closing...   FAIL (closing_count_mismatch)
5. Merkle proof for step 3:       VALID
6. Signed evidence:               PASS (or FAIL — see note)
7. Incomplete evidence:           FAIL (no_signed_receipts)
```

**⚠️ The most important observation in this demo** — sub-demo 2 (tamper): the gate may report the *tampered* trace as PASS. Read the printed reason carefully. This is **not a bug**: `verify_trace` rebuilds the chain from the file's own contents, so a *self-consistent* forged chain verifies. A hash chain proves events are consistent *with each other* — it does not prove they are the events that originally happened. Binding to reality requires the **signatures** (sub-demo 6). Record this lesson in your notes.

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

**What this does**: Builds chains of 10/50/100/500 receipts and times full Merkle verification of every leaf.

**Expected output** (times vary by machine — record yours):

```
trace_size 10   -> ~0.04 ms
trace_size 50   -> ~0.18 ms
trace_size 100  -> ~0.40 ms
trace_size 500  -> ~2.5  ms
```

**Record your times** in the reproducibility table — they will differ from another participant's machine, which is itself a reproducibility lesson (timing is environment-dependent; verdicts are not).

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
| Tests passed | | `14 passed` |
| Complete trace verdict | | PASS (Step 3.1) |
| Omission verdict | | FAIL, `step_count_mismatch` (Step 3.3) |
| Bad count verdict | | FAIL, `closing_count_mismatch` (Step 3.4) |
| Merkle proof | | VALID (Step 3.5) |
| Incomplete evidence | | FAIL, `no_signed_receipts` (Step 3.7) |
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
| Standard | External anchor: publish the Merkle root to a separate file; verify against it; defeat the self-consistent forgery from Step 3 | The verifier needs an expectation the attacker cannot edit |
| Standard | Delete step 4 AND renumber steps 5–6 AND fix counts — which check catches it? | `required_steps=6` is held outside the trace |
| Extension | Key rotation: steps 1–3 signed by key A, 4–6 by key B, with a schedule record | Gate must verify against the *scheduled* key |
| Extension | Partial verification with checkpoints (`verify_prefix`) | What does a partial proof mean downstream? |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: cryptography` | Deps not installed | Repo root: `make setup` |
| `ValueError: Key ID must start with 'DEMO_KEY_'` | You passed a non-demo key id | This is intentional — the demo refuses production-looking key names |
| `14 passed` fails after edits | Exercise changes | `git checkout -- student/ tests/ fixtures/` |
| Signature verification fails on your own package | You edited a receipt after signing | Re-sign: re-run the Step in `student/eviassure.py` main |
| Merkle proof returns False unexpectedly | Leaves were modified after tree construction | Rebuild both from the same list |

---

## Safety Reminder

⚠️ **Teaching demonstration only.** `DEMO_KEY_*` keys are generated per-run and are **not production signing keys** — do not use them for real releases. No real PKI, certificates, or live traces. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
