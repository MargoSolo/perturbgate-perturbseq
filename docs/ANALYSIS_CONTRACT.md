# Analysis contract

This document is the human-readable mirror of
[`results/frozen/analysis_contract.json`](../results/frozen/analysis_contract.json).
It records what was pre-specified, what was measured, and what may and may not be
claimed for the frozen PerturbGate v1.0.0 release. Where a number appears here it is
copied from a frozen artifact under [`results/frozen/`](../results/frozen/); no value
in this document is estimated or rounded beyond the precision of its source table.

PerturbGate is an evidence-gated pipeline for T-cell Perturb-seq mechanism
hypotheses. Its central premise is that a real perturbation effect is **necessary
but not sufficient** for target nomination. The contract below exists so that every
retained claim can be traced to an explicit record of how competing claims failed.
This is a target-**nomination** exercise, not a gene-ranking leaderboard.

Related documents: [Methods](METHODS.md) - [Limitations](LIMITATIONS.md) -
[Reproducibility levels](REPRODUCIBILITY_LEVELS.md) -
[Superseded results](SUPERSEDED_RESULTS.md) - [Failure modes](FAILURE_MODES.md).

---

## 1. Primary hypothesis

> A perturbation is a candidate mechanism node only if its knockdown reverses a
> donor-paired disease-state direction and survives guide, donor, condition,
> matched-null and confound checks.

The hypothesis is directional and gate-structured: a measurable transcriptional
effect alone does not qualify a perturbation. Reversal of a disease direction must
persist across guides, disease donors, activation conditions, a covariate-matched
null of other perturbations, and explicit confound removals.

---

## 2. Primary disease vector

| Field | Value |
| --- | --- |
| Name | JIA synovium-vs-blood, activated-memory CD4, raw-count donor-paired pseudobulk |
| Contrast | JIA synovium (tissue + fluid) vs blood, activated-memory CD4 |
| Construction | per-donor `log2((CPM_syn + 1) / (CPM_blood + 1))`, meta across 11 paired donors |
| Primary state | `activated_memory` |
| Paired donors | 11 |
| Genes | 12071 (full transcriptome) |
| Residency regressed | No |
| md5 | `2b18d92684db1f70b637e1f098374c7e` |
| Source | CZ CELLxGENE collection `10eb236d-d42d-45b8-8363-c2dcf865f388` (CC-BY-4.0) |

Synovium-vs-blood is an anatomical/compartment contrast within JIA patients. It is
**not** a disease-vs-healthy comparison, and residency is deliberately not regressed
out of the primary vector (a sensitivity vector that adjusts covariates is treated
as same-cohort sensitivity, not independent replication; see Sections 6 and 14).

---

## 3. Primary state

`activated_memory` CD4 T cells. All primary reversal scores are computed against the
activated-memory disease vector. Condition-resolved knockdown effects
(Rest / Stim8hr / Stim48hr) are reported as a robustness axis (criterion 7), not as
separate primary hypotheses.

---

## 4. Sign convention

```
reversal = -centered_Pearson(KD_log2FC, disease_log2FC)
```

- **reversal > 0** - knockdown moves the transcriptome opposite to the disease
  direction (disease-**reversing** / candidate mechanism node).
- **reversal < 0** - knockdown reinforces the disease direction (disease-**mimicking**).

Reversal is the centered Pearson correlation between the knockdown log2 fold-change
vector and the disease log2 fold-change vector, negated so that positive means
therapeutically desirable. Spearman and ranked-GSEA variants use the same sign
convention.

---

## 5. Target comparison set

Three perturbations carry a controlled public label in this release:

| Target | Role | Final controlled label |
| --- | --- | --- |
| **RICTOR** | Retained mechanism hypothesis | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` |
| **PAK2** | Deep-validated then rejected | `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` |
| **RIPK1** | Benchmark comparator | `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` |

These are the only three controlled labels used publicly. Their authoritative numbers
live in [`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv).

---

## 6. Gene-universe and representation definitions

Two substrates are used, and they are never silently mixed. Responder-resolved scores
must not be compared directly against all-cell null-substrate scores.

| Substrate | Definition | Aligned genes | RICTOR reversal | Used for |
| --- | --- | --- | --- | --- |
| **Primary (responder-resolved)** | responder-DE donor random-effects meta KD vector, full transcriptome | 10832 | **+0.161** | primary directional claim |
| **Conservative (all-cell)** | genome-scale all-cell effect vectors (mean of conditions) projection | 7393-gene intersection | **+0.131** | matched-null calibration only |

The all-cell substrate is the **conservative** number. It is used exclusively to place
RICTOR in the same feature space as the matched-perturbation null (Section 8).

Decomposition of the +0.030 gap between the two substrates
([`results/frozen/confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv)
and the frozen contract):

- **-0.036** attributable to the narrower gene universe (7393-gene intersection);
- **+0.066** attributable to the responder -> all-cell representation change.

### Primary vs sensitivity representations

- **Primary representation:** responder-resolved donor-RE meta (reversal +0.161).
- **Conservative/sensitivity representation:** all-cell effect-vector projection
  (reversal +0.131), used only for null calibration.

The two are complementary, not interchangeable. Reporting one substrate's reversal
against the other substrate's null is prohibited by this contract.

---

## 7. The eight pre-specified RICTOR criteria

These eight checks were fixed **before** the corrected raw-count result was viewed.
They constitute the confirmatory, bounded rescue of RICTOR
([`results/frozen/rictor_guides.tsv`](../results/frozen/rictor_guides.tsv),
[`rictor_lodo.tsv`](../results/frozen/rictor_lodo.tsv),
[`rictor_conditions.tsv`](../results/frozen/rictor_conditions.tsv),
[`matched_null.tsv`](../results/frozen/matched_null.tsv)).

| # | Criterion | RICTOR result |
| --- | --- | --- |
| 1 | centered-Pearson reversal > 0 | **+0.161** (p = 1.8e-63, r^2 ~ 2.6%, 10832 aligned genes) - met |
| 2 | Spearman reversal > 0 | **+0.100** - met |
| 3 | ranked-GSEA reversal in the same direction | positive, same direction - met |
| 4 | both RICTOR guides positive | RICTOR-1 **+0.141**, RICTOR-2 **+0.178** - met |
| 5 | all 11 disease-donor leave-one-out folds positive | **11/11** positive (band +0.154 to +0.167) - met |
| 6 | responder-only support | 93% of strata positive, all donors positive - met |
| 7 | positive in all three conditions | Rest **+0.153**, Stim8hr **+0.092**, Stim48hr **+0.042** - met |
| 8 | above the matched-perturbation null at the frozen point estimate | conservative substrate **+0.131**, percentile 96.5 (global 97.9); nominally exceeded - see caveat |

### Criterion 8 is the weakest / most marginal

Criterion 8 is explicitly the weakest of the eight and must not be presented as
decisive. In the conservative all-cell substrate
([`results/frozen/matched_null.tsv`](../results/frozen/matched_null.tsv)):

- observed reversal **+0.131**; null mean ~ 0.004, null sd ~ 0.063, z ~ 2.02;
- **7 of 200** matched perturbations exceed RICTOR;
- empirical **p = 0.0398**;
- Wilson 95% CI **(0.0171, 0.0705)** - i.e. the upper bound reaches ~ 0.07;
- Monte-Carlo bootstrap 95% CI **(0.0149, 0.0647)**;
- seed-stable p range **[0.032, 0.042]**; pooled Monte-Carlo p **0.034**.

**Do not write "8/8 decisive criteria."** The contract-mandated wording is:

> RICTOR satisfied seven strong convergence checks and nominally exceeded a
> matched-perturbation null, with borderline finite-pool uncertainty.

---

## 8. Matched-null design

Matched-null construction (frozen contract; seed 0):

- **Features (z-scored):** magnitude, breadth, donor_sign_consistency,
  guide_sign_concordance, ontarget_lfc.
- **Matching:** z-scored Euclidean distance, k = 200 nearest neighbours.
- **Pool size:** 200 matched perturbations (200 unique matched).
- **Exceeding RICTOR:** 7 of 200.
- **Empirical p:** 0.0398; pooled Monte-Carlo p 0.0339.
- **Finite-pool caveat:** with only 200 matched controls the Wilson upper bound on
  the exceedance rate reaches ~ 0.07, so nominal significance is not definitive.

The matched null is computed on the conservative all-cell substrate so that RICTOR and
its matched comparators occupy the same 7393-gene feature space (Section 6). Never mix
responder-resolved scores with all-cell null-substrate scores.

### Confound resistance (context for criterion interpretation)

Removing cell-cycle, activation, stress, apoptosis, or T-identity gene sets leaves the
responder-resolved reversal essentially unchanged (all within ~ +/-0.0012 of the base
+0.161; [`confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv)).
Removing the 780 strongly-knockdown-down genes drops reversal to **+0.093**, but that
set **includes the pathogenic disease-UP genes** CXCR6, CCL4, IFNG - so that removal
subtracts real signal, not confound. Leading edge: RICTOR knockdown turns **down**
disease-UP genes CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, RGS1, with 0 reinforced.

---

## 9. Seeds

| Component | Seed(s) |
| --- | --- |
| Scoring | 0 |
| Matched null | 0 |
| Monte-Carlo replicates | 0-19 (20 seeds) |

---

## 10. Exclusion rules

1. Genes with non-finite knockdown or disease log2FC are dropped before correlation.
2. Reversal is undefined below 200 shared finite genes.
3. Superseded vectors (the old +0.43 / 77-gene / residency-removed representation)
   are never used as the primary substrate - only in explicitly labelled
   [superseded](SUPERSEDED_RESULTS.md) context.

---

## 11. Final controlled labels and per-target decisions

### RICTOR - `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`

Decision: **RETAINED_AS_MECHANISM_HYPOTHESIS.** Primary responder-resolved reversal
+0.161 (centered Pearson, p = 1.8e-63, r^2 ~ 2.6%, 10832 aligned genes); Spearman
+0.100; both guides positive (+0.141, +0.178); 11/11 disease-donor LODO folds positive
(band +0.154 to +0.167); positive in all three conditions; responder-only support 93%
of strata, all donors positive. Matched null: conservative +0.131, percentile 96.5
(global 97.9), empirical p 0.0398, borderline finite-pool uncertainty to ~ 0.07.
Safety: a mild, donor-inconsistent early-tox flag (apoptosis +0.030, <= 33% strata
consistent); T-cell and Treg identity preserved. Modality: mTORC2 core scaffold with
**no selective small-molecule modality** - the "modality gap." Principal limitation:
matched-null borderline finite-pool to 0.07; synovium-vs-blood is not
disease-vs-healthy; no independent replication; modality gap.

RICTOR is **not** a validated drug target (see Section 15).

### PAK2 - `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL`

Decision: **REJECTED_NOT_THERAPEUTICALLY_DIRECTIONAL** (frozen internal label
`REPRODUCIBLE_PAK2_RESPONDER_SIGNATURE_WITHOUT_THERAPEUTIC_RELEVANCE`).
PAK2 **passed technical validation:** on-target knockdown ~ 83-86% for both guides;
guide concordance 0.85 (100% direction agreement); a 112-gene frozen responder
programme robust across donor, guide and LODO at the gene level; Mixscape responder
fraction 76.5%; non-toxic (`specific_non_toxic`). PAK2 **failed therapeutic
validation:** disease reversal **+0.010, p = 0.297** (not significant), matched-null
41st percentile; responder NF-kB delta = -0.011 (p = 0.05, negligible, no
donor-direction consistency); external JIA enrichment is **activation-confounded**
(FROZEN_UP and FROZEN_DOWN modules co-elevate, diverge = False -> disease_relevant =
False); partial-inhibition sufficiency **NOT_ESTABLISHED** (both guides similarly
strong, no strong-vs-weak titration axis); no safer druggable immune-directional
escape (0/10 pass the veto stack). PAK2 is a real, reproducible cellular hit that is
**not** an anti-inflammatory target.

### RIPK1 - `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS`

Decision: **COMPARATOR_ONLY.** Weak / incoherent disease reversal +0.038 (both GSEA
NES negative), matched-null 42nd percentile. RIPK1 is included as a benchmark
comparator - real IBD / autoinflammatory genetics and clinical-stage kinase inhibitors
exist, and full loss-of-function causes immunodeficiency, so kinase inhibition (not
knockdown) is the relevant modality. It is not nominated by this directional test.

---

## 12. Superseded analyses

The following are recorded in
[`results/frozen/superseded_claims.json`](../results/frozen/superseded_claims.json)
and [`docs/SUPERSEDED_RESULTS.md`](SUPERSEDED_RESULTS.md). None may be presented as a
current result.

| ID | Entity | Superseded claim | Replaced by |
| --- | --- | --- | --- |
| SUP-01 | RICTOR | reversal ~ +0.43 (old covariate-adjusted / residency-removed 77-gene subset; inflated by frozen-subset universe + KD representation) | +0.161 primary / +0.131 null-substrate |
| SUP-02 | PAK2 | JIA joint enrichment as disease support | UP/DOWN modules co-elevate -> generic activation confound -> not supported |
| SUP-03 | PAK2 | partial inhibition is supported | both guides similarly strong KD -> NOT_ESTABLISHED |
| SUP-04 | PAK2 | a safer PAK2 neighbour reproduces the programme | gene-ID namespace mismatch + incomplete vetoes -> none found |
| SUP-05 | PAK2 | PAK2-WASF2 is a validated therapeutic axis | structural/directional evidence insufficient -> not validated |

The old RICTOR **+0.43** figure appears in this table only as an explicitly superseded
value. It is never the current RICTOR result. Structural work (AF2/AF3) is not the
target-discovery result of this project.

---

## 13. Screen / attrition denominators

The screen is a **branching decision map, not a linear funnel**. Not all perturbations
underwent every deep test. Denominators trace to
[`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv),
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv), and
[`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv).

| Stage | Scope | Entering | Advanced | Not advanced / rejected |
| --- | --- | --- | --- | --- |
| S0 screen-level reversal scoring | screen-wide | 924 | 208 | 716 not advanced |
| S1 biological robustness | screen-wide | 208 (convergent + FDR<0.10) | 21 | 187 broad / donor-unstable |
| S2 safety / essentiality / modality | screen-wide | 21 | 0 | 21 constrained -> NO_ROBUST_CANDIDATE |
| D0 PAK2 deep validation | candidate-specific | 1 | 0 | 1 rejected (not directional) |
| R0 RICTOR bounded rescue (8 criteria) | candidate-specific | 1 | 1 | retained mechanism hypothesis |
| C0 RIPK1 comparator | candidate-specific | 1 | 0 | comparator only |

924 perturbations were scored at screen level on the activated-memory corrected
raw-count disease vector. The single-state screen produced **0 advanceable** candidates
(NO_ROBUST_CANDIDATE): the 21 robust hits were safety- or modality-constrained -
broad/essential hubs (e.g. GNAS, STAT3, SMARCB1, TET2) safety-constrained, and
immune-directional but undruggable transcription factors (e.g. KLF13, IRF9, ELF4) with
no credible modality. RICTOR, PAK2 and RIPK1 were carried into candidate-specific
branches; do not imply all 924 underwent the deep tests.

---

## 14. Confirmatory vs exploratory boundary

| Class | Analyses |
| --- | --- |
| **Confirmatory (pre-specified)** | RICTOR 8-criterion bounded rescue; PAK2 four-criterion decision gate |
| **Exploratory** | single-state 924-perturbation reversal screen (NO_ROBUST_CANDIDATE); old-vector sensitivity analysis (same cohort - **not** independent replication) |

The old-vector / covariate-adjusted sensitivity analysis is same-cohort sensitivity,
not independent biological replication. Exploratory screen outputs are hypothesis-
generating and were not used to make a nomination decision on their own.

---

## 15. What this contract does not claim

- RICTOR is **not** a validated drug target.
- Systemic RICTOR inhibition is **not** shown to be safe; no selective RICTOR modality
  currently exists (the modality gap).
- Synovium-vs-blood is **not** disease-vs-healthy.
- The adjusted-vector sensitivity is **not** independent biological replication (same
  cohort).
- PAK2 is **not** an anti-inflammatory target.
- Not all 924 perturbations underwent deep validation.
- Nominal matched-null significance is **not** definitive.

Every biological claim in this release resolves to a data artifact, a primary paper, or
an official database. Model output is not itself scientific evidence.

---

*Frozen hackathon release v1.0.0 (2026-07-13). This contract mirrors
[`results/frozen/analysis_contract.json`](../results/frozen/analysis_contract.json);
where the two differ, the JSON artifact governs.*
