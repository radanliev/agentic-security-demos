# Demo 01: Blind Verification - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 01: Blind Verification"
	@echo ""
	@echo "  make setup    # Install deps, generate fixtures"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run full demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-01-blind-verification..."
	@$(PYTHON) -m pip install -q -r ../../requirements.txt 2>/dev/null || true
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete."

test:
	@echo "Running tests for demo-01..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 01: Blind Verification ==="
	@echo ""
	@echo "Step 1: Run baseline agent (cheats by reading oracle)"
	@cd $(DEMO_DIR) && $(PYTHON) student/baseline_agent.py
	@echo ""
	@echo "Step 2: Run verified agent (blind commitment)"
	@cd $(DEMO_DIR) && $(PYTHON) student/verified_agent.py
	@echo ""
	@echo "Step 3: Evaluate both against sealed oracles"
	@cd $(DEMO_DIR) && $(PYTHON) student/oracle_evaluator.py --commitments commitments_baseline.json --output results/baseline_eval.json
	@cd $(DEMO_DIR) && $(PYTHON) student/oracle_evaluator.py --commitments commitments_verified.json --output results/verified_eval.json
	@echo ""
	@echo "Step 4: Generate comparison table"
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/test_blind_verification.py::TestComparisonTable::test_generate_comparison -v
	@echo ""
	@echo "Results:"
	@cat $(DEMO_DIR)/results/comparison_table.json | $(PYTHON) -m json.tool

clean:
	@rm -f $(DEMO_DIR)/commitments_*.json
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete