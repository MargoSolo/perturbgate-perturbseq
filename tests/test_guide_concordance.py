"""Both RICTOR guides must reverse in the same (positive) direction (criterion 4),
and the frozen values must match the golden guide reversals."""
import pandas as pd

from targetgate import GOLDEN
from targetgate.io import frozen_dir
from targetgate.robustness import guide_summary


def test_both_rictor_guides_positive_and_concordant():
    g = pd.read_csv(frozen_dir() / "rictor_guides.tsv", sep="\t")
    summ = guide_summary(g)
    assert summ.n == 2
    assert summ.all_positive


def test_guide_values_match_golden():
    g = pd.read_csv(frozen_dir() / "rictor_guides.tsv", sep="\t").set_index("guide")["reversal_pearson"]
    assert abs(g["RICTOR-1"] - GOLDEN["RICTOR_guide1_reversal"]) < 1e-3
    assert abs(g["RICTOR-2"] - GOLDEN["RICTOR_guide2_reversal"]) < 1e-3
