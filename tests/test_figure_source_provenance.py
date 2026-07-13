"""Figure-provenance guards: every figure value must resolve to a committed artifact.

(1) Source-data TSVs that mirror a frozen table must equal that table byte-for-byte
    (catches figure/frozen drift).
(2) The RICTOR robustness figure: nine tracks must match their source frozen tables
    (no silent divergence), the two server-scale narrative anchors must be labelled,
    and every track must carry a non-empty source_artifact.
"""
import pandas as pd
import pytest

from perturbgate.io import frozen_dir, repo_root

# figure source_data stem -> frozen table it mirrors verbatim
MIRRORS = {
    "figure_3_gate_matrix": "gate_matrix",
    "supplementary_rictor_robustness": "rictor_robustness_tracks",
}


def _sd(stem):
    return repo_root() / "figures" / "source_data" / f"{stem}.tsv"


@pytest.mark.parametrize("sd_stem,frozen_name", MIRRORS.items())
def test_source_data_mirrors_frozen_table(sd_stem, frozen_name):
    sd = _sd(sd_stem)
    fz = frozen_dir() / f"{frozen_name}.tsv"
    assert sd.exists(), f"missing figure source data {sd}"
    # exact content equality (both are written with explicit LF)
    assert sd.read_bytes() == fz.read_bytes(), f"{sd_stem}.tsv drifted from {frozen_name}.tsv"


@pytest.fixture(scope="module")
def tracks():
    return pd.read_csv(frozen_dir() / "rictor_robustness_tracks.tsv", sep="\t")


def test_every_track_has_source_artifact(tracks):
    assert len(tracks) == 11
    assert tracks["source_artifact"].astype(str).str.strip().ne("").all()
    assert tracks["source_artifact"].notna().all()


def test_server_scale_anchors_are_labelled(tracks):
    anchors = tracks[tracks.track.isin(["adjusted-vector sensitivity", "responder-only mean"])]
    assert len(anchors) == 2
    assert anchors["source_artifact"].str.contains("narrative anchor").all()
    assert anchors["source_artifact"].str.contains("not recomputed at Level 1").all()


@pytest.fixture(scope="module")
def sensitivities():
    return pd.read_csv(frozen_dir() / "rictor_server_scale_sensitivities.tsv", sep="\t")


def test_anchor_values_match_server_scale_export(tracks, sensitivities):
    """The two anchor values in the tracks table must equal the frozen server-scale
    sensitivity export — the same verify-against-source guarantee as the nine derived tracks."""
    sens = sensitivities.set_index("track")
    for track in ["adjusted-vector sensitivity", "responder-only mean"]:
        tv = float(tracks.loc[tracks.track == track, "reversal"].iloc[0])
        sv = round(float(sens.loc[track, "reversal"]), 6)
        assert abs(tv - sv) < 1e-6, f"{track}: tracks {tv} != export {sv}"


def test_server_scale_export_carries_full_provenance(sensitivities):
    assert set(sensitivities.track) == {"adjusted-vector sensitivity", "responder-only mean"}
    for col in ["source_artifact", "source_artifact_sha256", "source_run_commit",
                "analysis_scope", "reproducibility_level"]:
        assert sensitivities[col].astype(str).str.strip().ne("").all(), f"empty {col}"
    # sha256 is a real 64-hex digest; run commit is a 40-hex git sha
    assert sensitivities["source_artifact_sha256"].str.fullmatch(r"[0-9a-f]{64}").all()
    assert sensitivities["source_run_commit"].str.fullmatch(r"[0-9a-f]{40}").all()
    # wording preserved: same-cohort Level-3 sensitivity, not independent validation, not Level-1
    assert sensitivities["reproducibility_level"].str.contains("Level 3").all()
    assert sensitivities["reproducibility_level"].str.contains("not recomputed at Level 1").all()
    assert sensitivities["analysis_scope"].str.contains("not independent validation").all()


def test_derived_tracks_match_their_frozen_sources(tracks):
    """The nine non-anchor tracks must equal the values in their cited frozen tables."""
    def val(track):
        return float(tracks.loc[tracks.track == track, "reversal"].iloc[0])

    pc = pd.read_csv(frozen_dir() / "primary_comparison.tsv", sep="\t")
    r = pc[pc.target == "RICTOR"].iloc[0]
    lodo = pd.read_csv(frozen_dir() / "rictor_lodo.tsv", sep="\t")
    folds = lodo[lodo.fold != "ALL"]["reversal_pearson"].astype(float)
    conf = pd.read_csv(frozen_dir() / "confound_decomposition.tsv", sep="\t")
    cr = float(conf[conf.removed == "cellcycle+activation+broaddown"]["reversal_pearson"].iloc[0])

    expected = {
        "primary raw-count vector": float(r["primary_reversal"]),
        "RICTOR guide 1": float(r["guide_1_reversal"]),
        "RICTOR guide 2": float(r["guide_2_reversal"]),
        "disease-donor LODO (11)": float(folds.mean()),
        "condition: Rest": float(r["condition_rest"]),
        "condition: Stim8hr": float(r["condition_stim8"]),
        "condition: Stim48hr": float(r["condition_stim48"]),
        "confound-removed (cc+act+broad)": float(cr),
        "matched-null substrate": float(r["matched_substrate_reversal"]),
    }
    for track, exp in expected.items():
        assert abs(val(track) - round(exp, 6)) < 1e-6, f"{track}: table {val(track)} != source {round(exp,6)}"

    # LODO range in the table must match the folds' min/max
    row = tracks.loc[tracks.track == "disease-donor LODO (11)"].iloc[0]
    assert abs(float(row["range_low"]) - round(folds.min(), 6)) < 1e-6
    assert abs(float(row["range_high"]) - round(folds.max(), 6)) < 1e-6
