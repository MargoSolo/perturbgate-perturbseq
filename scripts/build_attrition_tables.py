#!/usr/bin/env python3
"""(Re)build the candidate-attrition artifacts: candidate_funnel.tsv, gate_matrix.tsv,
gate_ablation.tsv (curated), and — from the private substrate, when configured —
all_perturbations_authoritative_reversal.tsv and rejection_ledger.tsv.

The screen-level tables are produced by scripts/build_public_inputs.py (needs the
server roots); the curated attrition tables are produced by
scripts/build_curated_frozen.py (runs anywhere). This wrapper runs the curated
builder so the funnel/gate tables are regenerated deterministically.
"""
import runpy
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    print("Rebuilding curated attrition tables (funnel, gate matrix, gate ablation) ...")
    runpy.run_path(str(REPO / "scripts" / "build_curated_frozen.py"), run_name="__main__")
    print("Screen-level all_perturbations + rejection_ledger require the server substrate:")
    print("  python scripts/build_public_inputs.py  (with SERVER_* env vars set)")
    sys.exit(0)
