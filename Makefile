# Root Makefile for agentic-security-demos
# Provides unified commands across all demos

SHELL := /bin/bash
PYTHON := python3
DEMO_DIRS := demo-01-blind-verification demo-02-supply-chain-aibom demo-03-eval-invariants demo-04-authoritybound demo-05-eviassure demo-06-reconscope demo-07-triagetrap demo-08-inclusiontrap demo-09-interceptbound demo-10-scanbound demo-11-degenerate-reporting

.PHONY: help setup test demo clean all-demos verify-safety

help:
	@echo "Agentic Security Demos - Root Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup              # Install deps, generate fixtures for all demos"
	@echo ""
	@echo "Testing:"
	@echo "  make test               # Run tests for all demos"
	@echo "  make test DEMO=01       # Run tests for specific demo"
	@echo ""
	@echo "Demonstrations:"
	@echo "  make demo DEMO=01       # Run demo 01 (blind-verification)"
	@echo "  make demo DEMO=02       # Run demo 02 (supply-chain-aibom)"
	@echo "  ...                     # DEMO=03 through DEMO=11"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean              # Remove generated files, caches, results"
	@echo "  make verify-safety      # Check for safety violations"
	@echo "  make all-demos          # Run all demos sequentially"
	@echo ""

setup:
	@echo "=== Setting up all demos ==="
	@for d in $(DEMO_DIRS); do \
		if [ -f $$d/Makefile ]; then \
			echo "--- Setting up $$d ---"; \
			$(MAKE) -C $$d setup PYTHON="$(PYTHON)" || exit 1; \
		else \
			echo "WARNING: $$d/Makefile not found, skipping"; \
		fi \
	done
	@echo "=== Setup complete ==="

test:
ifdef DEMO
	@echo "=== Testing demo-$(DEMO) ==="
	@$(MAKE) -C demo-$(DEMO)-* test PYTHON="$(PYTHON)"
else
	@echo "=== Testing all demos ==="
	@for d in $(DEMO_DIRS); do \
		if [ -f $$d/Makefile ]; then \
			echo "--- Testing $$d ---"; \
			$(MAKE) -C $$d test PYTHON="$(PYTHON)" || exit 1; \
		fi \
	done
	@echo "=== Testing shared library ==="
	@$(PYTHON) -m pytest tests/test_shared.py -v || exit 1;
	@echo "=== All tests passed ==="
endif

demo:
ifndef DEMO
	$(error DEMO is required. Usage: make demo DEMO=01)
endif
	@echo "=== Running demo-$(DEMO) ==="
	@$(MAKE) -C demo-$(DEMO)-* demo PYTHON="$(PYTHON)"

clean:
	@echo "=== Cleaning all demos ==="
	@for d in $(DEMO_DIRS); do \
		if [ -f $$d/Makefile ]; then \
			$(MAKE) -C $$d clean PYTHON="$(PYTHON)"; \
		fi \
	done
	@rm -rf __pycache__ .pytest_cache .coverage htmlcov dist build *.egg-info
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "=== Clean complete ==="

verify-safety:
	@echo "=== Verifying safety constraints ==="
	@echo "Checking for network imports in test files..."
	@! grep -r "^import socket\|^import requests\|^import urllib\|^from urllib\|^import http.client\|^import aiohttp\|^import httpx" --include="*test*.py" demo-*/ 2>/dev/null || (echo "FAIL: Network imports found" && exit 1)
	@echo "Checking for credentials..."
	@! grep -r "sk-\|ghp_\|gho_\|ghu_\|ghs_\|github_pat_\|aws_access_key\|AWS_SECRET\|BEGIN PRIVATE\|-----BEGIN" --include="*.py" --include="*.json" demo-*/ 2>/dev/null | grep -v "task-00" || (echo "FAIL: Credentials found" && exit 1)
	@echo "Checking for external URLs in tests..."
	@! grep -r "http://\|https://" --include="*test*.py" demo-*/ 2>/dev/null | grep -v "example.com\|localhost\|127.0.0.1\|0.0.0.0" || (echo "FAIL: External URLs in tests" && exit 1)
	@echo "Checking for network imports in student modules and shared/..."
	@# shared/reproducibility.py imports socket only to disable it (enforce_offline); it is excluded by name.
	@! grep -r "^import socket\|^from socket\|^import requests\|^from requests\|^import urllib$$\|^import urllib\.request\|^from urllib\.request\|^from urllib import request\|^import http\.client\|^from http import client\|^import aiohttp\|^import httpx" --include="*.py" --exclude=reproducibility.py demo-*/student/ shared/ 2>/dev/null || (echo "FAIL: Network imports found in runtime code" && exit 1)
	@echo "=== Safety verification passed ==="

all-demos:
	@for d in $(DEMO_DIRS); do \
		if [ -f $$d/Makefile ]; then \
			echo "=== Running $$d ==="; \
			$(MAKE) -C $$d demo PYTHON="$(PYTHON)" || exit 1; \
		fi \
	done

# Individual demo targets for convenience
demo-01: ; @$(MAKE) demo DEMO=01
demo-02: ; @$(MAKE) demo DEMO=02
demo-03: ; @$(MAKE) demo DEMO=03
demo-04: ; @$(MAKE) demo DEMO=04
demo-05: ; @$(MAKE) demo DEMO=05
demo-06: ; @$(MAKE) demo DEMO=06
demo-07: ; @$(MAKE) demo DEMO=07
demo-08: ; @$(MAKE) demo DEMO=08
demo-09: ; @$(MAKE) demo DEMO=09
demo-10: ; @$(MAKE) demo DEMO=10