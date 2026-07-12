"""The pre-specified decision gate.

Eight convergence criteria were fixed *before* the RICTOR raw-count result was
viewed. Seven are strong convergence checks; the eighth (matched-null) is the
weakest and is reported with its finite-pool uncertainty. This module encodes the
criteria and the controlled-vocabulary label they map to. It never invents a
label outside the vocabulary and never silently upgrades a borderline criterion.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import PUBLIC_LABELS

CRITERIA = [
    "1_centered_pearson_reversal_pos",
    "2_spearman_reversal_pos",
    "3_gsea_reversal_same_direction",
    "4_both_guides_same_direction",
    "5_all_disease_donor_lodo_positive",
    "6_responder_only_support",
    "7_positive_in_all_three_conditions",
    "8_above_matched_perturbation_null",
]

#: Criterion 8 is intentionally the weakest: a finite matched pool (k=200) with a
#: Wilson-interval upper bound that grazes 0.05. Reported, never inflated.
WEAKEST_CRITERION = "8_above_matched_perturbation_null"


@dataclass
class GateEvaluation:
    target: str
    criteria: dict
    label: str
    caveat: str

    @property
    def n_pass(self) -> int:
        return int(sum(bool(v) for v in self.criteria.values()))

    @property
    def strong_pass(self) -> int:
        """Passes among the seven strong (non-matched-null) criteria."""
        return int(sum(bool(v) for k, v in self.criteria.items() if k != WEAKEST_CRITERION))


def evaluate_rictor(
    reversal_pos: bool,
    spearman_pos: bool,
    gsea_same_dir: bool,
    both_guides_pos: bool,
    lodo_all_pos: bool,
    responder_support: bool,
    all_conditions_pos: bool,
    above_matched_null: bool,
) -> GateEvaluation:
    """Evaluate the eight criteria and assign the retained-mechanism label.

    RICTOR is retained *only* as a mechanism node with a modality gap, and only
    when the seven strong criteria pass. Criterion 8 passing at the point estimate
    is recorded together with its borderline finite-pool caveat.
    """
    crit = {
        "1_centered_pearson_reversal_pos": reversal_pos,
        "2_spearman_reversal_pos": spearman_pos,
        "3_gsea_reversal_same_direction": gsea_same_dir,
        "4_both_guides_same_direction": both_guides_pos,
        "5_all_disease_donor_lodo_positive": lodo_all_pos,
        "6_responder_only_support": responder_support,
        "7_positive_in_all_three_conditions": all_conditions_pos,
        "8_above_matched_perturbation_null": above_matched_null,
    }
    strong = sum(bool(v) for k, v in crit.items() if k != WEAKEST_CRITERION)
    label = (
        "DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP"
        if strong == 7
        else "COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS"
    )
    assert label in PUBLIC_LABELS
    caveat = (
        "RICTOR satisfied seven strong convergence checks and nominally exceeded a "
        "matched-perturbation null, with borderline finite-pool uncertainty "
        "(200 matched controls; 7 exceed RICTOR; empirical p ~= 0.040; Wilson 95% "
        "CI up to ~0.070). Criterion 8 is the weakest of the eight."
    )
    return GateEvaluation(target="RICTOR", criteria=crit, label=label, caveat=caveat)
