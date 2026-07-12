#!/usr/bin/env python3
"""Denominator audit: reconcile the perturbation counts used in the narrative.

The genome-scale screen perturbs all expressed genes; this analysis operates over
the perturbations that have a usable genome-scale effect vector in the processed
release. This script counts exactly what those rows are so the README never uses a
rounded "~920" and the precise "924" interchangeably. Reads only the committed
authoritative table; runs anywhere.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
FROZEN = REPO / "results" / "frozen"


def main() -> None:
    ap = pd.read_csv(FROZEN / "all_perturbations_authoritative_reversal.tsv", sep="\t")
    is_ensg = ap["perturbation_id"].astype(str).str.match(r"^ENSG\d+$")
    control_like = ap["gene_symbol"].astype(str).str.contains(
        r"NTC|CONTROL|SAFE.?HARBOR|NON.?TARGET|SCRAMBLE|GFP|OLFR", case=False, regex=True
    )
    deep = ap["evidence_depth"] == "DEEP"
    rows = [
        dict(quantity="total_rows_scored", count=int(len(ap)),
             definition="perturbations with a usable genome-scale effect vector in the processed release"),
        dict(quantity="biological_target_perturbations", count=int(is_ensg.sum()),
             definition="rows whose perturbation_id is an ENSG gene id (a gene knockdown)"),
        dict(quantity="unique_target_genes", count=int(ap["gene_symbol"].nunique()),
             definition="distinct HGNC gene symbols perturbed (no duplicates)"),
        dict(quantity="non_targeting_controls_in_scored_set", count=int(control_like.sum()),
             definition="NTC / safe-harbor / non-targeting rows among the scored perturbations "
                        "(controls are the baseline effects are measured against, not scored rows)"),
        dict(quantity="deep_validated_candidates", count=int(deep.sum()),
             definition="RICTOR, PAK2, RIPK1 (carried into candidate-specific deep validation)"),
    ]
    audit = pd.DataFrame(rows)
    with open(FROZEN / "denominator_audit.tsv", "w", encoding="utf-8", newline="") as fh:
        audit.to_csv(fh, sep="\t", index=False, lineterminator="\n")
    print(audit.to_string(index=False))
    print()
    n = int(len(ap))
    assert int(is_ensg.sum()) == n and int(ap["gene_symbol"].nunique()) == n and int(control_like.sum()) == 0
    print(f"RECONCILIATION: all {n} scored rows are unique gene-target perturbations; there is no "
          f"separate control/comparator subset. The precise denominator is {n}; '~920' is informal "
          f"branding only and is not used as a distinct count.")
    print("wrote results/frozen/denominator_audit.tsv")


if __name__ == "__main__":
    main()
