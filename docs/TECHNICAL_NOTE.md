# Technical note

**PerturbGate — an evidence-gated pipeline for T-cell Perturb-seq mechanism hypotheses**

PerturbGate v1.0.0 (frozen hackathon release, 2026-07-13). Prepared for *Built with Claude: Life Sciences* (Anthropic x Gladstone Institutes), Research track: "Find new drug targets in a T-cell Perturb-seq dataset from the Marson and Pritchard labs."

Sibling documents: [Results](RESULTS.md), [Decision trail](DECISION_TRAIL.md), [Claims and evidence](CLAIMS_AND_EVIDENCE.md), [Failure modes](FAILURE_MODES.md), [Limitations](LIMITATIONS.md), [Superseded results](SUPERSEDED_RESULTS.md), [Reproducibility](REPRODUCIBILITY.md), [Reproducibility levels](REPRODUCIBILITY_LEVELS.md).

---

## Abstract

A measurable perturbation effect is necessary but not sufficient to nominate a drug target. We built PerturbGate, an evidence-gated pipeline that scores whether a CD4+ T-cell CRISPRi knockdown reverses a donor-paired disease-state transcriptional direction, and that treats candidate attrition, detected confounds, and superseded interpretations as first-class outputs rather than hidden history. Against a juvenile idiopathic arthritis (JIA) synovium-versus-blood disease vector in activated-memory CD4 cells (11 paired donors, 12,071 genes), one perturbation — RICTOR — reversed the disease direction at a responder-resolved centered-Pearson reversal of +0.161 (p = 1.8e-63, r^2 ~ 2.6%, 10,832 aligned genes) and satisfied seven strong convergence checks (both guides, 11/11 disease-donor folds, all three activation conditions, ranked-GSEA direction, Spearman sign, responder-only support). It nominally exceeded a covariate-matched perturbation null in the conservative all-cell substrate (+0.131, 96.5th percentile; 7 of 200 matched controls exceeded it; empirical p = 0.040, Wilson 95% CI 0.017–0.070), with borderline finite-pool uncertainty at the eighth criterion. RICTOR is retained as `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` — a mechanism hypothesis, not a validated drug target, and with no selective small-molecule modality. In contrast, PAK2 passed every technical-validation gate (on-target knockdown ~83–86%, guide concordance 0.85, reproducible 112-gene responder programme) yet did not reverse disease (+0.010, p = 0.297, n.s.) and was rejected as `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL`. RIPK1, a benchmark comparator, was not directionally supported by this test (+0.038, 42nd matched-null percentile). PerturbGate's contribution is the retained record of how competing claims failed, not the discovery of a single positive hit.

## Background

Perturb-seq screens generate thousands of reproducible transcriptional phenotypes. Most are not therapeutically actionable: a knockdown can produce a robust, on-target, donor-consistent cellular signature and still push the cell in a direction orthogonal to — or reinforcing — a disease state. Gene-ranking framings reward the size and reproducibility of an effect. Target *nomination* requires an additional, directional, disease-anchored question: does the perturbation move cells *away* from the pathogenic state, and does that survive confound, donor, and null-model scrutiny?

PerturbGate is built around that distinction. It reframes the challenge from gene ranking to target nomination and enforces an explicit sequence of gates. The central operational finding is negative in spirit: the pipeline "succeeded" not by surfacing a positive hit but by producing an auditable record of why most candidates — including a technically flawless one (PAK2) — do not qualify. This note documents the contract, the methods, the attrition, the two decisive case studies (PAK2 rejection, RICTOR bounded retention), the negative controls, and the translational boundary.

## Data

Two open datasets underlie every result (`data/public_data_manifest.tsv`, `NOTICE`). Derived per-gene aggregate vectors are committed to the repository; redistribution is permitted with attribution.

1. **Primary CD4+ T-cell Perturb-seq** (Marson lab and Pritchard lab). Genome-scale CRISPRi in primary human CD4+ T cells across resting and stimulated conditions. bioRxiv DOI 10.64898/2025.12.23.696273; CZI Virtual Cell Models; processed matrices on public S3 (`s3://genome-scale-tcell-perturb-seq/`, no registration required for processed data); raw reads GEO GSE314342 / SRA SRP643211. License MIT (redistribution permitted).
2. **JIA synovial single-cell atlas** ("Integrated global cells"; Knight et al., bioRxiv DOI 10.64898/2026.05.01.716870; companion Bolton/Mahony et al., *Science Translational Medicine* 2025, DOI 10.1126/scitranslmed.adt6050). CZ CELLxGENE collection `10eb236d-d42d-45b8-8363-c2dcf865f388`. License CC-BY-4.0; fully open, no registration.

**Disease vector.** The primary disease direction is JIA synovium (synovial tissue and fluid) versus blood, restricted to activated-memory CD4 T cells, built from raw-count donor-paired pseudobulk. Per donor we compute per-gene log2((CPM_syn + 1)/(CPM_blood + 1)) and meta-analyze across 11 paired donors over the full transcriptome (12,071 genes). Tissue residency is **not** regressed out. The frozen vector has md5 `2b18d92684db1f70b637e1f098374c7e` (`results/frozen/analysis_contract.json`). Synovium-versus-blood is a compartment contrast, **not** disease-versus-healthy tissue; this bounds every downstream interpretation (see Translational boundary).

## Analysis contract

The primary hypothesis was pre-registered in `results/frozen/analysis_contract.json`: *a perturbation is a candidate mechanism node only if its knockdown reverses a donor-paired disease-state direction and survives guide, donor, condition, matched-null, and confound checks.*

- **Sign convention:** `reversal = -centered_Pearson(KD_log2FC, disease_log2FC)`; > 0 reverses the disease direction, < 0 mimics it.
- **Two substrates, never silently mixed.** (i) The **primary responder-resolved** vector — a responder-DE, donor random-effects meta knockdown vector over the full transcriptome (10,832 aligned genes), which yields RICTOR reversal +0.161. (ii) A **conservative all-cell effect-vector projection** (7,393-gene intersection), used **only** to calibrate against the matched null in the same feature space, which yields RICTOR reversal +0.131. The +0.030 gap between substrates decomposes into −0.036 (narrower gene universe) and +0.066 (responder-to-all-cell representation); the all-cell number is the conservative one (`results/frozen/confound_decomposition.tsv`, facts in the contract).
- **Confirmatory vs exploratory (pre-specified in the contract).** Confirmatory: the RICTOR eight-criterion bounded rescue and the PAK2 decision gate. Exploratory: the single-state 924-perturbation reversal screen (which returned `NO_ROBUST_CANDIDATE`) and the old-vector sensitivity analysis (same cohort — not independent replication).
- **Controlled labels.** Only three public outcome labels are used: `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`, `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL`, `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS`.

## Methods

Reference genome GRCh38. Pseudobulk profiles were formed by summing raw UMI counts within each (perturbation, condition, donor) group and modeling with pydeseq2; a minimum of 25 cells per pseudobulk was required. Each target had 2 CRISPRi guides. Conditions were Rest, Stim8hr, and Stim48hr. The Perturb-seq cohort comprised 4 donors (6 leave-two-out donor pairs for perturbation-side robustness). Reversal is the negated centered-Pearson correlation between the knockdown log2FC vector and the disease log2FC vector over shared finite genes; reversal is undefined below 200 shared finite genes, and genes with non-finite knockdown or disease log2FC are dropped before correlation.

The **covariate-matched null** selects, for each candidate, its k = 200 nearest neighbors (z-scored Euclidean distance) in a five-feature space: perturbation magnitude, breadth, donor sign-consistency, guide sign-concordance, and on-target log-fold-change. This matches controls for "how strong / broad / consistent" a perturbation is, so that a high reversal is tested against equally strong perturbations rather than against inert genes. Scoring seed and matched-null seed are 0; Monte Carlo replicates used seeds 0–19. Superseded vectors (the old +0.43 / 77-gene / residency-removed representation) are never used as primary (see [Superseded results](SUPERSEDED_RESULTS.md)).

## Candidate attrition

Attrition is a **branching decision map, not a linear funnel**; not all 924 perturbations underwent every deep test. Denominators trace to `results/frozen/candidate_funnel.tsv`, `results/frozen/rejection_ledger.tsv`, and `results/frozen/all_perturbations_authoritative_reversal.tsv`. See **Figure 1** (`figures/figure_1_target_attrition.svg`).

| Stage | Scope | Entering | Advanced | Not advanced / rejected | Principal reasons |
|---|---|---:|---:|---:|---|
| S0 Screen-level reversal scoring | screen-wide | 924 | 208 | 716 not advanced | no measurable effect; not advanced from screen |
| S1 Biological robustness (donor-consistent subvector, bootstrap, jackknife) | screen-wide | 208 | 21 | 187 not advanced | broad transcriptional effect; donor-unstable |
| S2 Safety / essentiality / tractability / modality | screen-wide | 21 | 0 | 21 constrained | essentiality/safety liability; no credible modality; broad effect |
| D0 PAK2 deep candidate validation | candidate | 1 | 0 | 1 rejected | not therapeutically directional; generic activation suppression; partial inhibition not established |
| R0 RICTOR bounded pre-specified rescue | candidate | 1 | 1 | 0 | retained mechanism hypothesis |
| C0 RIPK1 comparator | candidate | 1 | 0 | 1 | comparator only |

The single-state screen yielded **no** advanceable candidate: the 21 biologically robust reversers were either broad/essential hubs held back on safety (e.g. GNAS, STAT3, SMARCB1, TET2 — `final_evidence_class = SAFETY_CONSTRAINED`) or immune-directional but undruggable transcription factors (e.g. KLF13, IRF9, ELF4 — `NO_CREDIBLE_MODALITY`). The deep candidate branch then evaluated PAK2, RICTOR, and RIPK1 as named candidates carried from prior work, independent of the exploratory screen outcome.

## Results

Head-to-head outcomes are frozen in `results/frozen/primary_comparison.tsv`; directionality and the matched null are shown in **Figure 2** (`figures/figure_2_directionality_and_null.svg`) and the gate matrix in **Figure 3** (`figures/figure_3_gate_matrix.svg`, source `results/frozen/gate_matrix.tsv`).

| Target | Primary reversal (responder space) | Pearson p | Matched-null percentile (all-cell substrate) | Final label |
|---|---:|---:|---:|---|
| RICTOR | +0.161 | 1.8e-63 | 96.5 | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` |
| PAK2 | +0.010 | 0.297 (n.s.) | 41.3 | `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` |
| RIPK1 | +0.038 | 8.7e-05 | 42.2 | `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` |

Denominators: 10,832 aligned genes; 11 paired disease donors; a 924-perturbation matched pool (k = 200) for the null. Only RICTOR clears both the directional effect and the matched-null percentile; the two "hits" that failed did so for different reasons (PAK2 has no directional effect at all; RIPK1 has a weak, incoherent one), which the labels preserve rather than collapse.

## PAK2 rejection case study

PAK2 is the pipeline's most instructive result: a technically excellent hit that is not a target. See **Figure 4** (`figures/figure_4_pak2_rejection.svg`) and `CLAIM-PAK2-01` in `results/frozen/claims.json`.

**Passed technical validation.** On-target knockdown was ~83–86% for both guides; guide concordance was 0.85 with 100% direction agreement; the 112-gene frozen responder programme was robust at the gene level across donors, guides, and leave-one-donor-out; the Mixscape responder fraction was 76.5%; the perturbation was non-toxic (`specific_non_toxic`). The internal frozen label is `REPRODUCIBLE_PAK2_RESPONDER_SIGNATURE_WITHOUT_THERAPEUTIC_RELEVANCE`.

**Failed therapeutic validation.** Disease reversal was +0.010 (p = 0.297, not significant); in the all-cell null substrate PAK2 sat at the 41st percentile (below the median matched control). The responder NF-kB delta was −0.011 (p = 0.05, negligible effect, no donor-direction consistency). The apparent external JIA-joint enrichment was **activation-confounded**: the frozen UP and DOWN modules co-elevate together (diverge = False), i.e. the signature tracks generic T-cell activation, so `disease_relevant = False`. Partial-inhibition sufficiency was `NOT_ESTABLISHED` — both guides produce similarly strong knockdown, giving no strong-versus-weak titration axis. No safer, druggable, immune-directional escape target reproduced the programme (0/10 passed the veto stack).

Four earlier PAK2-favorable readings were explicitly superseded and are retained as such (`results/frozen/superseded_claims.json`): SUP-02 (joint enrichment as disease support → activation confound), SUP-03 (partial-inhibition supported → not established), SUP-04 (a safer neighbour reproduces the programme → none found after correcting a gene-ID namespace mismatch), SUP-05 (PAK2–WASF2 as a validated axis → structural/directional evidence insufficient). PAK2 is rejected as a target nomination despite being a real, reproducible cellular hit. It is **not** an anti-inflammatory target on this evidence.

## RICTOR bounded validation

RICTOR was subjected to a pre-specified eight-criterion bounded rescue, fixed before the raw-count result was viewed (`CLAIM-RICTOR-01`, `results/frozen/claims.json`). Robustness detail is in **Supplementary Figure** `figures/supplementary_rictor_robustness.svg`.

Seven strong convergence checks were met:
1. Centered-Pearson reversal > 0: **+0.161** (p = 1.8e-63, r^2 ~ 2.6%, 10,832 genes).
2. Spearman reversal > 0: **+0.100**.
3. Ranked-GSEA reversal in the same (reversing) direction.
4. Both guides positive: RICTOR-1 **+0.141**, RICTOR-2 **+0.178** (`results/frozen/rictor_guides.tsv`).
5. All 11 disease-donor leave-one-out folds positive, band **+0.154 to +0.167** (`results/frozen/rictor_lodo.tsv`).
6. Responder-only support: 93% of strata positive, all donors positive.
7. Positive in all three conditions: Rest **+0.153**, Stim8hr **+0.092**, Stim48hr **+0.042** (`results/frozen/rictor_conditions.tsv`).

The **eighth** criterion — exceeding the covariate-matched perturbation null — is the **weakest and most marginal** (`results/frozen/matched_null.tsv`, `rictor_matched_null_values.tsv`). In the conservative all-cell substrate, RICTOR's reversal of +0.131 sits at the 96.5th matched-pool percentile (97.9th global), with z = 2.02; **7 of 200** matched controls exceeded it, giving empirical p = 0.0398, Wilson 95% CI 0.017–0.070, Monte Carlo bootstrap 95% CI 0.015–0.065, seed-stable p range 0.032–0.042, and pooled MC p = 0.034. Summary: RICTOR satisfied seven strong convergence checks and **nominally** exceeded a matched-perturbation null, with **borderline finite-pool uncertainty** — the upper confidence bound grazes ~0.07. This is a bounded retention, not a decisive pass; it is deliberately not described as "8/8 decisive."

**Leading edge.** RICTOR knockdown turns *down* pathogenic disease-UP genes including CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, and RGS1, with 0 disease-UP genes reinforced (`results/frozen/leading_edge.tsv`), consistent with mTORC2 as a mechanism node upstream of a tissue-effector/exhaustion programme.

## Robustness and negative controls

**Confound resistance** (`results/frozen/confound_decomposition.tsv`). Removing cell-cycle (+0.162), activation (+0.162), stress (+0.160), apoptosis (+0.161), or T-cell-identity (+0.160) modules leaves the reversal essentially unchanged versus the +0.161 baseline. Removing the 780 strongly-knockdown-down genes drops the reversal to +0.093 — but those genes **include the pathogenic disease-UP effectors** (CXCR6, CCL4, IFNG), so their removal deletes real signal, not a confound. The reversal is therefore not an artifact of generic activation or broad suppression.

**Gate ablation** (`results/frozen/gate_ablation.tsv`, `figures/supplementary_gate_ablation.svg`) demonstrates what each gate prevents: removing the therapeutic-directionality gate would let PAK2 read as advanceable (it passes every technical gate); removing broad-effect/essentiality controls would elevate nonspecific reversers (GNAS, STAT3, SMARCB1, TET2); removing modality review would surface undruggable TFs (KLF13, IRF9, ELF4); and reading the RICTOR matched-null point estimate as decisive would ignore that the 7/200 Wilson/bootstrap interval grazes 0.05–0.07.

**Negative comparators.** PAK2 (+0.010, p = 0.297) and RIPK1 (+0.038, both GSEA NES negative, 42nd matched-null percentile, single-condition Stim48hr coverage) both fail the matched null (each at the 33rd within-pool percentile), providing internal negative anchors against which RICTOR's percentile is read.

**Safety flags** (`results/frozen/safety_summary.tsv`). RICTOR carries a mild, donor-inconsistent early-toxicity flag (apoptosis mean delta +0.030, consistent in ≤33% of strata); T-cell and Treg identity are preserved. This is logged, not dismissed.

## Translational boundary

RICTOR is retained as a **mechanism hypothesis with a modality gap**, and the boundary is stated explicitly (see [Limitations](LIMITATIONS.md)). We do **not** claim: that RICTOR is a validated drug target; that systemic RICTOR inhibition is safe; or that a selective RICTOR modality exists — RICTOR is a core mTORC2 scaffold protein, and there is currently no selective small-molecule modality (the "modality gap"). We also do not claim that PAK2 is an anti-inflammatory target, that synovium-versus-blood equals disease-versus-healthy, or that nominal matched-null significance is definitive. RIPK1 remains a benchmark comparator only: real IBD/autoinflammatory genetics and clinical-stage kinase inhibitors exist, full loss-of-function causes immunodeficiency (so kinase inhibition, not knockdown, is the relevant modality), and it was not nominated by this test.

## Limitations

- **Matched-null marginality.** The eighth RICTOR criterion is borderline: 7/200 controls exceed it, Wilson 95% CI 0.017–0.070. Nominal significance is not definitive on a finite pool.
- **Same-cohort sensitivity, not independent replication.** The old-vector sensitivity analysis re-uses the same donor cohort; it is not independent biological replication.
- **Compartment, not disease, contrast.** The JIA vector is synovium-versus-blood, not disease-versus-healthy tissue; residency is not regressed.
- **Substrate dependence.** Responder-resolved (+0.161) and all-cell (+0.131) reversals differ by design; the two are never mixed, and the conservative number is used for null calibration.
- **Incomplete deep validation.** Not all 924 perturbations underwent every deep test; screen-wide counts are traceable to frozen artifacts only.
- **Modality gap.** No selective small-molecule modality for RICTOR currently exists.
- **Structural work is not the discovery result.** AF2/AF3 exploration around PAK2–WASF2 (SUP-05) did not establish a validated therapeutic interface and is not headline evidence.

## Open-data and reproducibility statement

Both source datasets are open (MIT for the Perturb-seq data; CC-BY-4.0 for the JIA atlas); derived aggregate vectors are committed with attribution (`data/public_data_manifest.tsv`, `NOTICE`). Every biological claim resolves to a data artifact, a primary paper, or an official database; model output is not treated as evidence. Reproducibility is tiered (`Makefile`, [Reproducibility levels](REPRODUCIBILITY_LEVELS.md)):

- **Level 1 (`make demo`)** — laptop, minutes, no server or private data: recomputes RICTOR/PAK2/RIPK1 reversals from compact committed inputs (`data/demo/*.tsv.gz`), regenerates tables and figures, and validates golden values.
- **Level 2 (`make reproduce`)** — recomputes guide and leave-one-donor-out robustness from committed pseudobulk (`data/reproduce/`) and compares to frozen values at tolerance 5e-3.
- **Level 3 (`make full`)** — high-memory server (~128 GB RAM, hours): downloads the open JIA h5ad and Perturb-seq matrices, rebuilds the disease vector and genome-scale effect vectors, and reruns everything; any input that cannot be rebuilt is stated honestly.

Provenance is anchored by the disease-vector checksum (md5 `2b18d92684db1f70b637e1f098374c7e`) and the frozen analysis contract. No compute-cluster names, hostnames, usernames, home paths, or job identifiers appear in this repository; server-scale steps refer only to a generic high-memory server.

## Future manuscript plan

A full manuscript would (1) replace the borderline eighth criterion with an independent replication cohort — ideally a second JIA synovial cohort and, separately, a disease-versus-healthy contrast — to convert RICTOR's bounded retention into a testable directional prediction; (2) enlarge the matched-null pool beyond 200 controls to tighten the Wilson/bootstrap interval currently grazing 0.07; (3) test the mTORC2 mechanism-node hypothesis with a selective perturbation of RICTOR-dependent effector output (CXCR6/IFNG/GZMB axis) rather than the scaffold itself, addressing the modality gap directly; (4) formalize the gate-ablation analysis (Figure 3, `gate_ablation.tsv`) as a general method for separating reproducible cellular hits from therapeutically directional ones; and (5) present PAK2 as a worked negative case demonstrating that on-target reproducibility and activation-tracking enrichment are not evidence of disease relevance. Structural work would remain supporting, not primary. The organizing claim for any such manuscript is process-level (`CLAIM-PROCESS-01`): candidate attrition, detected confounds, and corrected interpretations are auditable primary outputs, and Claude's contribution mattered most where the initial hypothesis failed — designing stricter falsification tests, preserving negative results, identifying confounds, and preventing an attractive cellular hit from becoming an unsupported drug-target claim.
