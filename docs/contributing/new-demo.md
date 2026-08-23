# Adding a New Demo

## Overview

Each demo follows a consistent structure. This guide walks through creating demo-XX.

## Step 1: Create Directory Structure

```bash
mkdir -p demo-XX-name/{fixtures,student,tests,results}
```

## Step 2: Create Fixtures

### `fixtures/data.json`

```json
{
  "scenarios": [
    {
      "id": "scenario-001",
      "description": "Description",
      "input": "input data",
      "expected": "expected output"
    }
  ],
  "policy": {
    "allowed": ["item1", "item2"],
    "denied": ["item3"]
  },
  "seed": 42
}
```

**Rules:**
- ✅ Synthetic data only
- ✅ No real credentials, IPs, hostnames
- ✅ Seed field for reproducibility
- ❌ No real API keys, passwords, tokens

## Step 3: Create Student Code

### `student/module.py`

```python
"""Module docstring explaining purpose."""

from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import json

@dataclass
class MyConfig:
    """Configuration for X."""
    allowed: List[str]
    denied: List[str]

class MyAgent:
    """Agent that does X."""
    
    def __init__(self, config: MyConfig):
        self.config = config
    
    def process(self, input_data: str) -> dict:
        """Process input and return result."""
        # TODO: Implement logic
        return {"status": "not_implemented"}

def main():
    """Run demo."""
    data = json.loads(Path("fixtures/data.json").read_text())
    config = MyConfig(**data["policy"])
    agent = MyAgent(config)
    
    for scenario in data["scenarios"]:
        result = agent.process(scenario["input"])
        print(f"{scenario['id']}: {result}")

if __name__ == "__main__":
    main()
```

### `student/generate_results.py`

```python
"""Generate standardized JSON results for demo."""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from module import MyAgent, MyConfig

def main():
    data = json.loads(Path("fixtures/data.json").read_text())
    config = MyConfig(**data["policy"])
    agent = MyAgent(config)
    
    results = []
    for scenario in data["scenarios"]:
        result = agent.process(scenario["input"])
        results.append({
            "scenario": scenario["id"],
            "result": result
        })
    
    output = {
        "demo": "demo-XX-name",
        "experiment": "main",
        "seed": 42,
        "commit": "local",
        "environment": "test",
        "command": "make demo DEMO=XX",
        "result": "pass",
        "notes": "Synthetic teaching fixture",
        "results": results
    }
    
    Path("results/results.json").parent.mkdir(exist_ok=True)
    Path("results/results.json").write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
```

## Step 4: Create Tests

### `tests/test_module.py`

```python
"""Tests for Demo XX."""

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "student"))
from module import MyAgent, MyConfig

class TestDemoXX:
    """Tests for demo XX functionality."""
    
    @pytest.fixture
    def data(self):
        return json.loads(Path("fixtures/data.json").read_text())
    
    @pytest.fixture
    def agent(self, data):
        config = MyConfig(**data["policy"])
        return MyAgent(config)
    
    def test_basic_functionality(self, agent, data):
        """Test basic scenario."""
        scenario = data["scenarios"][0]
        result = agent.process(scenario["input"])
        assert result["status"] == "expected"
    
    def test_safety_no_network(self):
        """Verify no network imports in student code."""
        source = Path("student/module.py").read_text()
        assert "import socket" not in source
        assert "import requests" not in source
        assert "import urllib" not in source

class TestExercises:
    """Exercise validation tests."""
    
    def test_exercise_beginner(self):
        """Exercise: Add new scenario to fixtures."""
        data = json.loads(Path("fixtures/data.json").read_text())
        assert len(data["scenarios"]) >= 1
    
    def test_exercise_standard(self):
        """Exercise: Implement feature X."""
        pass  # Student implements
    
    def test_exercise_extension(self):
        """Exercise: Extend with feature Y."""
        pass  # Student implements

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Step 5: Create Makefile

### `Makefile`

```makefile
SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo XX: Name"
	@echo ""
	@echo "  make setup    # Install deps"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run full demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-XX-name..."
	@$(PYTHON) -m pip install -q -r ../../requirements.txt 2>/dev/null || true
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete."

test:
	@echo "Running tests for demo-XX..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo XX: Name ==="
	@cd $(DEMO_DIR) && $(PYTHON) student/module.py
	@echo ""
	@echo "Generating results..."
	@cd $(DEMO_DIR) && $(PYTHON) student/generate_results.py

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete
```

## Step 6: Register in Root

### Root `Makefile`

Add to `DEMO_DIRS`:

```makefile
DEMO_DIRS := demo-01-blind-verification demo-02-supply-chain-aibom \
             demo-03-eval-invariants demo-04-authoritybound \
             demo-05-eviassure demo-06-reconscope \
             demo-07-triagetrap demo-08-inclusiontrap \
             demo-09-interceptbound demo-10-scanbound \
             demo-XX-name
```

### `.github/workflows/ci.yml`

Add test job:

```yaml
- name: Test demo-XX-name
  run: |
    cd demo-XX-name
    make test
```

## Step 6: Update Root README

Add to demo table:

| XX | [Name](demos/XX-name.md) | Description | Key Concepts | Difficulty |

## Step 7: Verify

```bash
# From root
make setup
make test DEMO=XX
make demo DEMO=XX
make verify-safety
```

## Checklist

- [ ] `fixtures/data.json` with synthetic data + seed
- [ ] `student/module.py` with type hints, docstrings
- [ ] `student/generate_results.py` with standardized schema
- [ ] `tests/test_module.py` with beginner/standard/extension tests
- [ ] `Makefile` with setup/test/demo/clean
- [ ] `README.md` with objectives, safety notice, reproducibility
- [ ] Registered in root Makefile
- [ ] CI entry added
- [ ] Root README updated
- [ ] `make test` passes
- [ ] `make verify-safety` passes
- [ ] `make demo DEMO=XX` works

---

*Follow this pattern for consistency across all demos.*