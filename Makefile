# PerturbGate — Makefile is the primary user interface.
# Every target also works as a plain command (shown in docs/REPRODUCIBILITY.md)
# for users without `make`.

PYTHON ?= python
export PYTHONPATH := src

.PHONY: help setup lint test demo reproduce full figures curated manifest verify \
        privacy-audit release-check clean

help:
	@echo "PerturbGate targets:"
	@echo "  make setup          install the package (+ dev tools) in editable mode"
	@echo "  make demo           Level 1: recompute headline reversal from compact inputs (minutes)"
	@echo "  make reproduce      Level 2: recompute robustness from public derived matrices"
	@echo "  make full           Level 3: reconstruct from open raw data (server-scale)"
	@echo "  make figures        regenerate all figures + source data"
	@echo "  make test           run the test suite"
	@echo "  make lint           run ruff"
	@echo "  make verify         checksums + schemas + golden values + tests + demo + figures + audit"
	@echo "  make privacy-audit  scan the whole repo for private/superseded/forbidden content"
	@echo "  make check-refs     DOI/PMID integrity check on the translational tables"
	@echo "  make release-check  everything required before public approval"

setup:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check src scripts tests

test:
	pytest

curated:
	$(PYTHON) scripts/build_curated_frozen.py

demo:
	$(PYTHON) -m perturbgate.cli demo

reproduce:
	$(PYTHON) -m perturbgate.cli reproduce

full:
	$(PYTHON) scripts/run_full_pipeline.py

figures:
	$(PYTHON) -m perturbgate.cli figures

manifest:
	$(PYTHON) -m perturbgate.cli manifest

# `make verify` is the composite gate: it regenerates the demo outputs and
# figures, rewrites the manifest, validates schemas/golden/claims/funnel/
# superseded labels, runs the tests, and scans for forbidden private terms.
verify: demo figures manifest
	$(PYTHON) -m perturbgate.cli verify
	pytest -q
	$(PYTHON) scripts/public_readiness_audit.py
	$(PYTHON) scripts/check_references.py

privacy-audit:
	$(PYTHON) scripts/public_readiness_audit.py

check-refs:
	$(PYTHON) scripts/check_references.py

release-check: lint verify
	@echo "release-check complete — review the audit report before public approval."

clean:
	rm -rf results/demo results/reproduced .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
