# Translational review status

**Status: COMPLETE (this release).**
**Scope: RICTOR only.**
**Verdict: `NOT_ADVANCEABLE_WITH_CURRENT_EVIDENCE_AND_MODALITIES` (translational STOP).**
**Effect on the core repository: the frozen biological result is unchanged; this adds a
second, independent axis.**

This page records the state of the RICTOR *translational* audit. It exists so that the
retained RICTOR hypothesis is never read as more than it is. The frozen analysis
establishes a bounded, directionally-robust disease-reversal signal for RICTOR
knockdown; it does **not** establish that RICTOR is a drug target. The translational
audit is now complete: **modality** (no validated selective agent), **human-genetic
efficacy** (no support; strong loss constraint), and **systemic safety** (essentiality
+ opposing cell-type effects) were assessed and together yield a **STOP** verdict;
**independent same-tissue replication** remains the one genuinely open item and is
scoped as a future-validation plan (not causal validation). Full detail with verified
PMIDs/DOIs: [TRANSLATIONAL_AUDIT_UPDATE.md](TRANSLATIONAL_AUDIT_UPDATE.md) and
[results/translational/RICTOR_TRANSLATIONAL_VERDICT.md](../results/translational/RICTOR_TRANSLATIONAL_VERDICT.md).

RICTOR's controlled public label already encodes this boundary:
`DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`. It is a mechanism-node hypothesis
with an acknowledged modality gap, not a validated target.

---

## What is already bounded (context, not closure)

The evidence that motivates a *translational* review — rather than dismissal — is the
directional convergence summarised in [RESULTS.md](RESULTS.md) and
[`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv):

- Primary responder-resolved reversal **+0.161** (centered-Pearson; r² ≈ 2.6% over
  **10,832** aligned genes). Direction is robust; magnitude is small.
- Both guides positive (RICTOR-1 **+0.141**, RICTOR-2 **+0.178**); Spearman **+0.100**.
- **11 of 11** disease-donor leave-one-out folds positive (band **+0.154 to +0.167**).
- Positive in all three conditions (Rest **+0.153**, Stim8hr **+0.092**,
  Stim48hr **+0.042**).
- Conservative all-cell null-substrate projection **+0.131**; matched-perturbation null
  percentile **96.5** (global 97.9), with **7 of 200** matched perturbations exceeding
  RICTOR (empirical p ≈ 0.040; Wilson 95% CI 0.017–0.070; MC-bootstrap 95% CI
  0.015–0.065).

The pre-specified rescue was a **confirmatory** test (the eight RICTOR criteria were
fixed before the raw-count result was viewed; see
[`results/frozen/analysis_contract.json`](../results/frozen/analysis_contract.json)).
The summary of that test is deliberately worded as: **RICTOR satisfied seven strong
convergence checks and nominally exceeded a matched-perturbation null, with borderline
finite-pool uncertainty.** The matched-null criterion is the weakest of the eight and is
not treated as decisive. This is context for why the translational review is open — it
is not itself a translational result.

Everything below is what that bounded signal does **not** yet answer.

---

## Open item 1 — Modality (PENDING)

**Current state.** RICTOR is a core scaffold subunit of mTORC2. There is **no selective
small-molecule modality** against RICTOR itself; the measured reversal leans on RICTOR's
selective downregulation arm (a knockdown effect), which is a genetic perturbation, not a
demonstrated therapeutic intervention. This gap is named directly in the public label
(`..._WITH_MODALITY_GAP`).

**What is required to close it.**
- Identification of a selective, tractable modality acting on RICTOR / mTORC2 in the
  disease-beneficial direction (for example a selective inhibitor or degrader with
  demonstrated directional effect), or an explicit statement that no such modality
  exists at time of review.
- Evidence that the therapeutically achievable perturbation reproduces the
  knockdown-direction signal, rather than assuming equivalence between knockdown and
  pharmacological inhibition.

**We do not claim** that a druggable RICTOR route exists.

## Open item 2 — Safety (PENDING)

**Current state.** A mild, **donor-inconsistent** early-toxicity flag is present:
apoptosis Δ (knockout minus control) **+0.030**, consistent in **≤ 33%** of strata
(see [`results/frozen/safety_summary.tsv`](../results/frozen/safety_summary.tsv)).
T-cell and Treg identity are preserved in the perturbation data. This is a cellular,
single-dataset observation only.

**What is required to close it.**
- Assessment of systemic / sustained RICTOR-inhibition safety, which cannot be inferred
  from a single Perturb-seq cohort and is not established here.
- Resolution of the early-toxicity flag against an independent readout, given its
  donor-inconsistency in the present data.

**We do not claim** that systemic RICTOR inhibition is safe.

## Open item 3 — Human-genetic direction (PENDING)

**Current state.** Whether human genetics support inhibition of RICTOR / mTORC2 in the
**disease-beneficial** direction has **not been evaluated** in this project. The frozen
analysis is transcriptomic and cellular; it does not incorporate human genetic
association or allelic-direction evidence for RICTOR.

**What is required to close it.**
- A directional human-genetics assessment (association and, where available,
  coding-variant / loss-of-function directionality) linking RICTOR / mTORC2 to the
  relevant disease axis, resolving whether the genetically-supported direction is
  consistent with therapeutic inhibition.
- An explicit record if human genetics are **absent or contradictory**, since either
  outcome bounds the hypothesis.

This item is **unevaluated**; no direction is asserted here.

## Open item 4 — Independent same-tissue replication (PENDING)

**Current state.** All disease-direction statistics derive from a **single** JIA
synovial atlas (**11** paired donors; disease vector md5
`2b18d92684db1f70b637e1f098374c7e`). The leave-one-donor-out analysis (11/11 folds
positive) demonstrates **within-cohort** robustness, not cross-cohort replication. The
old covariate-adjusted vector (+0.147) is a **same-cohort sensitivity analysis**, not
independent biological replication — it re-uses the same donors. Two additional design
bounds apply: the disease contrast is **synovium (tissue + fluid) versus blood**, an
inflamed-site-versus-circulation surrogate, **not** disease-versus-healthy tissue; and the
primary (+0.161, responder-resolved) and conservative (+0.131, all-cell null-substrate)
substrates measure the same directional effect in two deliberately different spaces and
are never mixed silently.

**What is required to close it.**
- Recomputation of the RICTOR reversal on an **independent** same-tissue (synovial CD4)
  cohort, ideally including a disease-versus-healthy contrast, using the identical scoring
  contract.
- A concordance statement across cohorts (direction, magnitude band, and donor
  robustness), reported with denominators and uncertainty rather than a single p-value.

**We do not claim** that the same-cohort sensitivity analysis constitutes independent
replication.

---

## Closure criteria (summary)

| Item | Axis | Current status | Closes when |
| --- | --- | --- | --- |
| 1 | Modality | PENDING — modality gap named | A selective, tractable, directionally-consistent RICTOR/mTORC2 modality is identified, or its absence is stated |
| 2 | Safety | PENDING — mild donor-inconsistent early-tox flag (apoptosis Δ +0.030, ≤ 33% strata) | Systemic-inhibition safety is assessed and the early-tox flag is resolved against an independent readout |
| 3 | Human-genetic direction | PENDING — not evaluated | A directional human-genetics assessment resolves (or is recorded as absent/contradictory) |
| 4 | Independent same-tissue replication | PENDING — single JIA cohort (11 donors); LODO is within-cohort | The reversal is recomputed on an independent synovial-CD4 cohort with a concordance statement |

Until all four items are resolved, this review is **PENDING** and RICTOR remains a
bounded mechanism-node hypothesis. Resolving them does not, by itself, upgrade the label;
it removes the reasons this review is open.

---

## Why this does not block the core repository

The core repository is a **target-nomination pipeline with an explicit falsification
record**, not a drug-target validation. Its deliverable is the retained/rejected/superseded
claim set and the reproducible machinery that produced it — all of which is frozen and
complete independent of this translational review:

- The frozen results, gates, and figures (including
  [`figure_2_directionality_and_null`](../figures/figure_2_directionality_and_null.png)
  and [`supplementary_rictor_robustness`](../figures/supplementary_rictor_robustness.png))
  stand on the committed inputs and reproduce at all three levels (see
  [REPRODUCIBILITY_LEVELS.md](REPRODUCIBILITY_LEVELS.md)).
- The other two candidates are already terminal within this analysis: **PAK2** is
  `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` (a real cellular hit —
  reversal **+0.010**, matched-null 41st percentile — rejected as a nomination), and
  **RIPK1** is `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` (weak/incoherent
  reversal **+0.038**, matched-null 42nd percentile; a benchmark comparator only). Neither
  depends on this page.
- RICTOR's open translational status is a *feature* of the pipeline's design, not a
  defect: the pipeline's purpose is to stop an attractive cellular signal from becoming an
  unsupported drug-target claim. Recording these four items as open — rather than
  resolving them by assertion — is that design working as intended.

The distinction between what is established (a bounded, directionally-robust reversal) and
what is not (modality, safety, human-genetic direction, independent replication) is stated
consistently across [LIMITATIONS.md](LIMITATIONS.md), [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md),
[FAILURE_MODES.md](FAILURE_MODES.md), and the "What we do not claim" box in the
[README](../README.md).

---

*This document assigns no translational verdict. It is a status record of open items and
their closure criteria.*
