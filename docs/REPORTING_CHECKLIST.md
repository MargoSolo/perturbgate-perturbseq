# Reporting checklist

This checklist confirms, item by item, that the public claims in **TargetGate — Evidence-Gated
Pipeline for T-cell Perturb-seq Mechanism Hypotheses** (v1.0.0, frozen hackathon release) meet
publication-grade reporting standards. Each item names the concrete artifact that supports it, so a
reviewer can verify the claim directly rather than trusting the prose.

TargetGate frames its output as **target nomination, not gene ranking**. A real perturbation effect is
necessary but not sufficient for a target nomination; every retained claim survived an explicit record
of how competing claims failed. This checklist is the reporting-hygiene face of that stance.

Scope: three perturbations are discussed under exactly three controlled labels — RICTOR
(`DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`), PAK2
(`REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL`), and RIPK1
(`COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS`).

Related documents: [Methods](METHODS.md) · [Results](RESULTS.md) ·
[Claims and evidence](CLAIMS_AND_EVIDENCE.md) · [Decision trail](DECISION_TRAIL.md) ·
[Limitations](LIMITATIONS.md) · [Superseded results](SUPERSEDED_RESULTS.md) ·
[Data availability](DATA_AVAILABILITY.md) · [Data licenses](DATA_LICENSES.md) ·
[Open-data statement](OPEN_DATA_STATEMENT.md) · [Reproducibility](REPRODUCIBILITY.md) ·
[Reproducibility levels](REPRODUCIBILITY_LEVELS.md).

---

## Checklist

### 1. Effect sizes are reported, not only p-values

- [x] **Every directional claim leads with a signed effect size and its magnitude, with the p-value as a
  secondary statistic.** RICTOR primary responder-resolved reversal is **+0.161** centered-Pearson
  (r^2 ~ 2.6%), Spearman **+0.100**; the p-value (1.8e-63) is reported alongside, not instead. PAK2 is
  reported as reversal **+0.010** (p = 0.297, not significant) — the near-zero effect size is the headline,
  not the p-value. RIPK1 is reported as reversal **+0.038** with both GSEA NES negative.

  *Supporting artifacts:* [`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv)
  (columns `primary_reversal`, `primary_spearman_reversal`, `primary_pearson_p`),
  [`results/frozen/claims.json`](../results/frozen/claims.json) (`supporting_metrics` blocks),
  [Results](RESULTS.md).

### 2. Denominators are stated

- [x] **Every proportion, fold, and percentile resolves to an explicit denominator.** RICTOR reversal is
  computed over **10,832 aligned genes**; leave-one-donor-out is **11/11 disease-donor folds** positive;
  the matched-null percentile (96.5) is over **200 matched perturbations** (k = 200 nearest neighbours),
  of which **7 exceed RICTOR**. The screen-level denominator is **924 perturbations** scored, **208**
  convergent and FDR < 0.10, **21** biologically robust, **0** advanceable from the single-state screen.
  Denominators are not implied — they are tabulated per stage with the definition of what entered each stage.

  *Supporting artifacts:* [`results/frozen/candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv)
  (columns `denominator_definition`, `n_entering`, `n_advanced`, `n_not_advanced`),
  [`results/frozen/matched_null.tsv`](../results/frozen/matched_null.tsv) (column `n_null`),
  [`results/frozen/claims.json`](../results/frozen/claims.json) (`denominator` field per claim).

### 3. Pre-specified (confirmatory) analyses are distinguished from exploratory analyses

- [x] **The eight RICTOR criteria were fixed before the corrected raw-count result was viewed, and are
  labelled confirmatory; the screen-wide scan is labelled exploratory.** The pre-specified criteria are:
  (1) centered-Pearson reversal > 0; (2) Spearman reversal > 0; (3) ranked-GSEA reversal same direction;
  (4) both RICTOR guides positive; (5) all 11 disease-donor LODO folds positive; (6) responder-only support;
  (7) positive in all three conditions; (8) above the matched-perturbation null at the frozen point estimate.
  **RICTOR satisfied seven strong convergence checks and nominally exceeded a matched-perturbation null,
  with borderline finite-pool uncertainty** — criterion 8 is explicitly identified as the weakest and most
  marginal. This is not reported as "8/8 decisive criteria." The 924-perturbation screen is reported
  separately as an exploratory branch that yielded `NO_ROBUST_CANDIDATE`.

  *Supporting artifacts:* [`results/frozen/analysis_contract.json`](../results/frozen/analysis_contract.json)
  (pre-registered criteria), [`results/frozen/candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv)
  (stage `R0` = bounded pre-specified rescue vs stages `S0-S2` = screen-wide exploratory),
  [Decision trail](DECISION_TRAIL.md), [Methods](METHODS.md).

### 4. Same-cohort sensitivity analyses are distinguished from independent replication

- [x] **Cross-condition, cross-donor, and cross-substrate checks are labelled same-cohort sensitivity, never
  independent replication.** The 11-donor leave-one-out folds, the Rest/Stim8hr/Stim48hr condition split
  (+0.153 / +0.092 / +0.042), and the conservative all-cell null-substrate projection (+0.131) all derive
  from the **same disease cohort and the same Perturb-seq experiment**; they bound internal robustness, not
  external generalization. The documentation states plainly that the adjusted-vector sensitivity is **not**
  independent biological replication (same cohort) and that **no independent same-tissue replication exists**.

  *Supporting artifacts:* [`results/frozen/rictor_lodo.tsv`](../results/frozen/rictor_lodo.tsv),
  [`results/frozen/rictor_conditions.tsv`](../results/frozen/rictor_conditions.tsv),
  [`results/frozen/claims.json`](../results/frozen/claims.json) (`limitations`: "no independent same-tissue
  replication"), [Limitations](LIMITATIONS.md).

### 5. Missing evidence is stated, not omitted

- [x] **What the analysis does not show is listed explicitly.** RICTOR is **not** a validated drug target;
  systemic RICTOR inhibition is **not** shown to be safe; **no selective small-molecule RICTOR modality
  currently exists** (the "modality gap" — mTORC2 core scaffold). The disease surrogate is JIA
  **synovium-vs-blood, which is not disease-vs-healthy**. Not all 924 perturbations underwent deep
  validation. Nominal matched-null significance is **not** definitive. These absences are recorded as
  first-class fields, not left to the reader to infer.

  *Supporting artifacts:* [`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv)
  (columns `modality_summary`, `principal_limitation`),
  [`results/frozen/claims.json`](../results/frozen/claims.json) (`limitations` arrays),
  [Limitations](LIMITATIONS.md), [Failure modes](FAILURE_MODES.md),
  [Translational review status](TRANSLATIONAL_REVIEW_STATUS.md).

### 6. Null-pool / finite-sample uncertainty is stated

- [x] **The matched-null empirical p-value is reported with its finite-pool interval, not as a point value.**
  On the conservative all-cell substrate, RICTOR reversal +0.131 sits at percentile 96.5 (global 97.9);
  **7 of 200** matched perturbations exceed it; empirical **p = 0.0398**, Wilson 95% CI **(0.017, 0.070)**,
  Monte-Carlo bootstrap 95% CI **(0.015, 0.065)**, seed-stable p range **[0.032, 0.042]**, pooled p 0.034.
  The upper CI reaching ~0.07 on a pool of only 200 controls is called out as the load-bearing uncertainty.
  Substrates are never silently mixed: the primary responder-resolved score (+0.161, 10,832 genes) and the
  all-cell null-substrate score (+0.131, 7,393-gene intersection) are reported separately, with the +0.030
  gap decomposed (-0.036 gene-universe + +0.066 responder->all-cell representation).

  *Supporting artifacts:* [`results/frozen/matched_null.tsv`](../results/frozen/matched_null.tsv)
  (columns `empirical_p`, `percentile`, `n_null`, `z`),
  [`results/frozen/rictor_matched_null_values.tsv`](../results/frozen/rictor_matched_null_values.tsv)
  (per-control null distribution),
  [`results/frozen/confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv)
  (substrate/gene-universe decomposition), [Methods](METHODS.md).

### 7. Exact controlled labels are used consistently

- [x] **Only the three controlled public labels appear, verbatim, wherever a target's status is stated.**
  RICTOR = `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`; PAK2 =
  `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL`; RIPK1 =
  `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS`. No target is described with an
  uncontrolled synonym, and RICTOR is never called a validated drug target.

  *Supporting artifacts:* [`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv)
  (column `final_public_label`), [`results/frozen/claims.json`](../results/frozen/claims.json)
  (`exact_public_wording`), [Claims and evidence](CLAIMS_AND_EVIDENCE.md).

### 8. Primary sources are cited

- [x] **Every dataset resolves to a primary paper and an official database accession; no biological claim
  rests on model output alone.** The primary Human CD4+ T-cell Perturb-seq dataset (Marson lab and Pritchard
  lab) is cited as bioRxiv DOI 10.64898/2025.12.23.696273, with processed data at
  `s3://genome-scale-tcell-perturb-seq/` and raw data at GEO GSE314342 / SRA SRP643211. The JIA synovial
  atlas (Knight et al., bioRxiv DOI 10.64898/2026.05.01.716870; companion Bolton/Mahony, *Sci Transl Med*
  2025, DOI 10.1126/scitranslmed.adt6050) is cited with CZ CELLxGENE collection
  10eb236d-d42d-45b8-8363-c2dcf865f388. Claude output is treated as pipeline and reasoning support, not
  scientific evidence.

  *Supporting artifacts:* [`data/public_data_manifest.tsv`](../data/public_data_manifest.tsv),
  [`NOTICE`](../NOTICE), [`CITATION.cff`](../CITATION.cff), [Data availability](DATA_AVAILABILITY.md),
  [Claude usage](CLAUDE_USAGE.md).

### 9. Figures have machine-readable source data

- [x] **Each published figure ships with the exact table it was rendered from.** All four main figures and
  both supplementary figures have a matching source-data TSV under `figures/source_data/`:
  `figure_1_target_attrition`, `figure_2_directionality_and_null`, `figure_3_gate_matrix`,
  `figure_4_pak2_rejection`, `supplementary_gate_ablation`, `supplementary_rictor_robustness`. Every figure
  is provided as both PNG and vector SVG.

  *Supporting artifacts:*
  [`figures/source_data/figure_1_target_attrition.tsv`](../figures/source_data/figure_1_target_attrition.tsv),
  [`figures/source_data/figure_2_directionality_and_null.tsv`](../figures/source_data/figure_2_directionality_and_null.tsv),
  [`figures/source_data/figure_3_gate_matrix.tsv`](../figures/source_data/figure_3_gate_matrix.tsv),
  [`figures/source_data/figure_4_pak2_rejection.tsv`](../figures/source_data/figure_4_pak2_rejection.tsv),
  and the two supplementary source-data TSVs in the same directory.

### 10. Open-data terms are documented

- [x] **License and access terms are stated for every input, and redistribution rights for derived vectors
  are recorded.** The Perturb-seq dataset is MIT-licensed (redistribution permitted; registration not
  required for the processed S3 mirror). The JIA atlas is CC-BY-4.0 (fully open, no registration). The
  committed per-gene aggregate disease and effect vectors are redistributed under attribution. All inputs
  used here are open; there is no gated or restricted-access dependency in the published claims.

  *Supporting artifacts:* [`data/public_data_manifest.tsv`](../data/public_data_manifest.tsv),
  [`NOTICE`](../NOTICE), [`LICENSE`](../LICENSE), [Data licenses](DATA_LICENSES.md),
  [Open-data statement](OPEN_DATA_STATEMENT.md).

### 11. Superseded results are registered, not silently dropped

- [x] **Earlier, stronger-sounding numbers that were later corrected are recorded as explicitly superseded
  and never presented as current.** The old RICTOR reversal of ~+0.43 (old covariate-adjusted /
  residency-removed 77-gene subset, inflated by a frozen-subset gene universe plus KD representation) is
  registered as **SUP-01** and replaced by the current +0.161 primary / +0.131 null-substrate values. Four
  PAK2 claims (JIA joint enrichment as disease support; partial-inhibition supported; safer neighbour
  reproduces the programme; PAK2-WASF2 validated therapeutic axis) are registered as **SUP-02 ... SUP-05**.
  The AF2/AF3 structural work is recorded as **not** the target-discovery result.

  *Supporting artifacts:* [`results/frozen/superseded_claims.json`](../results/frozen/superseded_claims.json)
  (SUP-01 ... SUP-05, each with `reason_superseded` and `authoritative_replacement`),
  [Superseded results](SUPERSEDED_RESULTS.md).

### 12. No private, server, or environment-specific details

- [x] **The public record contains no compute-cluster name, hostname, username, home path, job id,
  container image, or token.** Server-scale steps refer only to a generic "server" / "compute server" /
  "high-memory server" and to the placeholders `SERVER_DATA_ROOT` / `SERVER_RESULTS_ROOT`. Private
  conversation transcripts are not exposed. Integrity of the frozen artifacts is verifiable via committed
  SHA-256 checksums rather than any environment reference.

  *Supporting artifacts:* [`results/frozen/results_manifest.json`](../results/frozen/results_manifest.json)
  (SHA-256 of every frozen artifact and demo input), [Reproducibility](REPRODUCIBILITY.md),
  [Reproducibility levels](REPRODUCIBILITY_LEVELS.md).

---

## Summary

| # | Reporting item | Status | Primary artifact |
|---|----------------|--------|------------------|
| 1 | Effect sizes, not p-values alone | Confirmed | `results/frozen/primary_comparison.tsv` |
| 2 | Denominators stated | Confirmed | `results/frozen/candidate_funnel.tsv` |
| 3 | Pre-specified vs exploratory | Confirmed | `results/frozen/analysis_contract.json` |
| 4 | Same-cohort sensitivity vs replication | Confirmed | `results/frozen/rictor_lodo.tsv` |
| 5 | Missing evidence stated | Confirmed | `docs/LIMITATIONS.md` |
| 6 | Null-pool uncertainty stated | Confirmed | `results/frozen/matched_null.tsv` |
| 7 | Exact controlled labels | Confirmed | `results/frozen/primary_comparison.tsv` |
| 8 | Primary sources cited | Confirmed | `data/public_data_manifest.tsv` |
| 9 | Figures have source data | Confirmed | `figures/source_data/` |
| 10 | Open-data terms documented | Confirmed | `docs/OPEN_DATA_STATEMENT.md` |
| 11 | Superseded results registered | Confirmed | `results/frozen/superseded_claims.json` |
| 12 | No private/server details | Confirmed | `results/frozen/results_manifest.json` |

All twelve items are met against frozen v1.0.0 artifacts. The retained RICTOR claim is a bounded
mechanism hypothesis with a stated modality gap, not a validated drug target; PAK2 is a documented
negative result; RIPK1 is a comparator that this test does not directionally support.
