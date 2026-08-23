# Demo 02: Supply-Chain AIBOM Drift - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 02: Supply-Chain AIBOM Drift"
	@echo ""
	@echo "  make setup    # Install deps"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run full demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-02-supply-chain-aibom..."
	@$(PYTHON) -m pip install -q -r ../../requirements.txt 2>/dev/null || true
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete."

test:
	@echo "Running tests for demo-02..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 02: Supply-Chain AIBOM Drift ==="
	@echo ""
	@echo "Running policy gate on all drift scenarios..."
	@cd $(DEMO_DIR) && $(PYTHON) student/policy_gate.py
	@echo ""
	@echo "Running GitHub Actions validation script..."
	@cd $(DEMO_DIR) && $(PYTHON) student/validate_aibom.py
	@echo "Exit code: $$?"
	@echo ""
	@echo "Generating JSON results..."
	@cd $(DEMO_DIR) && $(PYTHON) student/generate_results.py

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete