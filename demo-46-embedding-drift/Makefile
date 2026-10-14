SHELL := /bin/bash
PYTHON := python3
DEMO_DIR := $(CURDIR)

.PHONY: help setup test demo clean

help:
	@echo "Demo 46: Embedding-swap cosine shift"

setup:
	@$(PYTHON) --version
	@mkdir -p $(DEMO_DIR)/results

test:
	@cd $(DEMO_DIR) && $(PYTHON) -m pytest tests/ -v --tb=short

demo: setup
	@cd $(DEMO_DIR) && $(PYTHON) student/run_drift.py

clean:
	@rm -rf $(DEMO_DIR)/results $(DEMO_DIR)/__pycache__ $(DEMO_DIR)/student/__pycache__ $(DEMO_DIR)/tests/__pycache__
