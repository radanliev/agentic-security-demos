# Demo 03: Evaluation Invariants - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 03: Evaluation Invariants"
	@echo ""
	@echo "  make setup    # Install deps"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run full demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-03-eval-invariants..."
	@$(PYTHON) -m pip install -q -r ../requirements.txt 2>/dev/null || true
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete."

test:
	@echo "Running tests for demo-03..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 03: Evaluation Invariants ==="
	@echo ""
	@echo "Running all five invariants on synthetic evaluation data..."
	@cd $(DEMO_DIR) && $(PYTHON) student/eval_invariants.py
	@echo ""
	@echo "Generating summary table..."
	@cd $(DEMO_DIR) && $(PYTHON) student/generate_summary.py

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete