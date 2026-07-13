#!/usr/bin/env python3
"""Build results/frozen/rictor_robustness_tracks.tsv — the single provenance-closed
artifact behind the RICTOR robustness figure.

Nine tracks are DERIVED from committed frozen tables (recomputable at Level 1 and
guarded by tests/test_figure_source_provenance.py). Two tracks are SERVER-SCALE
NARRATIVE ANCHORS (adjusted-vector sensitivity, responder-only mean) that come from
the full Level-3 run and are not recomputed at Level 1; each is labelled as such in
the `source_artifact` column so every number in the figure resolves to an artifact.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / "results" / "frozen"


def r6(x) -> float:
    return round(float(x), 6)


def build() -> pd.DataFrame:
    pc = pd.read_csv(F / "primary_comparison.tsv", sep="\t")
    r = pc[pc.target == "RICTOR"].iloc[0]
    lodo = pd.read_csv(F / "rictor_lodo.tsv", sep="\t")
    folds = lodo[lodo.fold != "ALL"]["reversal_pearson"].astype(float)
    conf = pd.read_csv(F / "confound_decomposition.tsv", sep="\t")
    cr = float(conf[conf.removed == "cellcycle+activation+broaddown"]["reversal_pearson"].iloc[0])

    ANCHOR = ("server-scale (make full / Level 3) run; same-cohort narrative anchor, "
              "not recomputed at Level 1; see docs/REPRODUCIBILITY_LEVELS.md")
    rows = [
        ("primary raw-count vector", r6(r["primary_reversal"]), "", "", "primary_comparison.tsv:RICTOR:primary_reversal"),
        ("adjusted-vector sensitivity", 0.147, "", "", "covariate-adjusted disease-vector sensitivity — " + ANCHOR),
        ("RICTOR guide 1", r6(r["guide_1_reversal"]), "", "", "primary_comparison.tsv:RICTOR:guide_1_reversal"),
        ("RICTOR guide 2", r6(r["guide_2_reversal"]), "", "", "primary_comparison.tsv:RICTOR:guide_2_reversal"),
        ("disease-donor LODO (11)", r6(folds.mean()), r6(folds.min()), r6(folds.max()), "rictor_lodo.tsv:11_folds(mean;min;max)"),
        ("responder-only mean", 0.054, "", "", "responder-only strata mean — " + ANCHOR),
        ("condition: Rest", r6(r["condition_rest"]), "", "", "primary_comparison.tsv:RICTOR:condition_rest"),
        ("condition: Stim8hr", r6(r["condition_stim8"]), "", "", "primary_comparison.tsv:RICTOR:condition_stim8"),
        ("condition: Stim48hr", r6(r["condition_stim48"]), "", "", "primary_comparison.tsv:RICTOR:condition_stim48"),
        ("confound-removed (cc+act+broad)", r6(cr), "", "", "confound_decomposition.tsv:cellcycle+activation+broaddown"),
        ("matched-null substrate", r6(r["matched_substrate_reversal"]), "", "", "primary_comparison.tsv:RICTOR:matched_substrate_reversal"),
    ]
    return pd.DataFrame(rows, columns=["track", "reversal", "range_low", "range_high", "source_artifact"])


def main() -> int:
    df = build()
    out = F / "rictor_robustness_tracks.tsv"
    out.write_bytes(df.to_csv(sep="\t", index=False, lineterminator="\n").encode("utf-8"))
    print(f"wrote {out.relative_to(ROOT)} ({len(df)} tracks; "
          f"{(df.source_artifact.str.contains('narrative anchor')).sum()} server-scale anchors)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
