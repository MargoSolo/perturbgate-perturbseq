"""Candidate-funnel denominators are internally consistent, the ledger vocabulary
is honest, and 'not advanced' is kept distinct from 'rejected after validation'."""
import pandas as pd

from targetgate import attrition
from targetgate.io import frozen_dir


def test_funnel_denominators_sum():
    fn = pd.read_csv(frozen_dir() / "candidate_funnel.tsv", sep="\t")
    assert attrition.check_funnel(fn) == []


def test_screen_starts_at_924():
    fn = pd.read_csv(frozen_dir() / "candidate_funnel.tsv", sep="\t")
    s0 = fn[fn.stage_id == "S0"].iloc[0]
    assert int(s0["n_entering"]) == 924
    assert s0["scope"] == "SCREEN_WIDE"


def test_ledger_vocabulary_and_depth_consistency():
    led = pd.read_csv(frozen_dir() / "rejection_ledger.tsv", sep="\t")
    assert attrition.check_ledger_depths(led) == []


def test_not_advanced_distinct_from_rejected():
    ap = pd.read_csv(frozen_dir() / "all_perturbations_authoritative_reversal.tsv", sep="\t")
    classes = set(ap["final_evidence_class"].dropna().unique())
    # both categories must exist and be different labels
    assert "NOT_ADVANCED_FROM_SCREEN" in classes
    assert "REJECTED_AFTER_DEEP_VALIDATION" in classes
    assert "RETAINED_MECHANISM_HYPOTHESIS" in classes


def test_only_one_retained_hypothesis():
    ap = pd.read_csv(frozen_dir() / "all_perturbations_authoritative_reversal.tsv", sep="\t")
    counts = attrition.screen_counts(ap)
    assert counts["n_total"] == 924
    assert counts["n_retained"] == 1  # RICTOR only
