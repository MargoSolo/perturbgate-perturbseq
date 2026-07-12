#!/usr/bin/env python3
"""Author the curated frozen artifacts (comparison, funnel, gate matrix, ablation,
claims, superseded claims, analysis contract).

Unlike ``build_public_inputs.py`` (which mechanically transforms private tables),
these files encode curated decisions and controlled-vocabulary labels. Every value
here traces to an authoritative artifact recorded in ``docs/SOURCE_SNAPSHOT.md``;
this script is the single place they are defined so tables, figures and docs stay
consistent. It reads nothing private and can run anywhere.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
FROZEN = REPO / "results" / "frozen"
FROZEN.mkdir(parents=True, exist_ok=True)

NA = ""  # explicit "not applicable / not evaluated" marker in TSVs


def write_tsv(rows: list[dict], name: str) -> None:
    df = pd.DataFrame(rows)
    df.to_csv(FROZEN / name, sep="\t", index=False)
    print(f"  wrote results/frozen/{name}  ({len(df)} rows)")


def write_json(obj, name: str) -> None:
    with open(FROZEN / name, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  wrote results/frozen/{name}")


# =====================================================================
# 1. primary_comparison.tsv
# =====================================================================
primary_comparison = [
    dict(
        target="RICTOR",
        final_public_label="DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP",
        primary_reversal=0.1606, primary_pearson_p=1.8e-63, primary_spearman_reversal=0.1000,
        gsea_reversal=1.844, guide_1_reversal=0.1410, guide_2_reversal=0.1781,
        disease_lodo_positive=11, disease_lodo_total=11,
        responder_support="yes_93pct_strata_all_donors",
        condition_rest=0.1532, condition_stim8=0.0916, condition_stim48=0.0422,
        matched_substrate_reversal=0.1314, matched_percentile=96.5, matched_empirical_p=0.0398,
        matched_ci_low=0.0171, matched_ci_high=0.0705, confound_resistant="yes",
        safety_summary="mild_donor_inconsistent_early_tox_flag;T_and_Treg_identity_preserved",
        modality_summary="mTORC2_scaffold;no_selective_small_molecule_modality",
        final_decision="RETAINED_AS_MECHANISM_HYPOTHESIS",
        principal_limitation="matched_null_borderline_finite_pool_to_0.07;synovium_vs_blood_not_disease_vs_healthy;no_independent_replication;modality_gap",
    ),
    dict(
        target="PAK2",
        final_public_label="REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL",
        primary_reversal=0.0100, primary_pearson_p=0.297, primary_spearman_reversal=0.0058,
        gsea_reversal=1.134, guide_1_reversal=-0.0300, guide_2_reversal=0.0885,
        disease_lodo_positive=NA, disease_lodo_total=NA,
        responder_support="no",
        condition_rest=-0.0283, condition_stim8=-0.0023, condition_stim48=0.0644,
        matched_substrate_reversal=-0.0308, matched_percentile=41.3, matched_empirical_p=0.672,
        matched_ci_low=NA, matched_ci_high=NA, confound_resistant="no_activation_confounded",
        safety_summary="specific_non_toxic",
        modality_summary="kinase_but_not_directionally_supported",
        final_decision="REJECTED_NOT_THERAPEUTICALLY_DIRECTIONAL",
        principal_limitation="real_reproducible_cellular_hit;external_JIA_enrichment_activation_confounded;partial_inhibition_not_established",
    ),
    dict(
        target="RIPK1",
        final_public_label="COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS",
        primary_reversal=0.0377, primary_pearson_p=8.68e-05, primary_spearman_reversal=0.0534,
        gsea_reversal=0.100, guide_1_reversal=0.0124, guide_2_reversal=0.0762,
        disease_lodo_positive=NA, disease_lodo_total=NA,
        responder_support=NA,
        condition_rest=NA, condition_stim8=NA, condition_stim48=0.0503,
        matched_substrate_reversal=-0.0293, matched_percentile=42.2, matched_empirical_p=0.672,
        matched_ci_low=NA, matched_ci_high=NA, confound_resistant=NA,
        safety_summary="full_LoF_immunodeficiency;kinase_inhibition_is_the_modality",
        modality_summary="clinical_stage_kinase_inhibitors_exist_benchmark",
        final_decision="COMPARATOR_ONLY",
        principal_limitation="weak_incoherent_disease_reversal_here;benchmark_comparator_not_nominated_by_this_test",
    ),
]
write_tsv(primary_comparison, "primary_comparison.tsv")

# =====================================================================
# 2. candidate_funnel.tsv  (branching decision map, not a linear funnel)
# =====================================================================
CMD_SCREEN = "perturbgate demo (rescue_screen substrate)"
funnel = [
    dict(stage_id="S0", stage_name="Screen-level reversal scoring", scope="SCREEN_WIDE",
         denominator_definition="all perturbations with a usable genome-scale effect vector",
         n_entering=924, n_advanced=208, n_not_advanced=716, n_rejected=0, n_unresolved=0,
         principal_reason_categories="NO_MEASURABLE_EFFECT;NOT_ADVANCED_FROM_SCREEN",
         source_artifact="results/frozen/all_perturbations_authoritative_reversal.tsv",
         generating_command=CMD_SCREEN),
    dict(stage_id="S1", stage_name="Biological robustness (donor-consistent subvector + bootstrap + jackknife)",
         scope="SCREEN_WIDE",
         denominator_definition="convergent (Pearson & Spearman & GSEA) and FDR<0.10 screen hits",
         n_entering=208, n_advanced=21, n_not_advanced=187, n_rejected=0, n_unresolved=0,
         principal_reason_categories="BROAD_TRANSCRIPTIONAL_EFFECT;DONOR_UNSTABLE",
         source_artifact="results/frozen/rejection_ledger.tsv",
         generating_command=CMD_SCREEN),
    dict(stage_id="S2", stage_name="Safety / essentiality / tractability / modality (external layer)",
         scope="SCREEN_WIDE",
         denominator_definition="biologically robust screen shortlist",
         n_entering=21, n_advanced=0, n_not_advanced=0, n_rejected=21, n_unresolved=0,
         principal_reason_categories="ESSENTIALITY_OR_SAFETY_LIABILITY;NO_CREDIBLE_MODALITY;BROAD_TRANSCRIPTIONAL_EFFECT",
         source_artifact="results/frozen/rejection_ledger.tsv",
         generating_command=CMD_SCREEN),
    dict(stage_id="D0", stage_name="PAK2 deep candidate validation (responder / guide / donor / disease)",
         scope="CANDIDATE_SPECIFIC",
         denominator_definition="lead candidate carried from the prior robustness spine",
         n_entering=1, n_advanced=0, n_not_advanced=0, n_rejected=1, n_unresolved=0,
         principal_reason_categories="NOT_THERAPEUTICALLY_DIRECTIONAL;GENERIC_ACTIVATION_SUPPRESSION;PARTIAL_INHIBITION_NOT_ESTABLISHED",
         source_artifact="results/frozen/primary_comparison.tsv",
         generating_command="deep PAK2 branch (technical vs therapeutic validation)"),
    dict(stage_id="R0", stage_name="RICTOR bounded pre-specified rescue (8 criteria)",
         scope="CANDIDATE_SPECIFIC",
         denominator_definition="separate bounded rescue on the corrected raw-count disease vector",
         n_entering=1, n_advanced=1, n_not_advanced=0, n_rejected=0, n_unresolved=0,
         principal_reason_categories="RETAINED_MECHANISM_HYPOTHESIS",
         source_artifact="results/frozen/rictor_guides.tsv;rictor_lodo.tsv;rictor_conditions.tsv;matched_null.tsv",
         generating_command="perturbgate demo (RICTOR rescue)"),
    dict(stage_id="C0", stage_name="RIPK1 comparator", scope="CANDIDATE_SPECIFIC",
         denominator_definition="benchmark comparator perturbation",
         n_entering=1, n_advanced=0, n_not_advanced=1, n_rejected=0, n_unresolved=0,
         principal_reason_categories="COMPARATOR_ONLY",
         source_artifact="results/frozen/primary_comparison.tsv",
         generating_command="perturbgate demo (comparator)"),
]
write_tsv(funnel, "candidate_funnel.tsv")

# =====================================================================
# 3. gate_matrix.tsv
# =====================================================================
gate_cols = [
    "measurable_cellular_effect", "responder_support", "guide_concordance",
    "perturbation_donor_robustness", "disease_directionality", "disease_donor_lodo",
    "matched_null_support", "confound_resistance", "safety_essentiality",
    "human_genetic_direction", "credible_modality", "final_public_decision",
]
gate_rows = [
    dict(row_label="RICTOR", measurable_cellular_effect="PASS", responder_support="PASS",
         guide_concordance="PASS", perturbation_donor_robustness="PASS",
         disease_directionality="PASS", disease_donor_lodo="PASS", matched_null_support="BORDERLINE",
         confound_resistance="PASS", safety_essentiality="BORDERLINE", human_genetic_direction="NOT_EVALUATED",
         credible_modality="TRANSLATIONAL_GAP", final_public_decision="RETAINED_MECHANISM_NODE"),
    dict(row_label="PAK2", measurable_cellular_effect="PASS", responder_support="PASS",
         guide_concordance="PASS", perturbation_donor_robustness="PASS",
         disease_directionality="FAIL", disease_donor_lodo="NOT_EVALUATED", matched_null_support="FAIL",
         confound_resistance="FAIL", safety_essentiality="PASS", human_genetic_direction="NOT_ESTABLISHED",
         credible_modality="NOT_ESTABLISHED", final_public_decision="REJECTED"),
    dict(row_label="RIPK1", measurable_cellular_effect="PASS", responder_support="NOT_EVALUATED",
         guide_concordance="BORDERLINE", perturbation_donor_robustness="NOT_EVALUATED",
         disease_directionality="FAIL", disease_donor_lodo="NOT_EVALUATED", matched_null_support="FAIL",
         confound_resistance="NOT_EVALUATED", safety_essentiality="FAIL", human_genetic_direction="PASS",
         credible_modality="PASS", final_public_decision="COMPARATOR_ONLY"),
    dict(row_label="broad / essential hubs (aggregate)", measurable_cellular_effect="PASS",
         responder_support="NOT_EVALUATED", guide_concordance="PASS", perturbation_donor_robustness="PASS",
         disease_directionality="BORDERLINE", disease_donor_lodo="NOT_EVALUATED", matched_null_support="NOT_EVALUATED",
         confound_resistance="FAIL", safety_essentiality="FAIL", human_genetic_direction="NOT_EVALUATED",
         credible_modality="NOT_ESTABLISHED", final_public_decision="SAFETY_CONSTRAINED"),
    dict(row_label="immune-directional TFs, no modality (aggregate)", measurable_cellular_effect="PASS",
         responder_support="NOT_EVALUATED", guide_concordance="PASS", perturbation_donor_robustness="PASS",
         disease_directionality="PASS", disease_donor_lodo="NOT_EVALUATED", matched_null_support="NOT_EVALUATED",
         confound_resistance="BORDERLINE", safety_essentiality="BORDERLINE", human_genetic_direction="PASS",
         credible_modality="FAIL", final_public_decision="EXPLORATORY_NO_MODALITY"),
]
write_tsv(gate_rows, "gate_matrix.tsv")

# =====================================================================
# 4. gate_ablation.tsv  (process ablation on frozen decisions only)
# =====================================================================
ablation = [
    dict(gate_removed="therapeutic_directionality",
         what_would_survive="a real, reproducible cellular hit with no disease reversal",
         example_entities="PAK2",
         why_misleading="PAK2 passes every technical gate; without the directionality gate it would read as advanceable",
         frozen_evidence="results/frozen/primary_comparison.tsv (PAK2 reversal +0.010, p=0.297)"),
    dict(gate_removed="broad_effect_and_essentiality_controls",
         what_would_survive="broad chromatin / RNA / essential-machinery reversers",
         example_entities="GNAS,STAT3,SMARCB1,TET2",
         why_misleading="high reversal driven by nonspecific broad suppression, not disease-specific biology",
         frozen_evidence="results/frozen/rejection_ledger.tsv (final_evidence_class=SAFETY_CONSTRAINED)"),
    dict(gate_removed="modality_review",
         what_would_survive="immune-directional but undruggable transcription factors",
         example_entities="KLF13,IRF9,ELF4",
         why_misleading="real immune-directional reversal + immune genetics, but no credible small-molecule modality",
         frozen_evidence="results/frozen/rejection_ledger.tsv (external_layer_verdict=NO_CREDIBLE_MODALITY)"),
    dict(gate_removed="finite_null_uncertainty_reporting",
         what_would_survive="RICTOR matched-null significance read as decisive",
         example_entities="RICTOR",
         why_misleading="point estimate p=0.040 looks firm, but the Wilson/bootstrap CI on 7/200 grazes 0.05-0.07",
         frozen_evidence="results/frozen/matched_null.tsv + rictor_matched_null_values.tsv"),
    dict(gate_removed="confound_decomposition",
         what_would_survive="reversal mistaken for generic activation / broad suppression",
         example_entities="RICTOR",
         why_misleading="without module-removal, a reversal could be dismissed as (or inflated by) nonspecific suppression",
         frozen_evidence="results/frozen/confound_decomposition.tsv (cell-cycle/activation removal delta ~ 0)"),
]
write_tsv(ablation, "gate_ablation.tsv")

# =====================================================================
# 5. claims.json  (every headline claim -> evidence -> artifact)
# =====================================================================
DISEASE_MD5 = "2b18d92684db1f70b637e1f098374c7e"  # authoritative raw-count disease vector
claims = [
    dict(
        claim_id="CLAIM-RICTOR-01",
        exact_public_wording=(
            "RICTOR knockdown reverses the corrected activated-memory JIA synovium-vs-blood "
            "disease direction at +0.161 centered-Pearson (r^2 ~ 2.6%); it is retained as a "
            "disease-reversing mechanism node with a modality gap, not a validated drug target."
        ),
        entity="RICTOR", claim_type="mechanism_hypothesis",
        evidence_status="supported_bounded", evidence_depth="DEEP",
        supporting_artifacts=[
            "results/frozen/primary_comparison.tsv",
            "results/frozen/rictor_guides.tsv",
            "results/frozen/rictor_lodo.tsv",
            "results/frozen/rictor_conditions.tsv",
            "results/frozen/matched_null.tsv",
            "results/frozen/confound_decomposition.tsv",
        ],
        supporting_metrics=dict(
            primary_reversal=0.1606, pearson_p=1.8e-63, guides=[0.1410, 0.1781],
            lodo_positive="11/11", conditions=[0.1532, 0.0916, 0.0422],
            matched_percentile=96.5, matched_empirical_p=0.0398,
        ),
        denominator="10832 aligned genes; 11 paired disease donors; 924-perturbation matched pool (k=200)",
        uncertainty="matched-null p 95% CI (Wilson) 0.017-0.070; finite pool of 200 controls",
        limitations=[
            "matched-null is the weakest of the 8 criteria (borderline)",
            "synovium-vs-blood is not disease-vs-healthy tissue",
            "no independent same-tissue replication",
            "mTORC2 scaffold: no selective small-molecule modality (modality gap)",
        ],
        superseded_claims=["SUP-01"],
        generating_command="perturbgate demo && perturbgate verify",
        code_version="1.0.0",
        input_checksums=dict(disease_vector_md5=DISEASE_MD5),
    ),
    dict(
        claim_id="CLAIM-PAK2-01",
        exact_public_wording=(
            "PAK2 is a real, reproducible CD4 T-cell perturbation hit that is NOT therapeutically "
            "directional: it does not reverse the disease state (+0.010, p=0.297, n.s.), its apparent "
            "external JIA enrichment is activation-confounded, and partial-inhibition sufficiency was "
            "not established. PAK2 is rejected as a target nomination."
        ),
        entity="PAK2", claim_type="negative_result",
        evidence_status="rejected_after_deep_validation", evidence_depth="DEEP",
        supporting_artifacts=[
            "results/frozen/primary_comparison.tsv",
            "results/frozen/matched_null.tsv",
            "results/frozen/rejection_ledger.tsv",
        ],
        supporting_metrics=dict(
            primary_reversal=0.0100, pearson_p=0.297, matched_percentile=41.3,
            responder_fraction=0.765, guide_concordance=0.85, knockdown_pct="83-86",
        ),
        denominator="10832 aligned genes; responder Mixscape on 11/12 retained subsets; 112-gene frozen programme",
        uncertainty="cellular effect is real and reproducible; therapeutic direction is absent, not merely weak",
        limitations=[
            "112-gene programme is reproducible but weakly coherent",
            "JIA surrogate is synovium-vs-blood, not adult RA disease-vs-healthy",
        ],
        superseded_claims=["SUP-02", "SUP-03", "SUP-04", "SUP-05"],
        generating_command="perturbgate demo && perturbgate verify",
        code_version="1.0.0",
        input_checksums=dict(disease_vector_md5=DISEASE_MD5),
    ),
    dict(
        claim_id="CLAIM-RIPK1-01",
        exact_public_wording=(
            "RIPK1 is retained only as a comparator that is not directionally supported by this "
            "disease-reversal test (+0.038, incoherent GSEA, matched-null 42nd percentile)."
        ),
        entity="RIPK1", claim_type="comparator",
        evidence_status="not_directionally_supported", evidence_depth="DEEP",
        supporting_artifacts=["results/frozen/primary_comparison.tsv", "results/frozen/matched_null.tsv"],
        supporting_metrics=dict(primary_reversal=0.0377, gsea_reversal=0.100, matched_percentile=42.2),
        denominator="10832 aligned genes; single-condition (Stim48hr) coverage only",
        uncertainty="benchmark comparator; not nominated or rejected by this specific test",
        limitations=["known Screen-8 benchmark, not a candidate from this analysis"],
        superseded_claims=[],
        generating_command="perturbgate demo && perturbgate verify",
        code_version="1.0.0",
        input_checksums=dict(disease_vector_md5=DISEASE_MD5),
    ),
    dict(
        claim_id="CLAIM-PROCESS-01",
        exact_public_wording=(
            "PerturbGate preserves negative and superseded results: candidate attrition, detected "
            "confounds, and corrected interpretations are first-class, auditable outputs, not hidden "
            "debugging history."
        ),
        entity="pipeline", claim_type="process",
        evidence_status="supported", evidence_depth="ARTIFACT",
        supporting_artifacts=[
            "results/frozen/candidate_funnel.tsv",
            "results/frozen/rejection_ledger.tsv",
            "results/frozen/gate_ablation.tsv",
            "results/frozen/superseded_claims.json",
        ],
        supporting_metrics=dict(perturbations=924, funnel_stages=6, superseded_claims=5),
        denominator="924 perturbations; 6 documented decision stages",
        uncertainty="none (process claim)",
        limitations=["counts are traceable to frozen artifacts only; not every perturbation was deep-validated"],
        superseded_claims=[],
        generating_command="perturbgate verify",
        code_version="1.0.0",
        input_checksums={},
    ),
]
write_json(claims, "claims.json")

# =====================================================================
# 6. superseded_claims.json
# =====================================================================
superseded = [
    dict(id="SUP-01", entity="RICTOR",
         old_wording="RICTOR reversal ~ +0.43",
         source_artifact="old covariate-adjusted / residency-removed 77-gene subset (superseded)",
         reason_superseded="inflated by a frozen-subset gene universe and a responder-only KD representation",
         authoritative_replacement=("full-transcriptome responder-resolved centered-Pearson reversal +0.161; "
                                     "conservative all-cell null-substrate projection +0.131"),
         replacement_artifact="results/frozen/primary_comparison.tsv;results/frozen/matched_null.tsv",
         may_appear_in_readme=False),
    dict(id="SUP-02", entity="PAK2",
         old_wording="PAK2 programme is enriched in JIA joint tissue (positive disease validation)",
         source_artifact="raw synovial enrichment (all modules up)",
         reason_superseded="UP and DOWN modules co-elevate under covariate adjustment + matched-null: generic activation confound",
         authoritative_replacement="not disease-directionally supported (disease_relevant=False)",
         replacement_artifact="results/frozen/primary_comparison.tsv",
         may_appear_in_readme=False),
    dict(id="SUP-03", entity="PAK2",
         old_wording="partial PAK2 inhibition is supported / bounded partial support",
         source_artifact="two-guide analysis interpreted as titration",
         reason_superseded="both guides produce similarly strong knockdown (~83-86%); no strong-vs-weak axis",
         authoritative_replacement="partial-inhibition sufficiency NOT_ESTABLISHED",
         replacement_artifact="results/frozen/rejection_ledger.tsv",
         may_appear_in_readme=False),
    dict(id="SUP-04", entity="PAK2",
         old_wording="a safer PAK2 neighbour reproduces the programme",
         source_artifact="global-cosine neighbour search (PTEN etc.)",
         reason_superseded="gene-ID namespace mismatch and incomplete essentiality/safety vetoes; corrected search finds none",
         authoritative_replacement="no safer, druggable, immune-directional escape target identified",
         replacement_artifact="results/frozen/rejection_ledger.tsv",
         may_appear_in_readme=False),
    dict(id="SUP-05", entity="PAK2",
         old_wording="PAK2-WASF2 is a supported therapeutic axis",
         source_artifact="structural / topology exploration (AF2/AF3)",
         reason_superseded="structural + directional evidence did not establish a high-confidence direct therapeutic interface",
         authoritative_replacement="not a validated therapeutic axis; structural work is not the target-discovery result",
         replacement_artifact="docs/SUPERSEDED_RESULTS.md",
         may_appear_in_readme=False),
]
write_json(superseded, "superseded_claims.json")

# =====================================================================
# 7. analysis_contract.json
# =====================================================================
contract = dict(
    primary_hypothesis=("A perturbation is a candidate mechanism node only if its knockdown reverses a "
                        "donor-paired disease-state direction and survives guide, donor, condition, "
                        "matched-null and confound checks."),
    primary_disease_vector=dict(
        name="JIA synovium-vs-blood, activated-memory CD4, raw-count donor-paired pseudobulk",
        state="activated_memory", md5="2b18d92684db1f70b637e1f098374c7e",
        n_paired_donors=11, n_genes=12071, residency_regressed=False,
        source="CZ CELLxGENE collection 10eb236d-d42d-45b8-8363-c2dcf865f388 (CC-BY-4.0)"),
    primary_state="activated_memory",
    sign_convention="reversal = -centered_Pearson(KD_log2FC, disease_log2FC); >0 reversing, <0 mimicking",
    target_comparison_set=["RICTOR", "PAK2", "RIPK1"],
    gene_universe=dict(
        primary="responder-DE donor random-effects meta KD vector, full transcriptome (10832 aligned genes)",
        null_substrate="genome-scale all-cell effect vectors (mean of conditions), 7393-gene intersection"),
    representations=dict(
        primary="responder-resolved donor-RE meta (reversal +0.161)",
        conservative="all-cell effect-vector projection (reversal +0.131, used only for null calibration)"),
    rictor_criteria=[
        "1. centered-Pearson reversal > 0",
        "2. Spearman reversal > 0",
        "3. ranked-GSEA reversal in the same direction",
        "4. both RICTOR guides positive",
        "5. all disease-donor leave-one-out folds positive",
        "6. responder-only support",
        "7. positive in all three conditions",
        "8. above the matched-perturbation null at the frozen point estimate",
    ],
    matched_null=dict(
        features=["magnitude", "breadth", "donor_sign_consistency", "guide_sign_concordance", "ontarget_lfc"],
        pool_size=200, k_nearest=200, unique_matched=200, n_exceed_rictor=7,
        empirical_p=0.0398, seed_range=[0.032, 0.042], pooled_mc_p=0.0339,
        wilson_95ci=[0.0171, 0.0705], mc_bootstrap_95ci=[0.0149, 0.0647],
        note=("Criterion 8 is the WEAKEST criterion. Do not write '8/8 decisive'. "
              "Preferred: 'RICTOR satisfied seven strong convergence checks and nominally exceeded a "
              "matched-perturbation null, with borderline finite-pool uncertainty.'")),
    random_seeds=dict(scoring=0, matched_null=0, monte_carlo_seeds=list(range(20))),
    exclusion_rules=[
        "genes with non-finite KD or disease log2FC dropped before correlation",
        "reversal undefined below 200 shared finite genes",
        "superseded vectors (old +0.43 / 77-gene / residency-removed) never used as primary",
    ],
    final_labels=[
        "DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP",
        "REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL",
        "COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS",
    ],
    superseded_analyses=["SUP-01", "SUP-02", "SUP-03", "SUP-04", "SUP-05"],
    confirmatory_vs_exploratory=dict(
        confirmatory=["RICTOR 8-criterion bounded rescue (pre-specified)", "PAK2 four-criterion decision gate"],
        exploratory=["single-state 924-perturbation reversal screen (NO_ROBUST_CANDIDATE)",
                     "old-vector sensitivity analysis (same cohort, not independent replication)"]),
)
write_json(contract, "analysis_contract.json")

print("Curated frozen tables + JSON written.")

