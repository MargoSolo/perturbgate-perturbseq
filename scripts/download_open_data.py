#!/usr/bin/env python3
"""Open-data download helper (Level 3).

Prints the exact, verified public download routes for the two open datasets and
(optionally, with --execute) downloads the compact ones. Large single-cell
objects are NOT downloaded automatically: the command is printed so the user can
run it deliberately. Nothing here uses a private connector, credential, or
internal path.

Datasets and licenses: docs/DATA_AVAILABILITY.md, docs/DATA_LICENSES.md.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FULL = REPO / "data" / "full"

ROUTES = {
    "jia_disease_h5ad": dict(
        title="JIA synovial atlas — Integrated global cells (CC-BY-4.0)",
        url="https://datasets.cellxgene.cziscience.com/f758894c-14bc-4bfe-94dd-16dd9945f7d3.h5ad",
        doi="10.64898/2026.05.01.716870",
        cmd="curl -L -o data/full/jia_synovial_integrated.h5ad "
            "https://datasets.cellxgene.cziscience.com/f758894c-14bc-4bfe-94dd-16dd9945f7d3.h5ad",
        note="~1-2 GB; registration not required.",
    ),
    "perturbseq_processed": dict(
        title="Primary Human CD4+ T Cell Perturb-seq — processed (MIT)",
        url="s3://genome-scale-tcell-perturb-seq/marson2025_data/",
        doi="10.64898/2025.12.23.696273",
        cmd="aws s3 cp --no-sign-request --recursive "
            "s3://genome-scale-tcell-perturb-seq/marson2025_data/ data/full/perturbseq/",
        note="anonymous S3 (no credentials); large. Raw: GEO GSE314342 / SRA SRP643211.",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true", help="run the printed download commands")
    args = ap.parse_args()
    FULL.mkdir(parents=True, exist_ok=True)
    print("Level-3 open-data download routes (verified public sources only):\n")
    for key, r in ROUTES.items():
        print(f"[{key}] {r['title']}")
        print(f"    DOI : {r['doi']}")
        print(f"    URL : {r['url']}")
        print(f"    cmd : {r['cmd']}")
        print(f"    note: {r['note']}\n")
    if not args.execute:
        print("Re-run with --execute to download the compact route, or copy the commands above.")
        print("See docs/REPRODUCIBILITY_LEVELS.md for what each dataset reconstructs.")
        return 0
    # Only the compact, credential-free route is auto-executed.
    r = ROUTES["jia_disease_h5ad"]
    print(f"Downloading: {r['title']} ...")
    try:
        subprocess.run(r["cmd"], shell=True, check=True, cwd=REPO)
    except subprocess.CalledProcessError as e:
        print(f"[warn] download failed ({e}); run the command manually.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
