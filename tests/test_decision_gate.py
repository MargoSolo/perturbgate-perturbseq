"""The decision gate must map seven strong criteria to the retained-mechanism
label, only ever emit controlled-vocabulary labels, and treat the matched-null as
the weakest criterion."""
from perturbgate import PUBLIC_LABELS
from perturbgate.decision_gate import WEAKEST_CRITERION, evaluate_rictor


def test_seven_strong_pass_gives_mechanism_node():
    g = evaluate_rictor(True, True, True, True, True, True, True, above_matched_null=True)
    assert g.label == "DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP"
    assert g.label in PUBLIC_LABELS
    assert g.strong_pass == 7
    assert g.n_pass == 8


def test_matched_null_is_weakest_not_load_bearing():
    # Failing only the matched-null (criterion 8) still retains the mechanism node,
    # because the seven strong criteria carry the label.
    g = evaluate_rictor(True, True, True, True, True, True, True, above_matched_null=False)
    assert g.label == "DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP"
    assert g.strong_pass == 7
    assert WEAKEST_CRITERION == "8_above_matched_perturbation_null"


def test_missing_strong_criterion_downgrades():
    g = evaluate_rictor(True, True, True, True, False, True, True, above_matched_null=True)
    assert g.label == "COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS"
    assert g.label in PUBLIC_LABELS


def test_caveat_names_the_borderline():
    g = evaluate_rictor(True, True, True, True, True, True, True, above_matched_null=True)
    assert "borderline" in g.caveat.lower()
    assert "weakest" in g.caveat.lower()
