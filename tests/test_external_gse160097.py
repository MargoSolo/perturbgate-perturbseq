"""External same-disease concordance (GSE160097) golden-value + guard tests.

Reproduces the external reversal offline from committed derived aggregates and the
committed KD vectors, and asserts the frozen external numbers. Also guards that the
external artifacts never claim causal/therapeutic/target validation and never say
"independent cohort" (the cohort-independence audit is NOT_FULLY_VERIFIABLE).
"""
import json
from pathlib import Path

import pytest

from perturbgate.external import gse160097 as ext


@pytest.fixture(scope="module")
def result():
    return ext.run(write=False)


def test_rictor_external_reversal(result):
    v = result["primary"]["RICTOR"]["reversal"]
    assert abs(v - ext.GOLDEN["RICTOR_reversal"]) < 1.5e-3
    # reproduces the internal reference within a small margin
    assert abs(v - ext.GOLDEN["internal_reference"]) < 0.02


def test_comparators_near_zero(result):
    assert abs(result["primary"]["PAK2"]["reversal"] - ext.GOLDEN["PAK2_reversal"]) < 1.5e-3
    assert abs(result["primary"]["RIPK1"]["reversal"] - ext.GOLDEN["RIPK1_reversal"]) < 1.5e-3
    assert result["primary"]["PAK2"]["reversal"] < 0.02
    assert result["primary"]["RIPK1"]["reversal"] < 0.02


def test_paired_lodo_all_positive(result):
    assert result["n_donor_pairs"] == 6
    assert result["lodo_all_positive"]
    assert all(v > 0 for v in result["lodo"].values())


def test_paired_bootstrap_excludes_zero(result):
    b = result["bootstrap"]
    assert b["frac_positive"] >= 0.999
    assert b["p2_5"] > 0
    assert abs(b["median"] - 0.160) < 0.01


def test_golden_validate_clean(result):
    assert ext.validate(result) == []


def test_cohort_independence_not_overclaimed():
    d = Path(__file__).resolve().parents[1] / "results" / "external_validation" / "gse160097"
    manifest = json.loads((d / "result_manifest.json").read_text(encoding="utf-8"))
    assert manifest["cohort_independence"] == "NO_OVERLAP_DETECTED_BUT_NOT_FULLY_VERIFIABLE"
    for f in ["result_manifest.json", "analysis_contract.json", "cohort_independence_audit.tsv"]:
        assert "independent cohort" not in (d / f).read_text(encoding="utf-8").lower()


def test_no_forbidden_translational_claims():
    d = Path(__file__).resolve().parents[1] / "results" / "external_validation" / "gse160097"
    text = " ".join((d / f).read_text(encoding="utf-8").lower()
                     for f in ["result_manifest.json", "analysis_contract.json"])
    for forbidden in ["therapeutic replication", "causal replication", "clinical validation",
                      "validated drug target"]:
        # only allowed inside an explicit not_claimed / negated list
        assert forbidden not in text or "not_claimed" in text
