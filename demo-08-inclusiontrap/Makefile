# Demo 08: InclusionTrap - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)
# Repo root on the import path so student scripts resolve this repo's shared/
# package even if another installed distribution provides a top-level `shared` module.
REPO_ROOT := $(abspath $(DEMO_DIR)/..)
export PYTHONPATH := $(REPO_ROOT)$(if $(PYTHONPATH),:$(PYTHONPATH))

.PHONY: help setup test demo clean

help:
	@echo "Demo 08: InclusionTrap"
	@echo ""
	@echo "  make setup    # Install deps"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run full demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-08-inclusiontrap..."
	@$(PYTHON) -m pip install -q -r ../requirements.txt 2>/dev/null || true
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete."

test:
	@echo "Running tests for demo-08..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 08: InclusionTrap ==="
	@echo ""
	@cd $(DEMO_DIR) && $(PYTHON) student/inclusiontrap.py
	@echo ""
	@echo "Generating results..."
	@cd $(DEMO_DIR) && $(PYTHON) student/generate_inclusion_results.py

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete