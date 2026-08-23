# Code Style Guide

## Python Style

### Formatting

- **Line length**: 100 characters (ruff default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Trailing commas**: Yes, in multi-line structures

```python
# Good
config = {
    "allowed_hosts": ["localhost", "127.0.0.1"],
    "allowed_ports": [80, 443],
}
```

### Type Hints

**Required** for all public functions (mypy strict mode).

```python
# Good
def validate_target(target: Target, scope: ScopePolicy) -> tuple[bool, str]:
    """Validate target against scope policy."""
    ...

# Bad
def validate(target, scope):  # No types
    ...
```

### Imports

```python
# Standard library first
import json
import hashlib
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Third party
import pytest
import yaml

# Local
from shared.result_schema import ResultRecord
from .models import Target, ScopePolicy
```

### Naming

| Type | Convention | Example |
|------|------------|---------|
| Functions/Variables | snake_case | `validate_target` |
| Classes | PascalCase | `ScopePolicy` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Enums | PascalCase | `TaintLevel` |
| Type variables | PascalCase + T | `T = TypeVar("T")` |

### Docstrings (Google Style)

```python
def process_artifact(artifact: Artifact, config: Config) -> TriageResult:
    """Process artifact through triage pipeline.
    
    Args:
        artifact: The artifact to triage.
        config: Triage configuration with thresholds.
        
    Returns:
        TriageResult with verdict, score, and reasons.
        
    Raises:
        ValueError: If artifact is missing required fields.
        
    Example:
        >>> result = process_artifact(artifact, config)
        >>> result.verdict
        Verdict.QUARANTINE
    """
```

## Testing Style

### Test Naming

```python
# Good
def test_guarded_agent_blocks_injection(self, files, scope, data):
    ...

def test_scope_escalation_blocked(self, frames, scope, buffer_config):
    ...

# Bad
def test_1(self):
    ...

def test_injection(self):
    ...
```

### Fixtures

```python
@pytest.fixture
def sample_artifact(self):
    """Create a sample artifact for testing."""
    return Artifact(
        id="test-001",
        type="pcap_metadata",
        source="network_tap_eth0",
        provenance=Provenance.TRUSTED_SENSOR,
        metadata={"src_ip": "192.168.1.1"},
        canary="CANARY_BENIGN_TEST"
    )
```

### Assertions

```python
# Good - descriptive
assert result.verdict == Verdict.QUARANTINE, f"Expected QUARANTINE, got {result.verdict}"
assert "injection_detected" in result.reasons

# Bad
assert result.verdict == Verdict.QUARANTINE
assert result.reasons
```

## Documentation Style

### README Sections (Required)

1. **Learning Objectives** — Bullet list
2. **Conceptual Explanation** — 2-3 paragraphs
3. **Safety Notice** — ⚠️ box with guarantees
4. **Running the Demo** — Code block with commands
5. **Scenarios/Fixtures** — Table format
5. **Exercises** — Beginner/Standard/Extension
6. **Key Files** — Table with purposes
7. **Difference from Private Research** — Table

### Code Comments

```python
# Good - explains WHY
# Use hash chain to detect tampering: any modification breaks the chain
prev_hash = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()

# Bad - explains WHAT
# Set prev_hash to genesis or previous hash
prev_hash = chain.genesis if i == 0 else chain.receipts[-1].compute_hash()
```

## Commit Messages

```
feat(demo-03): add saturation detection invariant
fix(demo-07): handle label contamination in sandbox verdict
docs(demo-04): clarify provenance label semantics
test(demo-01): add false positive exercise
refactor(shared): extract result schema to module
```

Format: `type(scope): description`

| Type | Description |
|------|-------------|
| `feat` | New feature/exercise |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Test addition/fix |
| `refactor` | Code restructuring |
| `style` | Formatting only |
| `safety` | Safety improvement |
| `chore` | Maintenance |