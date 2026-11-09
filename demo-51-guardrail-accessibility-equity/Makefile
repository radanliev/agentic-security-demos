# Demo 51: Guardrail Accessibility Equity - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 51: Guardrail Accessibility Equity"
	@echo ""
	@echo "  make setup    # Verify Python (stdlib only)"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run the equity audit over the synthetic scores"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-51-guardrail-accessibility-equity..."
	@$(PYTHON) --version
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete (standard library only)."

test:
	@echo "Running tests for demo-51..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 51: Guardrail Accessibility Equity ==="
	@echo ""
	@cd $(DEMO_DIR) && $(PYTHON) student/run_equity.py
	@echo ""
	@echo "Wrote results/guardrail_equity.json"

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/student/guardrail_equity/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete
