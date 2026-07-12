"""All 11 disease-donor leave-one-out folds must reverse positively (criterion 5),
and the conditions must all be positive (criterion 7)."""
import pandas as pd

from targetgate import GOLDEN
from targetgate.io import frozen_dir
from targetgate.robustness import condition_summary, lodo_summary


def test_all_11_lodo_folds_positive():
    lodo = pd.read_csv(frozen_dir() / "rictor_lodo.tsv", sep="\t")
    summ = lodo_summary(lodo)
    assert summ.n == GOLDEN["RICTOR_lodo_folds"]  # 11 folds (ALL excluded)
    assert summ.all_positive
    assert summ.min_value > 0.14  # tight band around +0.16


def test_all_three_conditions_positive():
    cond = pd.read_csv(frozen_dir() / "rictor_conditions.tsv", sep="\t")
    summ = condition_summary(cond)
    assert summ.n == 3
    assert summ.all_positive


def test_condition_values_match_golden():
    cond = pd.read_csv(frozen_dir() / "rictor_conditions.tsv", sep="\t").set_index("condition")["reversal_pearson"]
    assert abs(cond["Rest"] - GOLDEN["RICTOR_condition_Rest"]) < 1e-3
    assert abs(cond["Stim8hr"] - GOLDEN["RICTOR_condition_Stim8hr"]) < 1e-3
    assert abs(cond["Stim48hr"] - GOLDEN["RICTOR_condition_Stim48hr"]) < 1e-3
