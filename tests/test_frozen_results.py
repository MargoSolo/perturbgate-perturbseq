"""Golden-value tests on the frozen tables, with documented tolerances. These
guard against silent numerical regression and against a superseded value
re-entering the public outputs."""
import json

import pandas as pd
import pytest

from perturbgate import GOLDEN
from perturbgate.io import frozen_dir


@pytest.fixture(scope="module")
def primary():
    return pd.read_csv(frozen_dir() / "primary_comparison.tsv", sep="\t")


def test_rictor_primary_reversal(primary):
    v = float(primary.loc[primary.target == "RICTOR", "primary_reversal"].iloc[0])
    assert abs(v - GOLDEN["RICTOR_reversal_pearson"]) < 2e-3


def test_rictor_is_not_the_superseded_043(primary):
    v = float(primary.loc[primary.target == "RICTOR", "primary_reversal"].iloc[0])
    assert abs(v - GOLDEN["SUPERSEDED_RICTOR_reversal"]) > 0.2


def test_pak2_not_therapeutically_directional(primary):
    row = primary.loc[primary.target == "PAK2"].iloc[0]
    assert row["final_public_label"] == "REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL"
    assert abs(float(row["primary_reversal"]) - GOLDEN["PAK2_reversal_pearson"]) < 2e-3
    assert float(row["primary_pearson_p"]) > 0.05  # not significant


def test_matched_null_frozen_values():
    mn = pd.read_csv(frozen_dir() / "matched_null.tsv", sep="\t").set_index("target")
    assert abs(float(mn.loc["RICTOR", "empirical_p"]) - GOLDEN["RICTOR_matched_empirical_p"]) < 1e-4
    assert abs(float(mn.loc["RICTOR", "percentile"]) - GOLDEN["RICTOR_matched_percentile"]) < 0.5
    assert float(mn.loc["PAK2", "empirical_p"]) > 0.5   # PAK2 at the null median
    assert float(mn.loc["RIPK1", "empirical_p"]) > 0.5


def test_matched_null_values_exceedances():
    vals = pd.read_csv(frozen_dir() / "rictor_matched_null_values.tsv", sep="\t")
    assert len(vals) == GOLDEN["RICTOR_matched_n_null"]
    assert int(vals["exceeds_rictor"].sum()) == GOLDEN["RICTOR_matched_exceedances"]


def test_labels_in_controlled_vocabulary(primary):
    from perturbgate import PUBLIC_LABELS
    for lab in primary["final_public_label"]:
        assert lab in PUBLIC_LABELS


def test_analysis_contract_flags_weakest_criterion():
    contract = json.load(open(frozen_dir() / "analysis_contract.json", encoding="utf-8"))
    note = contract["matched_null"]["note"].lower()
    assert "weakest" in note
    assert "8/8 decisive" in note or "do not write" in note
