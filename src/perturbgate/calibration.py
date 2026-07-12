"""Matched-perturbation null calibration and finite-pool uncertainty.

The reversal score of a candidate is only meaningful relative to what other
*comparable* perturbations achieve against the same disease vector. We match on
five effect-shape features (magnitude, breadth, donor-sign consistency, guide
concordance, on-target knockdown), take the k nearest neighbours in z-scored
feature space, and ask how the candidate ranks inside that matched pool.

Criterion 8 of the decision gate is the weakest link precisely because the pool
is finite (k = 200). This module reports the deterministic empirical p together
with its finite-pool uncertainty (Wilson interval on the exceedance count) so the
significance is never overstated.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NullResult:
    observed: float
    n_null: int
    n_exceed: int
    empirical_p: float
    percentile: float
    null_mean: float
    null_sd: float
    z: float
    wilson_low: float
    wilson_high: float

    def as_dict(self) -> dict:
        return {
            "observed_reversal": self.observed,
            "n_null": self.n_null,
            "n_exceed": self.n_exceed,
            "empirical_p": self.empirical_p,
            "percentile": self.percentile,
            "null_mean": self.null_mean,
            "null_sd": self.null_sd,
            "z": self.z,
            "wilson_low": self.wilson_low,
            "wilson_high": self.wilson_high,
        }


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion k/n (default 95%).

    Used for the finite-pool uncertainty on the exceedance fraction, which is the
    honest limit on the empirical p — resampling the same pool with more Monte
    Carlo draws cannot shrink it.
    """
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (float(centre - half), float(centre + half))


def empirical_p(observed: float, null_values: np.ndarray) -> NullResult:
    """One-sided empirical p that ``observed`` is not exceeded by the matched null.

    p = (#{null >= observed} + 1) / (n + 1)  — the deterministic add-one estimator.
    Larger reversal is better, so exceedance means a matched perturbation reverses
    at least as strongly as the candidate.
    """
    null = np.asarray(null_values, dtype=float)
    null = null[np.isfinite(null)]
    n = len(null)
    n_exceed = int(np.sum(null >= observed))
    p = (n_exceed + 1) / (n + 1)
    pct = float(np.mean(null < observed) * 100.0)
    sd = float(null.std())
    z = float((observed - null.mean()) / sd) if sd > 0 else float("nan")
    lo, hi = wilson_interval(n_exceed, n)
    return NullResult(
        observed=float(observed),
        n_null=n,
        n_exceed=n_exceed,
        empirical_p=float(p),
        percentile=pct,
        null_mean=float(null.mean()),
        null_sd=sd,
        z=z,
        wilson_low=lo,
        wilson_high=hi,
    )
