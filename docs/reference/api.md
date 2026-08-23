# API Reference

## Shared Utilities

### `shared.result_schema`

```python
from shared.result_schema import ResultRecord, write_result, read_results

# Create and save result
record = write_result(
    demo="demo-01-blind-verification",
    experiment="my_experiment",
    seed=42,
    result="pass",
    notes="Custom experiment",
    command="make demo DEMO=01",
    duration_ms=123,
    metadata={"custom": "data"}
)

# Load results
records = read_results("demo-01-blind-verification", "results/")
```

### `shared.reproducibility`

```python
from shared.reproducibility import (
    generate_seed, deterministic_shuffle, set_global_seed,
    capture_environment, format_command, verify_offline
)

# Generate deterministic seed
seed = generate_seed("my-experiment")

# Shuffle deterministically
items = deterministic_shuffle(["a", "b", "c"], seed=42)

# Set global seeds
set_global_seed(42)

# Capture environment
env = capture_environment()  # "Python 3.11, Linux 5.15.0"

# Format command
cmd = format_command("01", "comparison")  # "make demo DEMO=01 EXPERIMENT=comparison"
```

### `shared.fixtures`

```python
from shared.fixtures import (
    write_fixture, read_fixture, generate_canary,
    generate_fake_hash, generate_fake_package_name,
    make_deterministic_dict
)

# Write fixture with seed comment
write_fixture({"key": "value"}, Path("fixtures/data.json"), seed=42)

# Read fixture (strips seed comment)
data = read_fixture(Path("fixtures/data.json"))

# Generate deterministic identifiers
canary = generate_canary("TEST", seed=42)      # "TEST_A1B2C3D4E5F6G7H8"
fake_hash = generate_fake_hash(seed=42)        # 64-char hex
pkg_name = generate_fake_package_name(seed=42) # "secure-parser-123"
```

## Demo-Specific Modules

### Demo 01: Blind Verification

```python
from student.baseline_agent import BaselineAgent
from student.verified_agent import VerifiedAgent
from student.oracle_evaluator import OracleEvaluator

# Baseline (cheats)
agent = BaselineAgent(Path("fixtures/scenarios.json"), Path("fixtures/sealed_oracles.json"))
result = agent.solve("authz-001")

# Verified (blind)
agent = VerifiedAgent(Path("fixtures/scenarios.json"))
result = agent.solve("authz-001")

# Evaluate
evaluator = OracleEvaluator(Path("fixtures/sealed_oracles.json"))
results = evaluator.evaluate_all(commitments)
```

### Demo 02: AIBOM Drift

```python
from student.policy_gate import PolicyGate, Waiver

gate = PolicyGate(Path("fixtures/aibom.json"))
result = gate.evaluate_system(capabilities, waiver=None)
```

### Demo 04: Authority Bound

```python
from student.authoritybound import (
    create_baseline_agent, create_provenance_aware_agent,
    Provenance, Tool
)

agent = create_provenance_aware_agent()
result = agent.process("Read file config.yaml", Provenance.USER_DATA)
```

### Demo 05: EVIAssure

```python
from student.eviassure import (
    HashChain, MerkleTree, WitnessReceipt,
    DemoKeyManager, ReleaseGate
)

chain = HashChain()
receipt = WitnessReceipt(step=1, action="init", data_hash="...", prev_hash="0"*64, timestamp="...")
chain.add_receipt(receipt)

key_manager = DemoKeyManager()
key = key_manager.generate_key("DEMO_KEY_RELEASE_001")
```

### Demo 06: ReconScope

```python
from student.reconscope import (
    ProtocolParser, ScopePolicy,
    ProvenanceAwareReconAgent
)

parser = ProtocolParser()
fields = parser.parse(fixture)  # Returns ParsedField list with provenance

scope = ScopePolicy(allowed_hosts, allowed_ports, denied_patterns)
agent = ProvenanceAwareReconAgent(scope)
observations = agent.probe(fixture)
```

### Demo 07: TriageTrap

```python
from student.triagetrap import (
    ProvenanceAwareTriageAgent, Artifact, Provenance, Verdict
)

agent = ProvenanceAwareTriageAgent(base_rates, threshold)
artifact = Artifact(id="art-001", type="pcap_metadata", ...)
result = agent.triage(artifact)
```

### Demo 08: InclusionTrap

```python
from student.inclusiontrap import (
    GuardedInclusionAgent, ScopePolicy, Provenance
)

scope = ScopePolicy(allowed_paths, denied_paths)
agent = GuardedInclusionAgent(files, scope)
result = agent.process(scenario)
```

### Demo 09: InterceptBound

```python
from student.interceptbound import (
    TaintAwareAgent, TaintTracker, EphemeralBuffer, ActionGuard
)

agent = TaintAwareAgent(scope_policy, buffer_config)
result = agent.process(frame)
```

### Demo 10: ScanBound

```python
from student.scanbound import (
    ScopeBoundScanner, ScopeValidator, CheckValidator,
    TaintTracker, ActionPolicy, Target, ScannerCheck
)

scanner = ScopeBoundScanner(scope, validator, taint_tracker, policy)
result = scanner.run(checks, scanner_output)
```

## Result Classes

All demos use standardized result creation:

```python
from shared.result_schema import write_result

record = write_result(
    demo="demo-XX-name",
    experiment="experiment-name",
    seed=42,
    result="pass",
    notes="Synthetic teaching fixture",
    command="make demo DEMO=XX",
    duration_ms=123,
    metadata={"key": "value"}
)
record.save(Path("results/output.json"))
```