"""Reversal must align on shared genes, drop non-finite values, and refuse to
score below the minimum shared-gene count (never a silent zero)."""
import numpy as np
import pandas as pd

from perturbgate.reversal import reversal


def test_alignment_on_shared_genes_only():
    kd = pd.Series([1.0, -1.0, 2.0], index=["a", "b", "c"])
    disease = pd.Series([-1.0, 1.0, -2.0], index=["a", "b", "d"])  # only a,b shared
    r = reversal(kd, disease, min_shared=2)
    assert r.n == 2  # 'c' and 'd' dropped


def test_non_finite_dropped():
    kd = pd.Series([1.0, np.nan, 2.0, -3.0], index=list("abcd"))
    disease = pd.Series([-1.0, 5.0, np.inf, 3.0], index=list("abcd"))
    r = reversal(kd, disease, min_shared=2)
    assert r.n == 2  # b (nan) and c (inf) dropped


def test_too_few_shared_returns_none():
    kd = pd.Series([1.0, 2.0], index=["a", "b"])
    disease = pd.Series([1.0, 2.0], index=["a", "b"])
    assert reversal(kd, disease, min_shared=200) is None


def test_degenerate_vector_returns_none():
    kd = pd.Series([1.0] * 300, index=[f"g{i}" for i in range(300)])  # zero variance
    disease = pd.Series(np.arange(300.0), index=[f"g{i}" for i in range(300)])
    assert reversal(kd, disease, min_shared=200) is None
