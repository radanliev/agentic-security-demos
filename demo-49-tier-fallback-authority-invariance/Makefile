# Demo 49: Authority Invariance under Model Fallback - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 49: Authority Invariance under Model Fallback"
	@echo ""
	@echo "  make setup    # Verify Python (stdlib only)"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run the checker over the synthetic traces"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-49-tier-fallback-authority-invariance..."
	@$(PYTHON) --version
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete (standard library only)."

test:
	@echo "Running tests for demo-49..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 49: Authority Invariance under Model Fallback ==="
	@echo ""
	@cd $(DEMO_DIR) && $(PYTHON) student/run_tiers.py
	@echo ""
	@echo "Wrote results/tier_invariance.json"

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/student/tier_invariance/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete
