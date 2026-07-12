#!/usr/bin/env python3
"""Level 3 orchestration (server-scale, open-data reconstruction).

This is the honest Level-3 driver. Full raw-data reconstruction requires the
genome-scale effect-vector substrate and the JIA h5ad, plus a high-memory server.
Rather than pretend a laptop can do this, the script:

  1. checks whether the open inputs / configured server roots are available;
  2. if they are, regenerates the frozen artifacts via scripts/build_public_inputs.py
     (the same anonymised transform used to build the release);
  3. otherwise prints exactly what is needed and points to the download helper.

No internal path, credential, or cluster name is used; configure the server roots
via environment variables (see configs/full.yaml).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    roots = {k: os.environ.get(k) for k in ("SERVER_RESULTS_ROOT", "SERVER_INPUTS_ROOT", "SERVER_DATA_ROOT")}
    have = all(roots.values()) and all(Path(v).exists() for v in roots.values() if v)
    print("PerturbGate — Level 3 (full open-data reconstruction)\n")
    if not have:
        print("Level-3 reconstruction inputs are not configured on this machine.\n")
        print("What Level 3 needs (see configs/full.yaml, docs/REPRODUCIBILITY_LEVELS.md):")
        print("  1. Download the open data:      python scripts/download_open_data.py --execute")
        print("  2. Rebuild the disease vector, genome-scale effect vectors and functional table")
        print("     on a high-memory server (~128 GB RAM, several hours).")
        print("  3. Point these environment variables at the outputs and re-run:")
        for k in roots:
            print(f"       {k}")
        print("  4. python scripts/build_public_inputs.py   # regenerate frozen artifacts")
        print("     python -m perturbgate.cli verify         # confirm reproduction matches frozen")
        print("\nLevels 1 (make demo) and 2 (make reproduce) are the honest, laptop-scale")
        print("reproducibility guarantees and do not require any of the above.")
        return 0
    print("Server roots configured — regenerating frozen artifacts from open-data reconstruction ...")
    subprocess.run([sys.executable, str(REPO / "scripts" / "build_public_inputs.py")], check=True, cwd=REPO)
    subprocess.run([sys.executable, str(REPO / "scripts" / "build_curated_frozen.py")], check=True, cwd=REPO)
    subprocess.run([sys.executable, "-m", "perturbgate.cli", "verify"], check=True, cwd=REPO,
                   env={**os.environ, "PYTHONPATH": "src"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
