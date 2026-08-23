# Demo 10: ScanBound - Makefile

SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 10: ScanBound"
	@echo ""
	@echo "  make setup    # Install deps"
	@echo "  make test     # Run all tests"
	@echo "  make demo     # Run full demonstration"
	@echo "  make clean    # Remove generated files"

setup:
	@echo "Setting up demo-10-scanbound..."
	@$(PYTHON) -m pip install -q -r ../../requirements.txt 2>/dev/null || true
	@mkdir -p $(DEMO_DIR)/results
	@echo "Setup complete."

test:
	@echo "Running tests for demo-10..."
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@echo "=== Demo 10: ScanBound ==="
	@echo ""
	@cd $(DEMO_DIR) && $(PYTHON) student/scanbound.py
	@echo ""
	@echo "Generating results..."
	@cd $(DEMO_DIR) && $(PYTHON) student/generate_scan_results.py

clean:
	@rm -rf $(DEMO_DIR)/results/
	@rm -rf $(DEMO_DIR)/__pycache__
	@rm -rf $(DEMO_DIR)/student/__pycache__
	@rm -rf $(DEMO_DIR)/tests/__pycache__
	@find $(DEMO_DIR) -name "*.pyc" -delete