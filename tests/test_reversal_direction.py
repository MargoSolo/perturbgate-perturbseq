"""The sign convention is the single most important invariant: KD opposite to
disease must give a positive reversal; KD equal to disease must be negative."""
import numpy as np
import pandas as pd

from perturbgate.reversal import reversal


def _series(vals):
    return pd.Series(vals, index=[f"g{i}" for i in range(len(vals))])


def test_opposite_direction_is_positive_reversal():
    rng = np.random.default_rng(0)
    disease = _series(rng.normal(size=500))
    kd = _series(-disease.to_numpy())  # perfectly opposite
    r = reversal(kd, disease)
    assert r.reversal_score > 0.99  # near +1: strong reversal
    assert r.pearson < 0


def test_same_direction_is_negative_reversal():
    rng = np.random.default_rng(1)
    disease = _series(rng.normal(size=500))
    kd = _series(disease.to_numpy())  # identical (mimicking)
    r = reversal(kd, disease)
    assert r.reversal_score < -0.99  # mimicking, not reversing


def test_reversed_reinforced_counts_use_floor():
    disease = _series([1.0, 1.0, -1.0, -1.0, 0.0])
    kd = _series([-1.0, 0.05, 1.0, 0.05, -1.0])  # 0.05 below KD_FLOOR=0.1
    r = reversal(kd, disease, min_shared=3)
    # only the two strong opposite-sign genes count as reversed
    assert r.n_reversed == 2
    assert r.n_reinforced == 0
