"""Level-2 analytical reproduction from public derived matrices.

Recomputes the two decision-critical RICTOR robustness axes from the shipped
Level-2 inputs and returns them for comparison against the frozen tables:

* guide-separate reversal (criterion 4) — pooled KO-vs-NTC pseudobulk per guide;
* leave-one-disease-donor-out reversal (criterion 5) — the responder-DE meta KD
  vector re-scored against each disease vector rebuilt with one donor removed.

Condition-level and matched-null reproduction require the per-condition meta
vectors and the genome-scale effect-vector substrate respectively (Level 3); see
docs/REPRODUCIBILITY_LEVELS.md.
"""
from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pandas as pd

from .io import load_kd_meta
from .reversal import reversal

CONDS = ["Rest", "Stim8hr", "Stim48hr"]


def _cpm(v: np.ndarray) -> np.ndarray:
    s = v.sum()
    return (v / s * 1e6) if s > 0 else v


def recompute_guides_conditions_lodo(repro_dir: Path, disease: pd.Series) -> dict[str, pd.DataFrame]:
    pb = pd.read_parquet(repro_dir / "pseudobulk_counts.parquet")
    pbm = pd.read_csv(repro_dir / "pseudobulk_meta.tsv", sep="\t", index_col=0)
    genes = list(pb.columns)
    ntc_units = pbm[pbm.responder == "NTC"].index
    ntc_all = _cpm(pb.loc[ntc_units].sum(0).to_numpy(dtype=float))

    def kd_pooled(target: str, guide: str) -> pd.Series | None:
        ids = pbm[(pbm.target == target) & (pbm.guide == guide) & (pbm.responder == "KO")].index
        if len(ids) == 0:
            return None
        ko = _cpm(pb.loc[ids].sum(0).to_numpy(dtype=float))
        return pd.Series(np.log2((ko + 1) / (ntc_all + 1)), index=genes)

    # --- guides ---
    grows = []
    guides = sorted(g for g in pbm[pbm.target == "RICTOR"].guide.dropna().unique()
                    if g not in ("ALL", "NA", "nan"))
    for gd in guides:
        r = reversal(kd_pooled("RICTOR", gd), disease)
        if r is not None:
            grows.append(dict(target="RICTOR", guide=gd, n_aligned=r.n,
                              reversal_pearson=r.reversal_score, reversal_spearman=r.reversal_spearman,
                              frac_reversed=r.frac_reversed))
    guides_df = pd.DataFrame(grows)

    # --- LODO ---
    ov = load_kd_meta("RICTOR")
    with gzip.open(repro_dir / "disease_perdonor_logfc_activated_memory.tsv.gz", "rt", encoding="utf-8") as fh:
        perdonor = pd.read_csv(fh, sep="\t", index_col=0)
    donors = list(perdonor.columns)
    lrows = [dict(fold="ALL", dropped="none",
                  reversal_pearson=reversal(ov, disease).reversal_score,
                  reversal_spearman=reversal(ov, disease).reversal_spearman,
                  n=reversal(ov, disease).n)]
    for dcol in donors:
        keep = [c for c in donors if c != dcol]
        dvec = perdonor[keep].mean(axis=1)
        r = reversal(ov, dvec)
        if r is not None:
            lrows.append(dict(fold=f"drop_{dcol}", dropped=dcol, reversal_pearson=r.reversal_score,
                              reversal_spearman=r.reversal_spearman, n=r.n))
    lodo_df = pd.DataFrame(lrows)

    return {"rictor_guides": guides_df, "rictor_lodo": lodo_df}
