"""TargetGate — evidence-gated pipeline for T-cell Perturb-seq mechanism hypotheses.

TargetGate turns perturbation effects into *evidence-gated mechanism hypotheses*.
A real cellular effect is treated as necessary but not sufficient for target
nomination: every retained claim must survive an explicit record of how competing
claims failed.

The package is deliberately small and auditable. The scientific core is:

    reversal      disease-state reversal scoring (centered-Pearson / Spearman / GSEA)
    calibration   matched-perturbation empirical null + finite-pool uncertainty
    robustness    guide / donor / condition / leave-one-donor-out summaries
    decision_gate the pre-specified controlled-vocabulary decision rule
    attrition     candidate funnel + rejection ledger construction and checks
    claim_ledger  claim -> artifact -> evidence resolution
    figures       code-generated, colour-blind-safe figures with source data
"""
from __future__ import annotations

__version__ = "1.0.0"
__all__ = ["__version__"]

# --- Controlled vocabulary: final public labels -----------------------------
# These are the only labels a public decision may carry. See docs/ANALYSIS_CONTRACT.md.
PUBLIC_LABELS = {
    "DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP",
    "REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL",
    "COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS",
}

# --- Frozen headline values (golden). Sources in results/frozen/ ------------
# Used by tests and `targetgate verify` to guard against silent regression or a
# superseded value re-entering the public outputs.
GOLDEN = {
    "RICTOR_reversal_pearson": 0.1605626914415677,
    "RICTOR_reversal_spearman": 0.09997246194193402,
    "RICTOR_n_aligned": 10832,
    "PAK2_reversal_pearson": 0.010021905940826631,
    "RIPK1_reversal_pearson": 0.03770091514851947,
    "RICTOR_matched_substrate_reversal": 0.13139354029469041,
    "RICTOR_matched_exceedances": 7,
    "RICTOR_matched_n_null": 200,
    "RICTOR_matched_empirical_p": 0.03980099502487562,
    "RICTOR_matched_percentile": 96.5,
    "RICTOR_guide1_reversal": 0.1409652082404923,
    "RICTOR_guide2_reversal": 0.17807160648954987,
    "RICTOR_condition_Rest": 0.15322575835075294,
    "RICTOR_condition_Stim8hr": 0.09159034556775436,
    "RICTOR_condition_Stim48hr": 0.04220380333572861,
    "RICTOR_lodo_folds": 11,
    # Values that must NEVER appear as a current RICTOR reversal (superseded):
    "SUPERSEDED_RICTOR_reversal": 0.43,
}
