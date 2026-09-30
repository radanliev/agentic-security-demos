# Root Makefile for agentic-security-demos
# Provides unified commands across all demos

SHELL := /bin/bash
PYTHON := python3
DEMO_DIRS := demo-01-blind-verification demo-02-supply-chain-aibom demo-03-eval-invariants demo-04-authoritybound demo-05-eviassure demo-06-reconscope demo-07-triagetrap demo-08-inclusiontrap demo-09-interceptbound demo-10-scanbound demo-11-degenerate-reporting demo-12-provenancebound demo-13-typed-commitments demo-14-conformal-gating demo-15-hijack-probes demo-16-infection-spread demo-17-report-fidelity demo-18-crosslingual-gap demo-19-lineage-risk demo-20-agent-web-census demo-21-mcp-ecosystem demo-22-memory-leakage demo-23-fault-injection demo-24-delegation-checks demo-25-attestation-verifier demo-26-sandbox-probes demo-27-ci-trigger-scan demo-28-memory-poisoning demo-29-provenance-graphs demo-30-default-configs demo-31-scope-creep demo-32-reproducibility-audit demo-33-protocol-coverage demo-34-visual-injection demo-35-scaling-metaregression demo-36-card-debt demo-37-detector-cost demo-38-assurance-claims demo-39-incident-taxonomy demo-40-corpus-union demo-41-ten-invariants demo-42-patch-lifecycle demo-43-terms-coding demo-44-toolflow-taint

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
	@echo "  ...                     # DEMO=03 through DEMO=44"
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
demo-11: ; @$(MAKE) demo DEMO=11
demo-12: ; @$(MAKE) demo DEMO=12
demo-13: ; @$(MAKE) demo DEMO=13
demo-14: ; @$(MAKE) demo DEMO=14
demo-15: ; @$(MAKE) demo DEMO=15
demo-16: ; @$(MAKE) demo DEMO=16
demo-17: ; @$(MAKE) demo DEMO=17
demo-18: ; @$(MAKE) demo DEMO=18
demo-19: ; @$(MAKE) demo DEMO=19
demo-20: ; @$(MAKE) demo DEMO=20
demo-21: ; @$(MAKE) demo DEMO=21
demo-22: ; @$(MAKE) demo DEMO=22
demo-23: ; @$(MAKE) demo DEMO=23
demo-24: ; @$(MAKE) demo DEMO=24
demo-25: ; @$(MAKE) demo DEMO=25
demo-26: ; @$(MAKE) demo DEMO=26
demo-27: ; @$(MAKE) demo DEMO=27
demo-28: ; @$(MAKE) demo DEMO=28
demo-29: ; @$(MAKE) demo DEMO=29
demo-30: ; @$(MAKE) demo DEMO=30
demo-31: ; @$(MAKE) demo DEMO=31
demo-32: ; @$(MAKE) demo DEMO=32
demo-33: ; @$(MAKE) demo DEMO=33
demo-34: ; @$(MAKE) demo DEMO=34
demo-35: ; @$(MAKE) demo DEMO=35
demo-36: ; @$(MAKE) demo DEMO=36
demo-37: ; @$(MAKE) demo DEMO=37
demo-38: ; @$(MAKE) demo DEMO=38
demo-39: ; @$(MAKE) demo DEMO=39
demo-40: ; @$(MAKE) demo DEMO=40
demo-41: ; @$(MAKE) demo DEMO=41
demo-42: ; @$(MAKE) demo DEMO=42
demo-43: ; @$(MAKE) demo DEMO=43
demo-44: ; @$(MAKE) demo DEMO=44