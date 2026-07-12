# Methods

TargetGate is an evidence-gated pipeline for generating and stress-testing mechanism
hypotheses from a T-cell Perturb-seq dataset. It was built for the "Built with Claude:
Life Sciences" event (Anthropic x Gladstone Institutes), Research track, for the
challenge *Find new drug targets in a T-cell Perturb-seq dataset from the Marson and
Pritchard labs*. This document specifies the data, statistics, decision logic, seeds,
and software used to produce the frozen 1.0.0 release.

The organising principle is deliberately restrictive: a real perturbation effect is
**necessary but not sufficient** for target nomination. Every method below is designed
to let a candidate *fail* on an explicit, pre-recorded criterion rather than to confirm
an attractive hit. The three reported targets — RICTOR, PAK2, RIPK1 — are the outcome of
that gating, not a ranked leaderboard. All numeric values below are read from the frozen
artifacts under [`results/frozen/`](../results/frozen); each subsection names the artifact
that backs it. See also [Reproducibility](REPRODUCIBILITY.md),
[Superseded results](SUPERSEDED_RESULTS.md), and [Data licenses](DATA_LICENSES.md).

---

## 1. Data sources

Both primary datasets are open. Only per-gene aggregate derived vectors are redistributed
in this repository (see [`data/public_data_manifest.tsv`](../data/public_data_manifest.tsv)
and [`NOTICE`](../NOTICE)); no raw single-cell matrices are committed.

**Primary Human CD4+ T Cell Perturb-seq** (Marson lab, Gladstone/UCSF; Pritchard lab,
Stanford). Single-cell CRISPR Perturb-seq in primary human CD4+ T cells.
bioRxiv DOI `10.64898/2025.12.23.696273`; distributed via CZI Virtual Cell Models;
processed data at anonymous S3 `s3://genome-scale-tcell-perturb-seq/marson2025_data/`;
raw archives GEO `GSE314342` / SRA `SRP643211`. License MIT (redistribution permitted with
attribution). Registration not required for the processed S3 objects. Two guides per target;
conditions Rest, Stim8hr, Stim48hr; four Perturb-seq donors.

**JIA synovial single-cell atlas — "Integrated global cells"** (Knight et al.,
bioRxiv DOI `10.64898/2026.05.01.716870`; companion Bolton/Mahony, *Sci Transl Med* 2025,
DOI `10.1126/scitranslmed.adt6050`). CZ CELLxGENE collection
`10eb236d-d42d-45b8-8363-c2dcf865f388`; h5ad served by CELLxGENE Discover. License
CC-BY-4.0, fully open, no registration.

Alignment/annotation is on genome build GRCh38. The two committed derived aggregates —
the disease-direction vector and the three knockdown effect vectors — inherit the upstream
licenses (CC-BY-4.0 and MIT respectively) and are redistributed with attribution.

---

## 2. Disease-vector construction

The disease direction is a **JIA synovium(tissue+fluid)-vs-blood** contrast in
**activated-memory CD4+ T cells**, computed as a **raw-count, donor-paired pseudobulk**
log fold-change and meta-analysed across donors.

- **State.** Cells are restricted to the activated-memory CD4 compartment
  (`state = activated_memory`). Tissue residency is deliberately **not regressed out**;
  it is a biological feature of the synovial compartment, and removing it was one of the
  errors that inflated a superseded earlier estimate (see §14 and
  [Superseded results](SUPERSEDED_RESULTS.md)).
- **Pseudobulk.** Raw UMI counts are summed per donor and compartment; per donor the
  contrast is `log2((CPM_syn + 1) / (CPM_blood + 1))`.
- **Meta-analysis.** Per-donor log2FC are combined across **11 paired synovium/blood
  donors** over the **full transcriptome (12,071 genes)**.
- **Provenance.** The frozen vector has md5 `2b18d92684db1f70b637e1f098374c7e`
  (recorded in [`results/frozen/analysis_contract.json`](../results/frozen/analysis_contract.json))
  and is committed for the demo as
  [`data/demo/disease_vector_activated_memory.tsv.gz`](../data/demo/disease_vector_activated_memory.tsv.gz)
  (sha256-16 `255d501174d9ee55`).

Interpretive caveat carried through every downstream claim: a synovium-vs-blood contrast is
a **compartment/anatomical** contrast, **not** a disease-vs-healthy contrast, and the 11
donors are a single cohort.

---

## 3. Knockdown responder-DE meta vectors

For each perturbation the primary knockdown (KD) effect vector is a **responder-resolved,
donor random-effects meta** of KD-vs-control differential expression:

- Pseudobulks are formed by summing raw UMI counts within each
  `(perturbation, condition, donor, responder-class)` cell group, requiring a minimum of
  **25 cells per pseudobulk**; differential expression against non-targeting controls is
  fit with **pydeseq2**.
- "Responder-resolved" means DE is computed within Mixscape-style responder strata (cells
  in which the perturbation produced a detectable transcriptional response), then combined
  across donors under a random-effects model. This yields a per-gene KD log2FC vector; the
  committed demo vectors span 18,130 genes each
  ([`data/demo/kd_meta_{RICTOR,PAK2,RIPK1}.tsv.gz`](../data/demo)).
- After intersection with the disease vector and dropping non-finite entries, the RICTOR
  primary comparison is over **10,832 aligned genes**.

A separate, more conservative **all-cell effect-vector projection** (genome-scale KD-vs-NTC
log2FC averaged over conditions, without responder resolution) is used **only** for
matched-null calibration; the two substrates are never mixed in a single score (see §12).

---

## 4. Reversal statistic and sign convention

A perturbation *reverses* a disease direction if its knockdown moves genes opposite to the
disease direction. The primary statistic
([`src/targetgate/reversal.py`](../src/targetgate/reversal.py)) is the **negative
centered-Pearson correlation** between the KD log2FC vector and the disease log2FC vector
over shared, finite genes:

```
reversal = -centered_Pearson(KD_log2FC, disease_log2FC)
         >  0  =>  reversing   (KD down where disease is up, and vice versa)
         <  0  =>  mimicking
```

The sign convention is fixed once and asserted in unit tests. Guardrails: a reversal is
**undefined below 200 shared finite genes** (returns a null result, never a silent zero);
constant vectors (std < 1e-9) are rejected. A companion Spearman reversal
(`-Spearman(KD, disease)`) is reported alongside, and a per-gene "moved" tally uses a
`|KD log2FC| >= 0.10` floor to count reversed vs reinforced genes. This is an
effect-size-first metric: correlations and their denominators (aligned-gene counts) are
reported rather than p-values alone.

---

## 5. Per-guide, per-condition, LODO, and responder computations

These are the confirmatory robustness checks applied to a candidate, all against the
primary responder-resolved KD vector.

- **Guide concordance.** Each target has two independent guides; the reversal is recomputed
  per guide. Both RICTOR guides are positive —
  **RICTOR-1 = +0.141** and **RICTOR-2 = +0.178** over 10,832 genes
  ([`rictor_guides.tsv`](../results/frozen/rictor_guides.tsv)). For PAK2, guide-level
  knockdown concordance is 0.85 with 100% direction agreement, but partial-inhibition
  sufficiency is not established because both guides knock down similarly strongly
  (~83–86%), giving no strong-vs-weak titration axis.
- **Condition consistency.** Reversal is recomputed within each Perturb-seq condition.
  RICTOR is positive in all three: **Rest +0.153, Stim8hr +0.092, Stim48hr +0.042**
  ([`rictor_conditions.tsv`](../results/frozen/rictor_conditions.tsv)).
- **Disease-donor leave-one-out (LODO).** The disease vector is rebuilt with each of the 11
  synovium/blood donors removed in turn; RICTOR reversal stays positive in **11/11 folds**,
  in a narrow band **+0.154 to +0.167**
  ([`rictor_lodo.tsv`](../results/frozen/rictor_lodo.tsv)).
- **Perturbation-donor robustness.** Separately, the four Perturb-seq donors support six
  leave-two-out pairs used to check donor stability of the KD effect.
- **Responder-only support.** Restricting to responder strata, **93% of strata are positive
  and all donors are positive** for RICTOR
  ([`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv),
  `responder_support = yes_93pct_strata_all_donors`).

---

## 6. Screen-level scoring and attrition

The screen is a **branching decision map, not a linear funnel**; the denominators trace to
[`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv),
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv), and
[`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv).

- **S0 — screen-level reversal.** 924 perturbations with a usable genome-scale effect vector
  are scored against the corrected raw-count activated-memory disease vector; 208 are
  convergent (Pearson & Spearman & GSEA agree) at FDR < 0.10, and 716 are not advanced.
- **S1 — biological robustness.** Of the 208, **21** survive donor-consistent subvector,
  bootstrap, and jackknife checks; 187 broad or donor-unstable hits are not advanced.
- **S2 — safety / essentiality / modality.** **0** of the 21 are advanceable from the
  single-state screen; all 21 are constrained by essentiality/safety (e.g. broad hubs
  GNAS, STAT3, SMARCB1, TET2) or by absence of a credible modality (immune-directional but
  undruggable transcription factors such as KLF13, IRF9, ELF4). The single-state screen
  therefore returns **NO_ROBUST_CANDIDATE**.
- **Deep candidate branch.** PAK2 was deep-validated and then rejected; RICTOR was carried
  into a bounded pre-specified rescue and retained as a mechanism hypothesis; RIPK1 is a
  comparator only.

Not all 924 perturbations underwent every deep test — that would misrepresent the design.
Deep validation applies to the candidate-specific branch.

---

## 7. Matched-perturbation null

The screen-level statistic can be inflated by generic effect magnitude, breadth, or
knockdown quality. To ask whether RICTOR's reversal exceeds what a comparably-behaving
perturbation would produce, we build a **covariate-matched empirical null**
([`src/targetgate/calibration.py`](../src/targetgate/calibration.py);
[`matched_null.tsv`](../results/frozen/matched_null.tsv),
[`rictor_matched_null_values.tsv`](../results/frozen/rictor_matched_null_values.tsv)).

- **Matching features (5, z-scored):** effect `magnitude`, `breadth`,
  `donor_sign_consistency`, `guide_sign_concordance`, and on-target `ontarget_lfc`.
- **Neighbourhood:** the **k = 200** nearest perturbations by Euclidean distance in the
  z-scored feature space (200 unique matched controls).
- **Substrate:** the null is evaluated on the **conservative all-cell effect-vector
  projection**, so RICTOR is scored in the *same* space as its matched controls; on that
  substrate RICTOR's reversal is **+0.131** (7,393-gene intersection), not the +0.161
  responder-resolved value.
- **Result:** **7 of 200** matched perturbations exceed RICTOR, giving an **empirical
  p = 0.0398**, within-pool percentile 96.5 (global 97.9), z = 2.02. The finite-pool
  uncertainty is reported explicitly: **Wilson 95% CI (0.017, 0.070)**, Monte-Carlo
  bootstrap 95% CI (0.015, 0.065), seed-stable p range **[0.032, 0.042]**, pooled MC
  p = 0.034.

This is **Criterion 8 of the RICTOR gate and it is the weakest/most marginal** of the eight
checks: the Wilson/bootstrap interval grazes 0.05–0.07 on a 7/200 count. Accordingly we do
not claim decisive matched-null significance; nominal significance here is not definitive.
For PAK2 and RIPK1 the same null places them near the middle of their matched pools
(PAK2 global percentile 41; RIPK1 global percentile 42), consistent with no directional
support.

---

## 8. Confound decomposition

To distinguish disease-specific reversal from nonspecific transcriptional suppression, the
RICTOR reversal is recomputed after removing curated gene modules
([`confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv); base
+0.161 over 10,832 genes).

- Removing **cell-cycle** (+0.162), **activation** (+0.162), **stress** (+0.160),
  **apoptosis** (+0.161), or **T-cell-identity** (+0.160) genes leaves the reversal
  essentially unchanged (|delta| <= 0.0012). RICTOR reversal is **not** an artefact of these
  programmes.
- Removing the **780 strongly KD-down genes** drops the reversal to **+0.093**. That drop is
  *not* evidence of confound: those 780 genes **include the pathogenic disease-UP genes**
  (CXCR6, CCL4, IFNG and others), so removing them deletes real signal rather than a
  nuisance covariate. This distinction is recorded so the confound test cannot be misread
  as debunking the result.

---

## 9. Safety decomposition

Safety is a per-stratum decomposition of knockout-minus-control shifts across toxicity- and
identity-relevant scores ([`safety_summary.tsv`](../results/frozen/safety_summary.tsv)),
reported as mean delta, worst stratum, and fraction of strata with a consistent adverse
direction rather than a single pass/fail flag.

For RICTOR this yields a **mild, donor-inconsistent early-toxicity flag**: an apoptosis
mean delta of **+0.030** that is consistent in only ~33% of strata (worst stratum +0.075),
with T-cell and Treg identity preserved (T-identity mean +0.001, Treg mean -0.002). The
flag is surfaced, not suppressed, and folded into the final label's translational caveats.
PAK2, by contrast, is `specific_non_toxic` on the same decomposition — being non-toxic did
not rescue it, because it failed on therapeutic directionality.

---

## 10. GSEA directional check

Alongside the correlation statistics, a lightweight rank-based directional test asks whether
disease-UP genes sit at the KD-DOWN end of the ranked KD vector and disease-DOWN genes at the
KD-UP end (`gsea_reversal` in [`reversal.py`](../src/targetgate/reversal.py)). It returns a
normalized enrichment score for the disease-UP set (`nes_up`, negative when pushed down by
KD) and the disease-DOWN set (`nes_down`, positive when pushed up), and their difference; a
positive difference agrees with the centered-Pearson reversal. RICTOR's `gsea_reversal` is
strongly positive and same-direction, satisfying Criterion 3. The **leading edge**
([`leading_edge.tsv`](../results/frozen/leading_edge.tsv)) shows RICTOR knockdown turning
**down** the disease-UP genes CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, and RGS1, with none
reinforced. RIPK1, by contrast, has **both** GSEA NES components negative — an incoherent,
non-directional pattern.

---

## 11. Pre-specified RICTOR criteria and the retained label

Eight criteria were fixed **before** viewing the corrected raw-count result
([`analysis_contract.json`](../results/frozen/analysis_contract.json), `rictor_criteria`):

1. centered-Pearson reversal > 0
2. Spearman reversal > 0
3. ranked-GSEA reversal in the same direction
4. both RICTOR guides positive
5. all 11 disease-donor LODO folds positive
6. responder-only support
7. positive in all three conditions
8. above the matched-perturbation null at the frozen point estimate

RICTOR's primary responder-resolved reversal is **+0.161** (centered Pearson,
p = 1.8e-63, r^2 ~ 2.6% over 10,832 aligned genes), Spearman **+0.100**. Criteria 1–7 are
strong, convergent checks; **Criterion 8 is the weakest and most marginal** (§7).
The honest summary is: **RICTOR satisfied seven strong convergence checks and nominally
exceeded a matched-perturbation null, with borderline finite-pool uncertainty.** We do not
describe this as "8/8 decisive". The final public label is
**DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP**: RICTOR is a mechanism hypothesis
retained for the record, targeting the mTORC2 core scaffold, for which **no selective
small-molecule modality currently exists** (the "modality gap"). RICTOR is **not** a
validated drug target; systemic RICTOR inhibition is **not** shown to be safe.

---

## 12. Two substrates: reconciling +0.161 and +0.131

Two KD substrates coexist and must never be silently mixed:

- **Primary responder-resolved donor-RE meta** vector: reversal **+0.161** over 10,832
  genes (the headline effect size; §3).
- **Conservative all-cell effect-vector projection** (mean over conditions): reversal
  **+0.131** over the 7,393-gene intersection, used **only** to score RICTOR in the same
  space as the matched null (§7).

The **+0.030** difference decomposes into **-0.036** from the smaller gene universe and
**+0.066** from the responder-vs-all-cell representation. The all-cell number is the
**conservative** figure. Responder-resolved scores are never compared against all-cell
null-substrate scores.

---

## 13. PAK2 and RIPK1 decisions

**PAK2 — REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL**
(frozen internal label `REPRODUCIBLE_PAK2_RESPONDER_SIGNATURE_WITHOUT_THERAPEUTIC_RELEVANCE`).
PAK2 **passed** technical validation: on-target knockdown ~83–86% for both guides; guide
concordance 0.85 (100% direction agreement); a 112-gene frozen responder programme robust at
gene level across donor, guide and LODO; Mixscape responder fraction 76.5%; non-toxic
(`specific_non_toxic`). It **failed** therapeutic validation: disease reversal **+0.010,
p = 0.297** (not significant), matched-null percentile 41; responder NF-kB delta = -0.011
(p = 0.05, negligible, no donor-direction consistency); its external JIA enrichment is
**activation-confounded** (FROZEN_UP and FROZEN_DOWN modules co-elevate, diverge = False,
so `disease_relevant = False`); partial-inhibition sufficiency **NOT_ESTABLISHED**; and no
safer druggable immune-directional escape target passes the veto stack (0/10). PAK2 is a
real, reproducible cellular hit that was **rejected** as a target nomination. Removing the
therapeutic-directionality gate is exactly what would have let PAK2 read as advanceable
([`gate_ablation.tsv`](../results/frozen/gate_ablation.tsv)).

**RIPK1 — COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS.** Weak, incoherent
disease reversal **+0.038** (both GSEA NES negative), matched-null percentile 42. RIPK1 is a
benchmark comparator (real IBD/autoinflammatory genetics and clinical-stage kinase inhibitors
exist; full loss-of-function causes immunodeficiency, so kinase inhibition — not knockdown —
is the relevant modality). It is **not** nominated by this test.

The full pass/borderline/fail decomposition for all rows is in
[`gate_matrix.tsv`](../results/frozen/gate_matrix.tsv).

---

## 14. Superseded analyses

Earlier framings that are **not** current are recorded in
[`superseded_claims.json`](../results/frozen/superseded_claims.json) and
[Superseded results](SUPERSEDED_RESULTS.md), and never presented as headline results:

- **SUP-01** — an old RICTOR reversal of **~ +0.43** from a covariate-adjusted,
  residency-removed **77-gene** subset. It was inflated by the frozen-subset gene universe
  and a responder-only KD representation, and is **replaced** by the full-transcriptome
  primary **+0.161** and the conservative null-substrate **+0.131**. The ~+0.43 value must
  only ever appear in an explicitly superseded context.
- **SUP-02** — PAK2 JIA joint enrichment as disease support (UP/DOWN modules co-elevate →
  generic activation confound; not supported).
- **SUP-03** — PAK2 partial-inhibition support (both guides similarly strong →
  NOT_ESTABLISHED).
- **SUP-04** — a "safer PAK2 neighbour reproduces the programme" (gene-ID namespace mismatch
  + incomplete vetoes; none found).
- **SUP-05** — PAK2–WASF2 as a validated therapeutic axis (structural/directional evidence
  insufficient). The AF2/AF3 structural work is **not** the target-discovery result.

The adjusted-vector sensitivity analysis uses the same cohort and is **not** independent
biological replication.

---

## 15. Random seeds

All stochastic steps are seeded and recorded in
[`analysis_contract.json`](../results/frozen/analysis_contract.json): scoring seed **0**,
matched-null seed **0**, and Monte-Carlo replicate seeds **0–19** for the pooled/bootstrap
null. The seed-stable empirical-p range for RICTOR's matched null is **[0.032, 0.042]**.

---

## 16. Software and versions

Implemented in Python (`>= 3.10`) as the installable `targetgate` package
([`pyproject.toml`](../pyproject.toml); build backend hatchling). Core dependencies:
**numpy** (>= 1.26, < 3), **pandas** (>= 2.1, < 3), **scipy** (>= 1.11, < 2; Pearson,
Spearman, rank statistics), **matplotlib** (>= 3.8, < 4; figures), and **pyarrow**
(>= 14; parquet I/O). Pseudobulk differential expression uses **pydeseq2**. Development and
provenance tooling: **pytest** (>= 7.4), **ruff** (>= 0.4), **pre-commit** (>= 3.5).
Genome build **GRCh38**. Every frozen artifact and demo input carries a sha256 checksum in
[`results/frozen/results_manifest.json`](../results/frozen/results_manifest.json).

Compute for the server-scale stages (disease-vector build from the JIA h5ad, genome-scale
effect-vector construction, and the all-perturbation null) is described generically as a
high-memory **compute server** (`SERVER_DATA_ROOT` / `SERVER_RESULTS_ROOT`); no internal
hostnames or paths are hardcoded.

---

## 17. Confirmatory vs exploratory, and reproducibility

**Confirmatory (pre-specified):** the RICTOR 8-criterion bounded rescue and the PAK2
decision gate. **Exploratory:** the single-state 924-perturbation reversal screen (which
returned NO_ROBUST_CANDIDATE) and the old-vector sensitivity analysis (same cohort, not
independent replication). See `confirmatory_vs_exploratory` in
[`analysis_contract.json`](../results/frozen/analysis_contract.json).

Three reproducibility levels are provided (see [Reproducibility](REPRODUCIBILITY.md) and the
[configs](../configs)):

- **Level 1 — `make demo`:** laptop-scale, minutes, no server or private data. Recomputes
  the RICTOR/PAK2/RIPK1 reversals from committed compact inputs
  ([`data/demo/*.tsv.gz`](../data/demo)), regenerates tables and figures, and validates
  golden values.
- **Level 2 — `make reproduce`:** recomputes guide and LODO robustness from committed
  pseudobulk ([`data/reproduce/`](../data/reproduce)) and compares to frozen values at
  tolerance 5e-3.
- **Level 3 — `make full`:** server-scale (~128 GB RAM, hours). Downloads the open JIA h5ad
  and Perturb-seq data, rebuilds the disease vector and genome-scale effect vectors, and
  reruns everything. Where a required processed input cannot be rebuilt from a public source
  under its license, that limitation is stated prominently and Levels 1–2 remain the honest
  reproducibility guarantee.

---

## 18. Role of AI tooling and scope of claims

Claude Code was used for pipeline implementation, debugging, server execution, tests,
provenance, packaging, and the reproducibility audit; Claude (Science) was used for
hypothesis red-teaming, prior-art review, confound identification, safety and modality
assessment, external-dataset scouting, and contradiction/retraction checks. Model output is
**not** treated as scientific evidence: every biological claim resolves to a named data
artifact, a primary publication, or an official database. The most consequential
contribution was made **after the initial hypothesis failed** — designing stricter
falsification tests, preserving negative results, and preventing an attractive cellular hit
(PAK2) from being reported as an unsupported drug-target claim.

**What this analysis does not claim:** RICTOR is not a validated drug target; systemic RICTOR
inhibition is not shown to be safe; no selective RICTOR modality currently exists;
synovium-vs-blood is not disease-vs-healthy; the adjusted-vector sensitivity is not
independent replication; PAK2 is not an anti-inflammatory target; not all 924 perturbations
underwent deep validation; and nominal matched-null significance is not definitive.
