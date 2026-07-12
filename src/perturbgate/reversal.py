"""Disease-state reversal scoring.

A perturbation *reverses* a disease direction if its knockdown (KD) effect vector
moves genes opposite to the disease direction. The primary statistic is the
negative centered-Pearson correlation between the KD log2FC vector and the disease
log2FC vector over shared, finite genes:

    reversal = -pearson(KD, disease)        (> 0 = reversing, < 0 = mimicking)

This is a deliberately simple, sign-explicit, effect-size-first metric. The sign
convention is fixed once here and asserted in tests: KD down where disease is up
(and KD up where disease is down) yields a positive reversal.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
from scipy import stats

#: minimum shared, finite genes for a reversal to be defined
MIN_SHARED = 200
#: |log2FC| for a gene to count as "moved" in the reversed / reinforced tally
KD_FLOOR = 0.10


@dataclass(frozen=True)
class ReversalResult:
    n: int
    pearson: float
    reversal_score: float
    pearson_p: float
    spearman: float
    reversal_spearman: float
    spearman_p: float
    n_reversed: int
    n_reinforced: int
    frac_reversed: float

    def as_dict(self) -> dict:
        return asdict(self)


def reversal(
    kd: pd.Series,
    disease: pd.Series,
    floor: float = KD_FLOOR,
    min_shared: int = MIN_SHARED,
) -> ReversalResult | None:
    """Return the reversal score of a KD vector against a disease vector.

    Parameters
    ----------
    kd, disease : pandas.Series indexed by gene id (e.g. ENSG...), values log2FC.
    floor : |KD log2FC| threshold for counting a gene as moved.
    min_shared : minimum shared finite genes; below this the score is undefined.

    Returns ``None`` when the vectors do not share enough finite, non-degenerate
    genes — never a silent zero.
    """
    if kd is None or disease is None:
        return None
    common = kd.index.intersection(disease.index)
    if len(common) < min_shared:
        return None
    k = kd.loc[common].to_numpy(dtype=float)
    v = disease.loc[common].to_numpy(dtype=float)
    ok = np.isfinite(k) & np.isfinite(v)
    k, v = k[ok], v[ok]
    if len(k) < min_shared or np.std(k) < 1e-9 or np.std(v) < 1e-9:
        return None
    r, p = stats.pearsonr(k, v)
    rho, prho = stats.spearmanr(k, v)
    strong = np.abs(k) >= floor
    n_rev = int(np.sum(strong & (np.sign(k) == -np.sign(v))))
    n_rei = int(np.sum(strong & (np.sign(k) == np.sign(v))))
    frac = n_rev / (n_rev + n_rei) if (n_rev + n_rei) else float("nan")
    return ReversalResult(
        n=len(k),
        pearson=float(r),
        reversal_score=float(-r),
        pearson_p=float(p),
        spearman=float(rho),
        reversal_spearman=float(-rho),
        spearman_p=float(prho),
        n_reversed=n_rev,
        n_reinforced=n_rei,
        frac_reversed=float(frac),
    )


def gsea_reversal(kd: pd.Series, disease: pd.Series, set_floor: float = 0.25,
                  cons: pd.Series | None = None, cons_floor: float = 0.70,
                  cap: int = 300) -> dict:
    """Rank-based reversal: are disease-UP genes at the KD-DOWN end (and vice versa)?

    Returns a dict with ``nes_up`` (disease-UP set, negative = pushed down by KD),
    ``nes_down`` (disease-DOWN set, positive = pushed up by KD) and their
    difference ``gsea_reversal`` (> 0 = same direction as centered-Pearson reversal).
    A light-weight rank-sum standin for a full permutation GSEA, adequate for the
    directional check the decision gate needs.
    """
    common = kd.index.intersection(disease.index)
    k = kd.loc[common]
    d = disease.loc[common]
    if cons is not None:
        c = cons.reindex(common).fillna(0.0)
        strong = (d.abs() >= set_floor) & (c >= cons_floor)
    else:
        strong = d.abs() >= set_floor
    up = d[strong & (d > 0)].sort_values(ascending=False).index[:cap]
    dn = d[strong & (d < 0)].sort_values().index[:cap]
    ranks = k.rank()
    n = len(k)

    def _nes(genes) -> float:
        if len(genes) == 0:
            return float("nan")
        # signed, mean-centered rank score in [-1, 1]
        return float((ranks.loc[genes].mean() - (n + 1) / 2) / ((n - 1) / 2))

    nes_up = _nes(up)
    nes_dn = _nes(dn)
    return {
        "nes_up": nes_up,
        "nes_down": nes_dn,
        "gsea_reversal": (nes_dn - nes_up) if np.isfinite(nes_up) and np.isfinite(nes_dn) else float("nan"),
        "n_up": int(len(up)),
        "n_down": int(len(dn)),
    }
