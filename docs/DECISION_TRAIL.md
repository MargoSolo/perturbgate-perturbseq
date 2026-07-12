# Decision trail

This document reconstructs how PerturbGate moved from a genome-scale T-cell
Perturb-seq screen to three final, explicitly-labelled mechanism claims. It is
deliberately drawn as a **branching decision map, not a linear funnel**. Two
things follow from that framing and should be read before the tables below.

1. **This is target *nomination*, not gene *ranking*.** A perturbation that
   produces a real, reproducible transcriptional effect has cleared a
   *necessary* bar, not a *sufficient* one. Every stage below asks a different
   falsification question, and a candidate can clear one and fail the next.
   PerturbGate's result is not that it found a positive hit; it is that every
   retained claim carries an explicit record of how competing claims failed.

2. **Not all 924 perturbations were deep-validated.** The screen-wide stages
   (Track A) scored and filtered the full set, but only a small deep-candidate
   branch (Track B) was carried through responder-, guide-, donor-, condition-,
   confound- and disease-directionality testing. The 924 → 208 → 21 → 0
   attrition and the PAK2 / RICTOR / RIPK1 candidate branches are **parallel
   evidence tracks on different substrates**, not a single pipe. Do not read the
   deep candidates as "the survivors of the 924".

Every denominator, disposition count and label in this document traces to a
frozen artifact under [`results/frozen/`](../results/frozen/); the two governing
ledgers are [`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv)
(stage-level attrition) and
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv)
(per-perturbation disposition and controlled reason codes). Effect sizes, method
detail and the disease-vector definition are documented in
[Methods](METHODS.md); superseded framings are catalogued in
[Superseded results](SUPERSEDED_RESULTS.md); recompute instructions are in
[Reproducibility](REPRODUCIBILITY.md).

---

## The map at a glance

```
  Track A — screen-wide attrition (single-state 924-perturbation screen)
  S0  924 scored ──► 208 convergent+FDR<0.10 ──► S1  21 biologically robust ──► S2  0 advanceable
       (716 not advanced)             (187 not advanced)          (21 safety/modality constrained)
                                                                        └─► NO_ROBUST_CANDIDATE

  Track B — deep candidate branches (carried leads, evaluated on the corrected raw-count disease vector)
  D0  PAK2  ──► REJECTED after deep validation   (technical pass, therapeutic fail)
  R0  RICTOR ──► RETAINED as mechanism hypothesis (bounded pre-specified rescue, modality gap)
  C0  RIPK1 ──► COMPARATOR only                   (benchmark, not nominated by this test)
```

The two tracks do not share a denominator. Track A is an exploratory
single-state screen that terminated with **no advanceable candidate**. Track B
evaluates a small set of leads (PAK2 carried from the prior robustness spine,
RICTOR as a separate bounded pre-specified rescue, RIPK1 as an external
benchmark comparator) against the JIA synovium-vs-blood corrected raw-count
disease vector.

---

## Stage ledger (all stages, both tracks)

| Stage | Scope | Denominator (definition) | n entering | Advanced | Not advanced | Rejected | Unresolved | Principal reason categories | Source artifact |
|-------|-------|--------------------------|-----------:|---------:|-------------:|---------:|-----------:|-----------------------------|-----------------|
| **S0** Screen-level reversal scoring | SCREEN_WIDE | all perturbations with a usable genome-scale effect vector | 924 | 208 | 716 | 0 | 0 | `NO_MEASURABLE_EFFECT`; `NOT_ADVANCED_FROM_SCREEN` | `all_perturbations_authoritative_reversal.tsv` |
| **S1** Biological robustness (donor-consistent subvector + bootstrap + jackknife) | SCREEN_WIDE | convergent (Pearson & Spearman & GSEA) and FDR<0.10 screen hits | 208 | 21 | 187 | 0 | 0 | `BROAD_TRANSCRIPTIONAL_EFFECT`; `DONOR_UNSTABLE` | `rejection_ledger.tsv` |
| **S2** Safety / essentiality / tractability / modality | SCREEN_WIDE | biologically robust screen shortlist | 21 | 0 | 0 | 21 | 0 | `ESSENTIALITY_OR_SAFETY_LIABILITY`; `NO_CREDIBLE_MODALITY`; `BROAD_TRANSCRIPTIONAL_EFFECT` | `rejection_ledger.tsv` |
| **D0** PAK2 deep candidate validation | CANDIDATE_SPECIFIC | lead candidate carried from the prior robustness spine | 1 | 0 | 0 | 1 | 0 | `NOT_THERAPEUTICALLY_DIRECTIONAL`; `GENERIC_ACTIVATION_SUPPRESSION`; `PARTIAL_INHIBITION_NOT_ESTABLISHED` | `primary_comparison.tsv` |
| **R0** RICTOR bounded pre-specified rescue (8 criteria) | CANDIDATE_SPECIFIC | separate bounded rescue on the corrected raw-count disease vector | 1 | 1 | 0 | 0 | 0 | `RETAINED_MECHANISM_HYPOTHESIS` | `rictor_guides.tsv`; `rictor_lodo.tsv`; `rictor_conditions.tsv`; `matched_null.tsv` |
| **C0** RIPK1 comparator | CANDIDATE_SPECIFIC | benchmark comparator perturbation | 1 | 0 | 1 | 0 | 0 | `COMPARATOR_ONLY` | `primary_comparison.tsv` |

The stage rows, denominators and counts above are reproduced verbatim from
[`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv).

---

## Track A — screen-wide attrition (924 → 208 → 21 → 0)

Track A is the **exploratory** single-state screen on the frozen corrected
raw-count activated-memory JIA disease vector. It is not confirmatory, and it did
not nominate a target.

### S0 — Screen-level reversal scoring (denominator: 924)

All 924 perturbations that had a usable genome-scale effect vector were scored
for disease-vector reversal. **208** were convergent across the centered-Pearson,
Spearman and ranked-GSEA reversal statistics *and* passed FDR < 0.10; the
remaining **716 were not advanced** (`NO_MEASURABLE_EFFECT` /
`NOT_ADVANCED_FROM_SCREEN`). No perturbation was rejected at S0 — failing to
advance from a screen is a weaker statement than a substantive rejection, and the
ledger keeps them distinct. Source:
[`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv).

### S1 — Biological robustness (denominator: 208)

The 208 convergent, FDR-passing hits were tested for donor-consistent signal
(donor-consistent subvector, bootstrap, leading-edge jackknife). **21** were
biologically robust; **187 were not advanced** because their reversal was a
`BROAD_TRANSCRIPTIONAL_EFFECT` or was `DONOR_UNSTABLE`. Source:
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv).

### S2 — Safety / essentiality / tractability / modality (denominator: 21)

The 21-perturbation robust shortlist was passed through an external safety,
essentiality, tractability and modality layer. **0 advanced; all 21 were
rejected** as safety- or modality-constrained, giving the single-state screen a
terminal verdict of **`NO_ROBUST_CANDIDATE`**. The rejections fall into two
recurring patterns visible in the ledger:

- **Broad / essential hubs — safety-constrained** (`ESSENTIALITY_OR_SAFETY_LIABILITY`):
  e.g. GNAS, STAT3, SMARCB1, TET2 (FOXP3 collapse, pan-essential machinery,
  tumour-suppressor or severe-immunodeficiency flags).
- **Immune-directional but undruggable transcription factors —
  `NO_CREDIBLE_MODALITY`**: e.g. KLF13, IRF9, ELF4.

A handful survive only as exploratory or non-specific-broad-reverser classes
(e.g. BRD1, INSR) and are not nominations. Source:
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv).

**Track A conclusion:** the single-state screen produced no advanceable target.
This is a preserved negative result, not a gap to be filled by relaxing the
gates.

---

## Track B — deep candidate branches (PAK2 rejected, RICTOR retained, RIPK1 comparator)

Track B carries a small number of leads through deep validation against the
corrected raw-count disease vector. Each branch has a denominator of one; the
point of the branch is the *reason*, not the count. Authoritative effect sizes
are in [`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv).

### D0 — PAK2: `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` → REJECTED

PAK2 is the clearest illustration of *necessary but not sufficient*: it **passed
technical validation and was rejected on therapeutic grounds**.

- **Passed (technical):** on-target knockdown ~83–86 % for both guides; guide
  concordance 0.85 with 100 % direction agreement; a 112-gene frozen responder
  programme robust to donor, guide and leave-one-donor-out at the gene level;
  Mixscape responder fraction 76.5 %; non-toxic (`specific_non_toxic`).
- **Failed (therapeutic directionality):** disease reversal **+0.010
  (p = 0.297, not significant)**, sitting at the **41st percentile** of the
  matched-perturbation null; responder NF-κB delta **−0.011 (p = 0.05,
  negligible)** with no donor-direction consistency; the external JIA joint
  enrichment is **activation-confounded** — the frozen UP and DOWN modules
  co-elevate together (`diverge = False`), so `disease_relevant = False`;
  partial-inhibition sufficiency `NOT_ESTABLISHED` (both guides knock down
  similarly hard, giving no strong-vs-weak titration axis); and **0 / 10**
  candidate escape neighbours passed the safer-druggable-directional veto stack.

Disposition: `NOT_THERAPEUTICALLY_DIRECTIONAL`; `GENERIC_ACTIVATION_SUPPRESSION`;
`PARTIAL_INHIBITION_NOT_ESTABLISHED` → final evidence class
**`REJECTED_AFTER_DEEP_VALIDATION`**. PAK2 is a real, reproducible cellular hit;
it is **not** an anti-inflammatory target nomination. Several earlier PAK2
framings are explicitly retired in [Superseded results](SUPERSEDED_RESULTS.md)
(SUP-02 through SUP-05).

### R0 — RICTOR: `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` → RETAINED

RICTOR is the only branch retained, and it is retained as a **mechanism
hypothesis**, not a validated drug target. It was evaluated in a **bounded,
pre-specified rescue** with eight criteria fixed before the raw-count result was
viewed (listed in [Methods](METHODS.md) and `analysis_contract.json`).

RICTOR **satisfied seven strong convergence checks and nominally exceeded a
matched-perturbation null, with borderline finite-pool uncertainty.** In detail:

- centered-Pearson responder-resolved reversal **+0.161** (p = 1.8e-63,
  r² ≈ 2.6 %, 10,832 aligned genes) and Spearman **+0.100**, same direction as
  ranked-GSEA;
- **both guides positive** (RICTOR-1 +0.141, RICTOR-2 +0.178);
- **11 / 11 disease-donor leave-one-out folds positive** (band +0.154…+0.167);
- **positive in all three conditions** (Rest +0.153, Stim8hr +0.092,
  Stim48hr +0.042);
- responder-only support: 93 % of strata positive, all donors positive;
- leading edge turns **down** the pathogenic disease-UP genes CXCL13, CXCR6,
  CCL4, IFNG, GZMB, PDCD1, RGS1 (0 reinforced);
- **confound-resistant** (removing cell-cycle, activation, stress, apoptosis and
  T-identity axes leaves the reversal essentially unchanged).

The **weakest / most marginal** criterion is criterion 8, the matched-null test.
On the conservative all-cell null substrate the reversal is **+0.131**, at
percentile **96.5** (global 97.9); **7 of 200** matched perturbations exceed
RICTOR, giving empirical **p = 0.0398**, Wilson 95 % CI **(0.017, 0.070)**, MC
bootstrap 95 % CI (0.015, 0.065), seed-stable p in [0.032, 0.042], pooled
p = 0.034. This is a **nominal** pass with real finite-pool uncertainty out to
~0.07, and it should never be described as "8/8 decisive".

Disposition: `RETAINED_MECHANISM_HYPOTHESIS` → final evidence class
**`RETAINED_MECHANISM_HYPOTHESIS`**, carried with the following open
limitations, which are part of the label and not footnotes:

- **Modality gap.** RICTOR is the mTORC2 core scaffold; there is **no selective
  small-molecule modality** for it today.
- **Safety.** A mild, donor-inconsistent early-toxicity flag (apoptosis +0.030,
  consistent in ≤ 33 % of strata); T-cell and Treg identity are preserved.
- **Not independent replication.** Synovium-vs-blood is not disease-vs-healthy,
  and the same-cohort adjusted-vector sensitivity is not an independent
  biological replicate.

The superseded ~+0.43 RICTOR figure (SUP-01) — an inflated frozen-subset /
residency-removed 77-gene estimate — is **not** a current result and is retained
only in [Superseded results](SUPERSEDED_RESULTS.md).

### C0 — RIPK1: `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` → COMPARATOR only

RIPK1 is included as an **external benchmark comparator**, not a nomination by
this test. Its disease reversal here is **weak and incoherent, +0.038** (both
GSEA NES negative), at the **42nd percentile** of the matched null. RIPK1 has
genuine IBD / autoinflammatory human genetics and clinical-stage kinase
inhibitors, but full loss-of-function causes immunodeficiency, so the relevant
modality is kinase inhibition rather than knockdown — which is why a knockdown
reversal test is not the right instrument for it. Disposition:
`COMPARATOR_ONLY` → **`COMPARATOR_ONLY`**. It calibrates the analysis; it is
**not nominated by this test**.

---

## Controlled rejection vocabulary

Dispositions use a fixed vocabulary so that "did not advance", "rejected" and
"retained" mean the same thing across the screen and the deep branches. Two
controlled fields carry it: `principal_reason_categories` in
[`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv) and
`final_evidence_class` in
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv).

**Stage reason categories** (`candidate_funnel.tsv`):

| Code | Meaning |
|------|---------|
| `NO_MEASURABLE_EFFECT` | No usable / measurable reversal signal at the screen level |
| `NOT_ADVANCED_FROM_SCREEN` | Below the convergence + FDR bar; not carried forward (weaker than a rejection) |
| `BROAD_TRANSCRIPTIONAL_EFFECT` | Reversal driven by a broad, non-specific transcriptional shift |
| `DONOR_UNSTABLE` | Signal not consistent across donors |
| `ESSENTIALITY_OR_SAFETY_LIABILITY` | Essential / broad hub or safety liability |
| `NO_CREDIBLE_MODALITY` | Immune-directional but no credible drug modality |
| `NOT_THERAPEUTICALLY_DIRECTIONAL` | Real cellular effect that does not move disease in the therapeutic direction |
| `GENERIC_ACTIVATION_SUPPRESSION` | Apparent disease relevance is a generic activation confound |
| `PARTIAL_INHIBITION_NOT_ESTABLISHED` | No strong-vs-weak titration axis to support partial inhibition |
| `RETAINED_MECHANISM_HYPOTHESIS` | Carried forward as a bounded mechanism hypothesis (not a validated target) |
| `COMPARATOR_ONLY` | Benchmark comparator; not nominated by this test |

**Final evidence classes** (`rejection_ledger.tsv`):
`SAFETY_CONSTRAINED`, `EXPLORATORY_SINGLE_STATE_HIT`,
`NONSPECIFIC_BROAD_REVERSER`, `REJECTED_AFTER_DEEP_VALIDATION`,
`COMPARATOR_ONLY`, `RETAINED_MECHANISM_HYPOTHESIS`.

Only three **public** outcome labels are used for the deep candidates, and only
these three:

- `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` (RICTOR)
- `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` (PAK2)
- `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` (RIPK1)

---

## A note on substrates (why the two tracks are not comparable line-by-line)

The screen-level `screen_reversal` values in
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv) (e.g. PAK2
−0.066, RIPK1 −0.033, RICTOR +0.085 on the single-state screen substrate) are
**not** the deep-validation numbers in
[`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv) (RICTOR
primary **+0.161** on the responder-resolved donor-RE meta over 10,832 genes).
Two substrates are used on purpose and must not be silently mixed:

- **Primary (responder-resolved) substrate** — the responder-DE donor
  random-effects meta knockdown vector, full transcriptome (10,832 aligned
  genes). This carries the headline RICTOR reversal **+0.161**.
- **Conservative all-cell null substrate** — the genome-scale all-cell
  effect-vector projection (7,393-gene intersection), used **only** to calibrate
  against the matched-perturbation null in the same space; here RICTOR reversal
  is **+0.131**.

The +0.030 gap between them decomposes into −0.036 (gene-universe change) and
+0.066 (responder → all-cell representation); the all-cell number is the
**conservative** one. Comparisons against the matched null are always made
within the all-cell substrate. See
[`confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv) and
[Methods](METHODS.md).

---

## What this decision trail does and does not establish

- It **does** establish an auditable path from 924 scored perturbations to three
  labelled outcomes, with every "not advanced", "rejected" and "retained"
  decision tied to a frozen artifact and a controlled reason code.
- It **does not** establish RICTOR as a validated drug target: systemic RICTOR
  inhibition is not shown safe, no selective RICTOR modality currently exists,
  and synovium-vs-blood is not disease-vs-healthy.
- It **does not** claim PAK2 as an anti-inflammatory target, and it does not
  claim that all 924 perturbations underwent deep validation.
- Nominal matched-null significance is **not** definitive.

The central message is that PerturbGate succeeded by keeping the record of failure
explicit: a real perturbation effect was treated as necessary but not sufficient,
and the strongest surviving claim (RICTOR) is retained as a bounded mechanism
hypothesis with a stated modality gap rather than promoted to a target
nomination.

---

## Source artifacts

| Artifact | Role in the decision trail |
|----------|----------------------------|
| [`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv) | Stage-level attrition, denominators, scope and disposition counts (S0–C0) |
| [`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv) | Per-perturbation disposition, last gate reached, reason and final evidence class |
| [`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv) | S0 screen-level reversal scores for the full 924 |
| [`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv) | Deep-candidate effect sizes, uncertainty and final public labels |
| [`analysis_contract.json`](../results/frozen/analysis_contract.json) | Pre-specified hypothesis, RICTOR 8 criteria, matched-null design, confirmatory-vs-exploratory split |
| [`matched_null.tsv`](../results/frozen/matched_null.tsv) / [`rictor_matched_null_values.tsv`](../results/frozen/rictor_matched_null_values.tsv) | RICTOR matched-perturbation null (criterion 8) |
| [`rictor_guides.tsv`](../results/frozen/rictor_guides.tsv), [`rictor_lodo.tsv`](../results/frozen/rictor_lodo.tsv), [`rictor_conditions.tsv`](../results/frozen/rictor_conditions.tsv) | RICTOR guide / leave-one-donor-out / condition robustness |
| [`superseded_claims.json`](../results/frozen/superseded_claims.json) | Retired framings (SUP-01…SUP-05); see [Superseded results](SUPERSEDED_RESULTS.md) |

Figures: [`figure_1_target_attrition`](../figures/figure_1_target_attrition.svg),
[`figure_2_directionality_and_null`](../figures/figure_2_directionality_and_null.svg),
[`figure_3_gate_matrix`](../figures/figure_3_gate_matrix.svg),
[`figure_4_pak2_rejection`](../figures/figure_4_pak2_rejection.svg),
[`supplementary_rictor_robustness`](../figures/supplementary_rictor_robustness.svg),
[`supplementary_gate_ablation`](../figures/supplementary_gate_ablation.svg).

See also: [Methods](METHODS.md) · [Superseded results](SUPERSEDED_RESULTS.md) ·
[Reproducibility](REPRODUCIBILITY.md).
