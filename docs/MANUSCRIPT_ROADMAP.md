# Manuscript roadmap

This document separates what the PerturbGate hackathon release establishes as
**frozen conclusions** from what a peer-reviewed manuscript would still require.
It is a planning document, not a results document. Nothing here changes any
frozen number or label; the authoritative record lives in
[`results/frozen/`](../results/frozen/) and is summarized in
[RESULTS.md](RESULTS.md), [CLAIMS_AND_EVIDENCE.md](CLAIMS_AND_EVIDENCE.md),
and the [decision trail](DECISION_TRAIL.md).

PerturbGate is *PerturbGate — Evidence-Gated Pipeline for T-cell Perturb-seq
Mechanism Hypotheses* (version 1.0.0, frozen hackathon release, 2026-07-13),
built for *Built with Claude: Life Sciences* (Anthropic x Gladstone Institutes),
Research track. Its central message is that **a real perturbation effect is
necessary but not sufficient for target nomination**: the pipeline is framed as
target *nomination*, not gene *ranking*, and every retained claim carries an
explicit record of how competing claims failed.

The purpose of a manuscript is not to upgrade the hackathon conclusions but to
subject the single surviving mechanism hypothesis (RICTOR) to the independent
tests that the hackathon scope could not include, and to report the negative and
comparator results (PAK2, RIPK1) with equal weight.

---

## A. Frozen hackathon conclusions (do not re-litigate)

These are fixed. Future work is layered on top of them and reported separately
(see [Section D](#d-versioning-policy)). Source of record:
[`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv)
and [`results/frozen/analysis_contract.json`](../results/frozen/analysis_contract.json).

### A.1 The three-target comparison set

| Target | Frozen public label | Primary reversal | Disposition |
|---|---|---|---|
| RICTOR | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` | +0.161 | Retained as a mechanism hypothesis |
| PAK2 | `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` | +0.010 (p = 0.297) | Rejected as a target nomination |
| RIPK1 | `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` | +0.038 | Benchmark comparator only |

Reversal is defined as `-centered_Pearson(KD_log2FC, disease_log2FC)` on the
primary responder-resolved donor random-effects meta KD vector against the JIA
disease vector; positive means reversing.

### A.2 RICTOR — retained, bounded

On the primary responder-resolved substrate (10,832 aligned genes), RICTOR
knockdown reverses the corrected activated-memory JIA synovium-vs-blood direction
at **+0.161** (centered Pearson, p = 1.8e-63, r^2 ~ 2.6%), Spearman **+0.100**.
It satisfied seven strong pre-specified convergence checks:

1. centered-Pearson reversal > 0 (+0.161);
2. Spearman reversal > 0 (+0.100);
3. ranked-GSEA reversal in the same direction;
4. both guides positive (RICTOR-1 +0.141, RICTOR-2 +0.178);
5. all 11/11 disease-donor leave-one-out folds positive (band +0.154..+0.167);
6. responder-only support (93% of strata positive, all donors positive);
7. positive in all three conditions (Rest +0.153, Stim8hr +0.092, Stim48hr +0.042).

The eighth criterion — exceeding a matched-perturbation null — is the weakest.
On the conservative all-cell null substrate the reversal is **+0.131**
(percentile 96.5; global 97.9), with **7 of 200** matched perturbations
exceeding RICTOR, empirical p = 0.0398, Wilson 95% CI (0.017, 0.070), Monte-Carlo
bootstrap 95% CI (0.015, 0.065), seed-stable p range [0.032, 0.042], pooled
p = 0.034. The frozen wording is therefore: **RICTOR satisfied seven strong
convergence checks and nominally exceeded a matched-perturbation null, with
borderline finite-pool uncertainty.** This is *not* "8/8 decisive criteria".

Supporting frozen observations: the reversal is confound-resistant (removing
cell-cycle / activation / stress / apoptosis / T-identity axes leaves it roughly
unchanged); the leading edge shows RICTOR turning **down** disease-UP genes
(CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, RGS1, with 0 reinforced); safety shows a
mild, donor-inconsistent early-tox flag (apoptosis +0.030, consistent in <=33% of
strata) with T-cell and Treg identity preserved; modality shows RICTOR as an
mTORC2 core scaffold with **no selective small-molecule modality** (the "modality
gap").

### A.3 PAK2 — real cellular hit, rejected as a nomination

PAK2 **passed technical validation** (on-target knockdown ~83-86% both guides;
guide concordance 0.85 with 100% direction agreement; a 112-gene frozen responder
programme robust at gene level across donor, guide and LODO; Mixscape responder
fraction 76.5%; non-toxic) but **failed therapeutic validation**: disease reversal
+0.010 (p = 0.297, not significant), matched-null 41st percentile; responder NF-kB
delta = -0.011 (p = 0.05, negligible, no donor-direction consistency); the external
JIA enrichment is **activation-confounded** (FROZEN_UP and FROZEN_DOWN modules
co-elevate, diverge = False, so disease_relevant = False); partial-inhibition
sufficiency **not established** (both guides similarly strong, no strong-versus-weak
titration axis); and no safer druggable immune-directional escape (0/10 passed the
veto stack). PAK2 is a reproducible cellular hit that is **not** an
anti-inflammatory target in this analysis.

### A.4 RIPK1 — comparator only

RIPK1 shows weak, incoherent disease reversal (+0.038, both GSEA NES negative),
matched-null 42nd percentile. It is included as a benchmark comparator (real
IBD/autoinflammatory genetics and clinical-stage kinase inhibitors exist; full
loss of function causes immunodeficiency, so kinase inhibition rather than
knockdown is the relevant modality). It is not nominated by this test.

### A.5 Screen-level attrition (branching, not a linear funnel)

Denominators trace to
[`results/frozen/candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv),
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv) and
[`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv):

- 924 perturbations scored at screen level on the activated-memory corrected
  raw-count disease vector;
- 208 convergent and FDR < 0.10; 716 not advanced;
- 21 biologically robust; 187 broad or donor-unstable, not advanced;
- 0 advanceable from the single-state screen; 21 safety/modality constrained ->
  `NO_ROBUST_CANDIDATE` (broad/essential hubs such as GNAS, STAT3, SMARCB1, TET2
  are safety-constrained; immune-directional but undruggable TFs such as KLF13,
  IRF9, ELF4 have `NO_CREDIBLE_MODALITY`).

Not all 924 perturbations underwent every deep test; the deep candidate branch is
PAK2 (deep-validated then rejected), RICTOR (bounded rescue, retained) and RIPK1
(comparator only). The single-state 924-perturbation screen is **exploratory**;
the RICTOR 8-criterion bounded rescue and the PAK2 decision gate are
**confirmatory** (see [`analysis_contract.json`](../results/frozen/analysis_contract.json)).

### A.6 What the hackathon release explicitly does NOT claim

RICTOR is **not** a validated drug target; systemic RICTOR inhibition is **not**
shown to be safe; **no** selective RICTOR modality currently exists; the
synovium-vs-blood contrast is **not** disease-versus-healthy; the
adjusted-vector sensitivity is same-cohort and is **not** independent biological
replication; PAK2 is **not** an anti-inflammatory target; nominal matched-null
significance is **not** definitive. Superseded intermediate claims (including the
old RICTOR reversal of ~+0.43) are recorded only as superseded in
[SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md) and
[`results/frozen/superseded_claims.json`](../results/frozen/superseded_claims.json)
and are never presented as current.

---

## B. Analyses still required for a manuscript

None of the following are done. Each would be run in a separate version/branch
(Section D) and would not overwrite any frozen number. They are ordered roughly
from most to least foundational for a RICTOR mechanism claim. The current
translational-readiness state is tracked in
[TRANSLATIONAL_REVIEW_STATUS.md](TRANSLATIONAL_REVIEW_STATUS.md); the honest
scope limits are in [LIMITATIONS.md](LIMITATIONS.md).

### B.1 Independent same-tissue disease validation (RA / OA / JIA)

The disease vector is a single JIA synovium-vs-blood contrast (activated-memory
CD4, raw-count donor-paired pseudobulk, 11 paired donors, 12,071 genes,
md5 `2b18d92684db1f70b637e1f098374c7e`). A manuscript needs the RICTOR reversal
re-tested against **independent** synovial CD4 datasets — additional JIA cohorts
and, critically, adult rheumatoid arthritis (RA) and osteoarthritis (OA) as a
disease-specificity contrast — computed with the identical pipeline and the same
sign convention. The pre-registered success measure is a positive reversal point
estimate with a reported effect size and confidence interval in each independent
tissue, not merely a p-value. OA in particular tests whether the direction is
inflammatory-arthritis-specific rather than generic synovial residency.

### B.2 Cross-cohort replication

Beyond a single independent dataset, the reversal should be evaluated across
multiple cohorts and platforms, with a random-effects meta-estimate and a
between-cohort heterogeneity statistic. This distinguishes a reproducible
directional effect from a cohort-specific one and would replace the current
single-cohort estimate as the headline directional evidence.

### B.3 Partial-inhibition / dose-response

Knockdown is not inhibition. Because no selective RICTOR modality exists
(Section A.2) and because partial-inhibition sufficiency was explicitly **not
established** for PAK2 (both guides similarly strong; see
[SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md), SUP-03), a manuscript needs a
graded perturbation axis for RICTOR: a strong-versus-weak knockdown titration, or
degron / inducible / graded-CRISPRi series, to ask whether the disease-reversing
direction is preserved at sub-maximal target engagement. Pre-registered readout:
whether reversal is monotone in on-target reduction and at what fractional
engagement it is lost.

### B.4 Improved matched-control calibration on a larger independent pool

Criterion 8 is the weakest link: the matched null used a 200-perturbation pool
(k = 200 nearest neighbours on magnitude, breadth, donor-sign-consistency,
guide-sign-concordance and on-target LFC), 7 of which exceeded RICTOR
(empirical p = 0.0398, Wilson CI up to ~0.070). A manuscript should re-run the
matched-null calibration against a substantially larger, independent
perturbation pool, report the tightened finite-pool interval, and pre-specify the
significance threshold before unblinding. The two substrates must never be
silently mixed: the primary responder-resolved score (+0.161, 10,832 genes) and
the conservative all-cell null substrate (+0.131, 7,393-gene intersection) live
in different spaces (the +0.030 gap decomposes into -0.036 gene-universe and
+0.066 responder-to-all-cell representation; see
[`confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv)).

### B.5 Final RICTOR safety / genetics / modality audit

A manuscript-grade audit would extend the frozen mild, donor-inconsistent
early-tox flag (apoptosis +0.030, <=33% of strata) into: (i) a human-genetics
review (constraint, known loss-of-function phenotypes, mTORC2/RICTOR biology);
(ii) an essentiality/dependency review across immune and non-immune lineages;
(iii) an explicit modality assessment of the mTORC2 scaffold, stating whether any
selective modality is even conceivable, since none currently exists. This audit
must be able to *veto* the nomination; a retained hypothesis is not a validated
target.

### B.6 Cell-type specificity

The primary vector is activated-memory CD4. A manuscript needs to resolve whether
the RICTOR reversal is specific to particular CD4 states/subsets (e.g. resident
versus circulating, effector versus regulatory) or is broadly shared, and whether
Treg identity is preserved when RICTOR is perturbed in the relevant subset. This
determines whether a hypothetical intervention would act on a defined pathogenic
compartment or indiscriminately.

### B.7 Prospective experimental validation

All current evidence is computational and retrospective on public data. A
manuscript claim of mechanism benefits from a prospective wet-lab arm: an
independent RICTOR perturbation in primary human synovial or activated CD4 T
cells with a pre-specified readout of the leading-edge disease-UP genes
(CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, RGS1), testing whether they move down as
predicted. This is the step that would convert a directional hypothesis into a
tested one.

### B.8 Pre-registration of future criteria

Before any of B.1-B.7 is unblinded, the acceptance criteria, substrates, gene
universes, sign conventions, null construction and significance thresholds should
be pre-registered — mirroring the frozen 8-criterion contract in
[`analysis_contract.json`](../results/frozen/analysis_contract.json). This keeps
the confirmatory/exploratory boundary explicit and prevents post-hoc criterion
drift. Same-cohort sensitivity analyses must continue to be labelled as such and
never presented as independent replication.

---

## C. Possible manuscript structure

A candidate structure (illustrative, not binding). It deliberately foregrounds
the gating logic and the negative/comparator results rather than a single
positive hit.

1. **Introduction** — target nomination versus gene ranking; why a real
   perturbation effect is necessary but not sufficient; the evidence-gating idea.
2. **Data and disease direction** — the CD4 Perturb-seq substrate and the
   donor-paired JIA synovium-vs-blood disease vector; open-data provenance
   ([DATA_AVAILABILITY.md](DATA_AVAILABILITY.md),
   [DATA_LICENSES.md](DATA_LICENSES.md)).
3. **Methods** — reversal scoring, guide/donor/condition/LODO robustness, the
   matched-perturbation null with finite-pool uncertainty, confound removal, and
   the pre-specified decision contract ([METHODS.md](METHODS.md)).
4. **Screen-level attrition** — the branching decision map (924 -> 208 -> 21 ->
   0 advanceable) and why robustness alone does not yield a nomination
   (Figure 1, target attrition).
5. **PAK2 — technical success, therapeutic rejection** — reproducible responder
   programme that fails directionality and is activation-confounded (Figure 4,
   PAK2 rejection).
6. **RICTOR — bounded rescue** — the seven convergence checks plus the nominal,
   finite-pool-limited null result; leading edge; confound resistance
   (Figure 2, directionality and null; supplementary RICTOR robustness).
7. **Comparators and gate ablation** — RIPK1 and the gate matrix / gate ablation
   showing which checks are load-bearing (Figure 3, gate matrix; supplementary
   gate ablation).
8. **Independent validation** — Section B analyses (RA/OA/JIA replication,
   cross-cohort meta-estimate, dose-response, prospective arm) once completed.
9. **Limitations and non-claims** — carried directly from
   [LIMITATIONS.md](LIMITATIONS.md) and [FAILURE_MODES.md](FAILURE_MODES.md); the
   modality gap; synovium-vs-blood is not disease-vs-healthy.
10. **Role of AI-assisted analysis** — the honest account in
    [CLAUDE_USAGE.md](CLAUDE_USAGE.md): implementation, red-teaming, confound
    identification and preservation of negative results; AI output is not
    evidence and every claim resolves to a data artifact, primary paper or
    database.
11. **Data and code availability / reproducibility** — the three honest
    reproducibility levels ([REPRODUCIBILITY.md](REPRODUCIBILITY.md),
    [REPRODUCIBILITY_LEVELS.md](REPRODUCIBILITY_LEVELS.md)).

Figures already generated and available under [`figures/`](../figures/):
`figure_1_target_attrition`, `figure_2_directionality_and_null`,
`figure_3_gate_matrix`, `figure_4_pak2_rejection`,
`supplementary_gate_ablation`, `supplementary_rictor_robustness` (each with PNG,
SVG and source data).

---

## D. Versioning policy

The frozen hackathon result is immutable. Manuscript-stage work extends it; it
does not edit it.

- **The frozen release is version 1.0.0 (2026-07-13).** Every number and label in
  [`results/frozen/`](../results/frozen/) and in the frozen labels list of
  [`analysis_contract.json`](../results/frozen/analysis_contract.json) is fixed at
  that version and is the citable record of the hackathon submission.
- **Future analyses live in a separate branch and a new version.** Section B work
  is developed on its own branch and released under a new version tag (a new minor
  or major version per [semantic versioning](https://semver.org/), following the
  existing [CHANGELOG.md](../CHANGELOG.md) convention). It never commits over the
  frozen artifacts.
- **Never overwrite the frozen hackathon result.** If a future independent
  analysis changes a conclusion, the frozen artifact stays in place and the change
  is recorded additively — a new artifact plus a superseding entry in the claim
  ledger ([`claims.json`](../results/frozen/claims.json)) and, where a prior claim
  is retired, in [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md) /
  [`superseded_claims.json`](../results/frozen/superseded_claims.json). Superseded
  material is always labelled as superseded and is never re-presented as current
  (the old RICTOR ~+0.43 is the canonical example).
- **Pre-registration precedes unblinding.** New confirmatory criteria (Section
  B.8) are committed before the corresponding independent result is viewed, and the
  confirmatory-versus-exploratory and same-cohort-versus-independent-replication
  distinctions are preserved in every subsequent version.
- **Provenance and privacy rules carry forward unchanged.** Every biological claim
  continues to resolve to a data artifact, a primary paper or an official
  database; compute is described only as "server"/"batch server"; AI-assisted
  analysis is not treated as scientific evidence.

---

*Related documents:* [RESULTS.md](RESULTS.md) ·
[METHODS.md](METHODS.md) · [DECISION_TRAIL.md](DECISION_TRAIL.md) ·
[FAILURE_MODES.md](FAILURE_MODES.md) · [LIMITATIONS.md](LIMITATIONS.md) ·
[CLAIMS_AND_EVIDENCE.md](CLAIMS_AND_EVIDENCE.md) ·
[SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md) ·
[TRANSLATIONAL_REVIEW_STATUS.md](TRANSLATIONAL_REVIEW_STATUS.md) ·
[REPRODUCIBILITY.md](REPRODUCIBILITY.md) ·
[DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) · [CLAUDE_USAGE.md](CLAUDE_USAGE.md)
