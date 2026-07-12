"""Disease-direction vector helpers.

The primary disease vector is a donor-paired, raw-count pseudobulk log2 fold change
of synovium (tissue + fluid) versus peripheral blood in activated-memory CD4 T
cells (JIA), meta-analysed across 11 paired donors. Level-1 loads the frozen
vector; Level-2 recomputes it (and its leave-one-donor-out variants) from the
per-donor log2FC matrix so the LODO robustness can be reproduced.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def meta_across_donors(perdonor: pd.DataFrame) -> pd.Series:
    """Mean log2FC across donor columns (genes x donors), ignoring NaN.

    A plain across-donor mean of per-donor log2FC — the frozen vector's central
    estimate. Genes with no finite donor value are dropped.
    """
    m = perdonor.apply(pd.to_numeric, errors="coerce")
    mean = m.mean(axis=1, skipna=True)
    return mean.dropna()


def leave_one_donor_out(perdonor: pd.DataFrame):
    """Yield (dropped_donor, disease_vector) for each donor column removed."""
    for donor in perdonor.columns:
        sub = perdonor.drop(columns=[donor])
        yield donor, meta_across_donors(sub)


def align(a: pd.Series, b: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """Aligned, finite value arrays for two gene-indexed series."""
    common = a.index.intersection(b.index)
    x = a.loc[common].to_numpy(dtype=float)
    y = b.loc[common].to_numpy(dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    return x[ok], y[ok]
