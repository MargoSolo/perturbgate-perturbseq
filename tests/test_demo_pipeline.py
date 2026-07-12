"""End-to-end demo: recompute the reversal from the committed compact inputs and
assert the headline values reproduce the golden numbers within tolerance. This is
the test that proves the demo genuinely recomputes +0.161 rather than echoing it."""

from perturbgate import GOLDEN
from perturbgate.io import load_disease_vector, load_kd_meta
from perturbgate.reversal import reversal

TOL = 1e-3


def _recompute():
    disease = load_disease_vector()
    rows = {}
    for t in ("RICTOR", "PAK2", "RIPK1"):
        r = reversal(load_kd_meta(t), disease)
        rows[t] = r
    return rows


def test_rictor_recomputes_to_golden():
    r = _recompute()["RICTOR"]
    assert abs(r.reversal_score - GOLDEN["RICTOR_reversal_pearson"]) < TOL
    assert abs(r.reversal_spearman - GOLDEN["RICTOR_reversal_spearman"]) < TOL
    assert r.n == GOLDEN["RICTOR_n_aligned"]


def test_pak2_and_ripk1_recompute_to_golden():
    rows = _recompute()
    assert abs(rows["PAK2"].reversal_score - GOLDEN["PAK2_reversal_pearson"]) < TOL
    assert abs(rows["RIPK1"].reversal_score - GOLDEN["RIPK1_reversal_pearson"]) < TOL


def test_rictor_reverses_pak2_does_not():
    rows = _recompute()
    assert rows["RICTOR"].reversal_score > 0.15
    assert abs(rows["PAK2"].reversal_score) < 0.05  # orthogonal


def test_demo_cli_runs_green():
    from perturbgate.cli import main
    assert main(["demo"]) == 0
