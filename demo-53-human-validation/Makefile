# Demo 53: Human Validation of Agent Outputs - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 53: Human Validation of Agent Outputs"
	@echo ""
	@echo "  make setup    # Verify Python (stdlib only)"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run the demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-53-human-validation..."
	@$(PYTHON) --version
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete (standard library only)."

test:
	@echo "Running tests for demo-53..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 53: Human Validation of Agent Outputs ==="
	@echo ""
	@cd $(DEMO_DIR) && $(PYTHON) student/run_validate.py
	@echo ""
	@echo "Wrote results/validation.json"

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete
