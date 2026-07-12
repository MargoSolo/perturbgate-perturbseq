#!/usr/bin/env python3
"""(Re)build the claim and superseded-claim registries (claims.json,
superseded_claims.json, analysis_contract.json) and verify that every claim
resolves to an on-disk supporting artifact."""
import runpy
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

if __name__ == "__main__":
    runpy.run_path(str(REPO / "scripts" / "build_curated_frozen.py"), run_name="__main__")
    from targetgate.claim_ledger import load_claims, resolve_claims
    problems = resolve_claims(load_claims())
    if problems:
        print("\nUNRESOLVED CLAIMS:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("\nAll claims resolve to on-disk artifacts.")
    sys.exit(0)
