#!/usr/bin/env python3
"""Build the public, anonymised frozen artifacts + compact demo inputs from the
authoritative private research tree.

This script is the ONE place where the public repository touches the private
working tree. It reads only from generic, environment-configured roots and writes
only anonymised, derived, redistributable artifacts into the public repo. It never
hardcodes an internal path, hostname, username, scheduler id, or cluster name.

Environment (point these at the private research outputs to regenerate the frozen
package; NOT required for `make demo`, which reads the committed outputs):

    SERVER_RESULTS_ROOT   private `results/` directory (rictor_rescue/, rescue_screen/)
    SERVER_INPUTS_ROOT    private `inputs/responder_de/` directory (KD meta vectors)
    SERVER_DATA_ROOT      private genome-scale substrate dir (effect_vectors_*.parquet,
                          functional_table.csv) — optional; only needed to regenerate
                          the matched-perturbation null values.

Usage:
    SERVER_RESULTS_ROOT=/path/results \
    SERVER_INPUTS_ROOT=/path/inputs/responder_de \
    SERVER_DATA_ROOT=/path/substrate \
    python scripts/build_public_inputs.py

All outputs are per-gene aggregate statistics (log2 fold changes, correlations,
ranks) — no single-cell or donor-identifiable data is emitted.
"""
from __future__ import annotations

import gzip
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
DEMO = REPO / "data" / "demo"
REPRO = REPO / "data" / "reproduce"
FROZEN = REPO / "results" / "frozen"
SRCDATA = REPO / "figures" / "source_data"
for d in (DEMO, REPRO, FROZEN, SRCDATA):
    d.mkdir(parents=True, exist_ok=True)

CONDS = ["Rest", "Stim8hr", "Stim48hr"]
TARGETS = ["RICTOR", "PAK2", "RIPK1"]
TARGET_ENS = {"RICTOR": "ENSG00000164327", "PAK2": "ENSG00000180370", "RIPK1": "ENSG00000137275"}


def _root(var: str, required: bool = True) -> Path | None:
    v = os.environ.get(var)
    if not v:
        if required:
            sys.exit(f"[FATAL] set {var} to the private research path (see module docstring)")
        return None
    p = Path(v)
    if not p.exists():
        if required:
            sys.exit(f"[FATAL] {var}={v} does not exist")
        return None
    return p


def _write_gz_tsv(df: pd.DataFrame, path: Path) -> None:
    with gzip.open(path, "wt", encoding="utf-8", newline="") as fh:
        df.to_csv(fh, sep="\t", index=False)
    print(f"  wrote {path.relative_to(REPO)}  ({path.stat().st_size/1024:.0f} KB, {len(df)} rows)")


def _write_tsv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, sep="\t", index=False)
    print(f"  wrote {path.relative_to(REPO)}  ({path.stat().st_size/1024:.0f} KB, {len(df)} rows)")


def main() -> None:
    RES = _root("SERVER_RESULTS_ROOT")
    INP = _root("SERVER_INPUTS_ROOT")
    DATA = _root("SERVER_DATA_ROOT", required=False)
    RR = RES / "rictor_rescue"
    RS = RES / "rescue_screen"

    print("[1/8] Compact demo inputs (per-gene disease + KD vectors)")
    # Disease vector: activated_memory state only, minimal columns.
    dv = pd.read_csv(RR / "disease_vector_rawcount_full.tsv", sep="\t")
    dv = dv[dv.state == "activated_memory"][
        ["gene", "symbol", "mean_logfc", "donor_consistency", "disease_sign"]
    ].reset_index(drop=True)
    _write_gz_tsv(dv, DEMO / "disease_vector_activated_memory.tsv.gz")
    # KD responder-meta overall vectors (gene, lfc) for the three deep targets.
    for t in TARGETS:
        m = pd.read_csv(INP / "freeze" / f"meta_{t}_overall.tsv", sep="\t")[["gene", "lfc"]]
        _write_gz_tsv(m, DEMO / f"kd_meta_{t}.tsv.gz")

    print("[2/8] Level-2 reproduction inputs (pseudobulk + per-donor disease)")
    # Pseudobulk counts drive guide/condition/LODO/responder recomputation.
    pb = pd.read_parquet(INP / "pseudobulk_counts.parquet")
    pb.to_parquet(REPRO / "pseudobulk_counts.parquet")
    print(f"  wrote data/reproduce/pseudobulk_counts.parquet  ({(REPRO/'pseudobulk_counts.parquet').stat().st_size/1e6:.1f} MB)")
    pbm = pd.read_csv(INP / "pseudobulk_meta.tsv", sep="\t", index_col=0)
    pbm.to_csv(REPRO / "pseudobulk_meta.tsv", sep="\t")
    perdonor = pd.read_csv(RR / "disease_perdonor_logfc_activated_memory.tsv", sep="\t", index_col=0)
    with gzip.open(REPRO / "disease_perdonor_logfc_activated_memory.tsv.gz", "wt", encoding="utf-8", newline="") as fh:
        perdonor.to_csv(fh, sep="\t")
    print("  wrote data/reproduce/disease_perdonor_logfc_activated_memory.tsv.gz")

    print("[3/8] RICTOR robustness tables (guides, LODO, conditions)")
    g = pd.read_csv(RR / "guides.tsv", sep="\t")
    _write_tsv(g[g.target == "RICTOR"].reset_index(drop=True), FROZEN / "rictor_guides.tsv")
    lodo = pd.read_csv(RR / "lodo.tsv", sep="\t")
    _write_tsv(lodo, FROZEN / "rictor_lodo.tsv")
    cond = pd.read_csv(RR / "condition.tsv", sep="\t")
    _write_tsv(cond[cond.target == "RICTOR"].reset_index(drop=True), FROZEN / "rictor_conditions.tsv")

    print("[4/8] Matched-null summary + confound + safety")
    mn = pd.read_csv(RR / "matched_null.tsv", sep="\t")
    _write_tsv(mn, FROZEN / "matched_null.tsv")
    conf = pd.read_csv(RR / "confound_decomposition.tsv", sep="\t")
    _write_tsv(conf, FROZEN / "confound_decomposition.tsv")
    # Safety: flatten the verdict json safety block into a tidy per-metric table.
    verdict = json.load(open(RR / "rictor_rescue_verdict.json"))
    safety_rows = []
    for metric, d in verdict["safety"].items():
        safety_rows.append(
            dict(
                metric=metric,
                mean_delta_ko_minus_ntc=d["mean_delta"],
                worst_stratum=d["worst"],
                frac_strata_consistent=d["frac_strata_consistent"],
                direction=d["direction"],
            )
        )
    _write_tsv(pd.DataFrame(safety_rows), FROZEN / "safety_summary.tsv")

    print("[5/8] Leading-edge genes (descriptive)")
    le = pd.read_csv(RR / "leading_edge_reversed.tsv", sep="\t")
    le = le.rename(columns={"rictor_lfc": "kd_lfc"})[["symbol", "arm", "disease_logfc", "kd_lfc"]]
    _write_tsv(le, FROZEN / "leading_edge.tsv")

    print("[6/8] All-perturbation authoritative reversal + rejection ledger")
    scr = pd.read_csv(RS / "reversal_screen_full.tsv", sep="\t")
    led = pd.read_csv(RS / "REJECTION_LEDGER.tsv", sep="\t").set_index("pert")
    scr = scr.sort_values("combined", ascending=False).reset_index(drop=True)
    scr["global_rank"] = np.arange(1, len(scr) + 1)
    scr["global_percentile"] = (1.0 - (scr["global_rank"] - 1) / len(scr)) * 100.0
    breadth_p90 = scr["breadth_down"].quantile(0.90)

    deep_meta = {
        "RICTOR": dict(depth="DEEP", status="BOUNDED_RESCUE_8_OF_8_CRITERIA",
                       reason="retained_as_mechanism_node_with_modality_gap",
                       cls="RETAINED_MECHANISM_HYPOTHESIS"),
        "PAK2": dict(depth="DEEP", status="REJECTED_AFTER_DEEP_VALIDATION",
                     reason="reproducible_cellular_hit_not_therapeutically_directional",
                     cls="REJECTED_AFTER_DEEP_VALIDATION"),
        "RIPK1": dict(depth="DEEP", status="COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED",
                      reason="weak_incoherent_disease_reversal_in_this_analysis",
                      cls="COMPARATOR_ONLY"),
    }

    rows = []
    for _, r in scr.iterrows():
        pid, sym = r["pert"], r["symbol"]
        in_led = pid in led.index
        lr = led.loc[pid] if in_led else None
        conv = bool(r["convergent"])
        fdr = float(r["fdr_sign"])
        if conv and fdr < 0.10:
            screen_status = "CONVERGENT_FDR<0.10"
        elif fdr < 0.10:
            screen_status = "SIGNIFICANT_NOT_CONVERGENT"
        else:
            screen_status = "NOT_SIGNIFICANT"
        depth = "SHORTLIST_VETTED" if in_led else "SCREEN_ONLY"
        dvstatus = "NOT_EVALUATED"
        reason = str(lr["rejection_reason"]) if in_led else "NOT_ADVANCED_FROM_SCREEN"
        fclass = str(lr["final_label"]) if in_led else "NOT_ADVANCED_FROM_SCREEN"
        ess = (str(lr["isEssential"]) if in_led and "isEssential" in lr and pd.notna(lr["isEssential"]) else "")
        modality = (str(lr["external_verdict"]) if in_led and pd.notna(lr["external_verdict"]) else "")
        if sym in deep_meta:
            dm = deep_meta[sym]
            depth, dvstatus, reason, fclass = dm["depth"], dm["status"], dm["reason"], dm["cls"]
        rows.append(dict(
            perturbation_id=pid,
            gene_symbol=sym,
            reversal_score=round(float(r["rev_pearson"]), 6),
            combined_score=round(float(r["combined"]), 4),
            global_rank=int(r["global_rank"]),
            global_percentile=round(float(r["global_percentile"]), 2),
            effect_magnitude=int(r["n_reversed"] + r["n_reinforced"]),
            breadth=round(float(r["breadth_down"]), 4),
            donor_sign_consistency=round(float(r["donor_sign_consistency"]), 4),
            guide_concordance=round(float(r["guide_sign_concordance"]), 4),
            on_target_knockdown=round(float(r["ontarget_lfc"]), 4),
            broad_effect_flag=bool(r["hub_any"]) or (float(r["breadth_down"]) >= breadth_p90),
            essentiality_flag=ess,
            safety_flag=str(r["treg_liability"]) if str(r["treg_liability"]) != "none" else "",
            modality_flag=modality,
            screen_level_status=screen_status,
            evidence_depth=depth,
            deep_validation_status=dvstatus,
            primary_rejection_or_nonadvance_reason=reason,
            final_evidence_class=fclass,
            source_artifact="rescue_screen/reversal_screen_full+REJECTION_LEDGER",
        ))
    allpert = pd.DataFrame(rows)
    _write_tsv(allpert, FROZEN / "all_perturbations_authoritative_reversal.tsv")

    # Rejection ledger: the 25 deep-shortlist rows + the 3 deep-validated targets.
    led_pub = led.reset_index()[
        ["pert", "symbol", "combined", "rev_pearson", "external_verdict",
         "removed_at_stage", "rejection_reason", "final_label"]
    ].rename(columns={
        "pert": "perturbation_id", "symbol": "gene_symbol", "rev_pearson": "screen_reversal",
        "external_verdict": "external_layer_verdict", "removed_at_stage": "last_gate_reached",
        "final_label": "final_evidence_class",
    })
    led_pub.insert(2, "evidence_depth", "SHORTLIST_VETTED")
    led_pub.insert(3, "decision_scope", "SINGLE_STATE_SCREEN")
    deep_ledger = pd.DataFrame([
        dict(perturbation_id=TARGET_ENS["PAK2"], gene_symbol="PAK2", evidence_depth="DEEP",
             decision_scope="DEEP_CANDIDATE_VALIDATION", combined=np.nan, screen_reversal=-0.066,
             external_layer_verdict="activation_confounded_no_escape",
             last_gate_reached="therapeutic_directionality",
             rejection_reason="NOT_THERAPEUTICALLY_DIRECTIONAL;GENERIC_ACTIVATION_SUPPRESSION;PARTIAL_INHIBITION_NOT_ESTABLISHED",
             final_evidence_class="REJECTED_AFTER_DEEP_VALIDATION"),
        dict(perturbation_id=TARGET_ENS["RIPK1"], gene_symbol="RIPK1", evidence_depth="DEEP",
             decision_scope="COMPARATOR", combined=np.nan, screen_reversal=-0.033,
             external_layer_verdict="benchmark_comparator",
             last_gate_reached="disease_directionality",
             rejection_reason="COMPARATOR_ONLY;not_directionally_supported_in_this_analysis",
             final_evidence_class="COMPARATOR_ONLY"),
        dict(perturbation_id=TARGET_ENS["RICTOR"], gene_symbol="RICTOR", evidence_depth="DEEP",
             decision_scope="BOUNDED_PRESPECIFIED_RESCUE", combined=np.nan, screen_reversal=0.085,
             external_layer_verdict="modality_gap_unresolved",
             last_gate_reached="retained_mechanism_node",
             rejection_reason="RETAINED_MECHANISM_HYPOTHESIS;modality_and_independent_replication_unresolved",
             final_evidence_class="RETAINED_MECHANISM_HYPOTHESIS"),
    ])
    ledger = pd.concat([led_pub, deep_ledger], ignore_index=True)
    _write_tsv(ledger, FROZEN / "rejection_ledger.tsv")

    print("[7/8] Matched-null distribution values (Figure 2B; needs SERVER_DATA_ROOT)")
    if DATA is not None and (DATA / "functional_table.csv").exists():
        _matched_null_values(DATA, dv, allpert, verdict)
    else:
        print("  SKIPPED (SERVER_DATA_ROOT not set) — Figure 2B will use the frozen summary stats.")

    print("[8/8] Done. Frozen artifacts written to results/frozen and data/.")


def _matched_null_values(DATA: Path, dv: pd.DataFrame, allpert: pd.DataFrame, verdict: dict) -> None:
    """Recompute the 200 RICTOR-matched effect-vector reversal values so the null
    distribution in Figure 2B is real (not a fitted Gaussian)."""
    disease = pd.Series(dv["mean_logfc"].values, index=dv["gene"].values)
    ev = {}
    for c in CONDS:
        E = pd.read_parquet(DATA / f"effect_vectors_{c}.parquet")
        common = [g for g in E.columns if g in disease.index]
        d = disease[common].values.astype(float)
        Emat = E[common].values.astype(float)
        Ec = Emat - np.nanmean(Emat, axis=1, keepdims=True)
        dc = d - np.nanmean(d)
        num = np.nansum(Ec * dc, axis=1)
        den = np.sqrt(np.nansum(Ec ** 2, axis=1) * np.nansum(dc ** 2))
        r = np.where(den > 0, num / den, np.nan)
        ev[c] = pd.Series(-r, index=E.index)
    evrev = pd.DataFrame(ev)
    evrev["mean_reversal"] = evrev[CONDS].mean(axis=1)

    ft = pd.read_csv(DATA / "functional_table.csv").set_index("gene_id")
    feats = ["magnitude", "breadth", "donor_sign_consistency", "guide_sign_concordance", "ontarget_lfc"]

    def feat(g, base):
        return np.nanmean([ft.loc[g].get(f"{base}_{c}", np.nan) for c in CONDS])

    FEAT = pd.DataFrame({b: {g: feat(g, b) for g in ft.index} for b in feats})
    uni = [g for g in evrev.index if g in FEAT.index]
    Z = ((FEAT.loc[uni] - FEAT.loc[uni].mean()) / FEAT.loc[uni].std(ddof=0)).fillna(0.0)
    tgt = TARGET_ENS["RICTOR"]
    d2 = ((Z - Z.loc[tgt]) ** 2).sum(axis=1).drop(index=tgt)
    nn = d2.sort_values().index[:200]
    null = evrev.loc[nn, "mean_reversal"].dropna()
    obs = float(evrev.loc[tgt, "mean_reversal"])
    out = pd.DataFrame({"perturbation_id": null.index, "matched_reversal": null.values})
    out["exceeds_rictor"] = out["matched_reversal"] >= obs
    _write_tsv(out, FROZEN / "rictor_matched_null_values.tsv")
    # Also dump the 924-perturbation global effect-vector reversal for the global percentile panel.
    glob = evrev["mean_reversal"].dropna().reset_index()
    glob.columns = ["perturbation_id", "effectvector_reversal"]
    _write_tsv(glob, FROZEN / "effectvector_reversal_all.tsv")
    print(f"  RICTOR observed substrate reversal = {obs:+.4f}; {int(out.exceeds_rictor.sum())}/200 exceed it")


if __name__ == "__main__":
    main()
