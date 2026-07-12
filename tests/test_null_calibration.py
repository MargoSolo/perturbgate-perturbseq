"""Matched-null empirical p and finite-pool (Wilson) uncertainty are deterministic
and match the frozen RICTOR calibration (7 of 200 exceed, p ~ 0.0398)."""
import numpy as np

from perturbgate import GOLDEN
from perturbgate.calibration import empirical_p, wilson_interval


def test_empirical_p_add_one_estimator():
    null = np.array([0.0] * 193 + [1.0] * 7)  # 7 of 200 exceed observed=0.5
    res = empirical_p(0.5, null)
    assert res.n_null == 200
    assert res.n_exceed == 7
    assert abs(res.empirical_p - (7 + 1) / (200 + 1)) < 1e-12
    assert abs(res.empirical_p - GOLDEN["RICTOR_matched_empirical_p"]) < 1e-9


def test_wilson_interval_on_7_of_200():
    lo, hi = wilson_interval(7, 200)
    assert 0.016 < lo < 0.018
    assert 0.069 < hi < 0.072  # grazes 0.05-0.07 as documented


def test_determinism():
    null = np.array([0.0] * 193 + [1.0] * 7)
    a = empirical_p(0.5, null).as_dict()
    b = empirical_p(0.5, null).as_dict()
    assert a == b


def test_nonfinite_null_values_ignored():
    null = np.array([0.0, np.nan, 1.0, np.inf, -np.inf])
    res = empirical_p(0.5, null)
    assert res.n_null == 2  # nan and +/-inf all dropped, leaving 0.0 and 1.0
