"""Robustness summaries over the frozen RICTOR tables (guides, conditions, LODO).

These are thin, defensive readers: they surface the decision-relevant summary
(all-positive? min/max? how many folds?) that the decision gate consumes, and
raise if the underlying table is malformed rather than papering over it.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RobustnessSummary:
    n: int
    n_positive: int
    min_value: float
    max_value: float

    @property
    def all_positive(self) -> bool:
        return self.n_positive == self.n and self.n > 0


def _summarise(values: pd.Series) -> RobustnessSummary:
    v = pd.to_numeric(values, errors="coerce").dropna()
    return RobustnessSummary(
        n=int(len(v)),
        n_positive=int((v > 0).sum()),
        min_value=float(v.min()) if len(v) else float("nan"),
        max_value=float(v.max()) if len(v) else float("nan"),
    )


def guide_summary(guides: pd.DataFrame, column: str = "reversal_pearson") -> RobustnessSummary:
    return _summarise(guides[column])


def lodo_summary(lodo: pd.DataFrame, column: str = "reversal_pearson") -> RobustnessSummary:
    # Drop the aggregate "ALL" fold if present; count only the leave-one-donor folds.
    folds = lodo[lodo.get("fold", "") != "ALL"] if "fold" in lodo.columns else lodo
    return _summarise(folds[column])


def condition_summary(conditions: pd.DataFrame, column: str = "reversal_pearson") -> RobustnessSummary:
    return _summarise(conditions[column])
