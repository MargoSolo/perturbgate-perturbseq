# Figure legends

Detailed legends for every figure in the PerturbGate v1.0.0 frozen hackathon release
(PerturbGate — Evidence-Gated Pipeline for T-cell Perturb-seq Mechanism Hypotheses).
Each legend states what is shown, the exact denominators, the effect sizes and their
uncertainty, the source-data table under `figures/source_data/`, and any caveats where a
panel is descriptive rather than independently validated.

These legends should be read alongside [Methods](METHODS.md), [Results](RESULTS.md),
[Claims and evidence](CLAIMS_AND_EVIDENCE.md), [Limitations](LIMITATIONS.md),
[Superseded results](SUPERSEDED_RESULTS.md) and the [Decision trail](DECISION_TRAIL.md).

Central message conveyed by the figure set: a real perturbation effect is **necessary but
not sufficient** for target nomination. The figures are framed as target *nomination*, not
gene *ranking*.

---

## Display conventions (apply to every figure)

- **Colour-blind-safe palette.** All figures use a colour-blind-safe qualitative palette.
  Colour is never the sole carrier of meaning.
- **Symbols, not colour alone.** Categorical status is always encoded redundantly with a
  glyph in addition to colour/position. The gate glyphs used across Figures 3 and 4 and
  the supplementary ablation are:
  - `✓` PASS
  - `✗` FAIL
  - `~` BORDERLINE
  - `△` TRANSLATIONAL_GAP / MODALITY_GAP (credible-modality column)
  - `?` NOT_ESTABLISHED
  - `–` NOT_EVALUATED (gate not applicable / not run for that row)
- **Effect size + denominator + uncertainty, not p-values alone.** Where a p-value appears
  as a panel annotation it is always paired with the effect size, the number of aligned
  genes or controls, and (where applicable) an interval. p-values are never presented in
  isolation.
- **Denominators are auditable.** Every count traces to a frozen table under
  `results/frozen/` — principally `candidate_funnel.tsv`, `rejection_ledger.tsv`,
  `all_perturbations_authoritative_reversal.tsv`, `primary_comparison.tsv` and
  `matched_null.tsv`.
- **Two substrates are never silently mixed.** The primary responder-resolved donor-RE
  meta knockdown (KD) vector (RICTOR reversal **+0.161**, 10,832 aligned genes) and the
  conservative all-cell effect-vector projection (RICTOR reversal **+0.131**, 7,393-gene
  intersection, used only to calibrate against the matched-perturbation null in the same
  space) are labelled explicitly wherever both appear.
- **Reversal metric.** `reversal = −centered_Pearson(KD_log2FC, disease_log2FC)`; a
  positive value means the perturbation moves the transcriptome opposite to the JIA
  synovium-vs-blood disease direction. The disease vector is the JIA
  synovium(tissue+fluid)-vs-blood activated-memory CD4 raw-count donor-paired pseudobulk
  (11 paired donors, full transcriptome 12,071 genes; see [Methods](METHODS.md)).

---

## Figure 1 — `figure_1_target_attrition`

**Title on figure:** *Target attrition through evidence gates — from 924 perturbations to a
small set of evidence-gated mechanism hypotheses.*

**What is shown.** A branching decision map (not a linear funnel) tracing how perturbations
move from a genome-scale screen into a small set of evidence-gated mechanism hypotheses.
The left/upper spine is the screen-wide attrition; the lower branches are the three
candidate-specific deep evaluations (PAK2, RICTOR, RIPK1). The footer states the central
message: "Ranking is not validation: a real perturbation effect is necessary but not
sufficient for target nomination."

**Exact denominators (screen-wide spine).**
- **S0 — Screen-level reversal scoring:** denominator = all perturbations with a usable
  genome-scale effect vector = **924**; **208** convergent (Pearson & Spearman & GSEA) with
  FDR < 0.10 advanced; **716** not advanced.
- **S1 — Biological robustness** (donor-consistent subvector + bootstrap + jackknife):
  denominator = the **208** convergent/FDR<0.10 screen hits; **21** biologically robust;
  **187** broad/donor-unstable not advanced.
- **S2 — Safety / essentiality / tractability / modality:** denominator = the **21**
  robust shortlist; **0** advanceable from the single-state screen; **21**
  safety/modality-constrained → outcome **NO_ROBUST_CANDIDATE**.

**Exact denominators (candidate-specific branches, each n = 1 perturbation).**
- **D0 — PAK2 (lead):** technical validation PASS, therapeutic direction FAIL → **REJECTED**
  (reproducible cellular hit, not therapeutically directional).
- **R0 — RICTOR (bounded rescue):** seven strong criteria PASS plus a borderline
  matched-null → **RETAINED** mechanism node with modality gap (+0.161; 11/11 disease-donor
  LODO folds positive).
- **C0 — RIPK1 (comparator):** weak/incoherent reversal → **COMPARATOR ONLY**, not
  directionally supported in this analysis.

**Effect sizes / uncertainty.** RICTOR annotation +0.161 and 11/11 LODO are carried on the
branch; full effect sizes and intervals are in Figures 2 and the supplementary panels.

**Caveat.** This is a branching decision map: **not all 924 perturbations underwent every
deep test.** Only the shortlist and the three named candidates were deeply evaluated. Do
not read S0→D0/R0/C0 as a single sequential pipeline.

**Source data:** `figures/source_data/figure_1_target_attrition.tsv`
(mirrors `results/frozen/candidate_funnel.tsv`; reasons in
`results/frozen/rejection_ledger.tsv`).

---

## Figure 2 — `figure_2_directionality_and_null` (panels A–D)

**Title/footer on figure:** *RICTOR disease-state reversal: effect size, denominator and
uncertainty (not a p-value alone).*

**Source data (all panels):** `figures/source_data/figure_2_directionality_and_null.tsv`
(panel-level supporting values in `results/frozen/primary_comparison.tsv`,
`rictor_guides.tsv`, `rictor_conditions.tsv`, `rictor_lodo.tsv`, `matched_null.tsv`,
`rictor_matched_null_values.tsv` and `leading_edge.tsv`).

### Panel A — Primary responder-resolved reversal

**What is shown.** Point estimates of disease-state reversal for the three named
perturbations in the **primary responder-resolved donor-RE meta KD substrate**, on the
x-axis `reversal = −centered Pearson(KD, disease)`.

**Effect sizes, denominators, uncertainty.** (The Pearson p-values below are
**descriptive gene-wise correlation p-values, not donor-level inference** — genes are
correlated, not independent replicates; donor-level uncertainty comes from the
leave-one-donor-out and matched-null analyses, not from these p-values.)
- **RICTOR +0.161** (centered-Pearson; Spearman +0.100; descriptive gene-wise p = 1.8e-63),
  on **10,832 aligned genes**, r² ≈ 2.6%.
- **PAK2 +0.010** (not directional; descriptive gene-wise p = 0.297), same responder-resolved metric.
- **RIPK1 +0.038** (weak/incoherent; descriptive gene-wise p = 8.7e-05), same responder-resolved metric.

The panel demonstrates that only RICTOR carries a meaningful positive reversal; PAK2 is
effectively null and RIPK1 is weak. p-values appear as annotations but are always paired
with the effect size and the aligned-gene denominator.

### Panel B — Matched-perturbation null (conservative substrate)

**What is shown.** The RICTOR reversal placed against a **matched-perturbation null** built
from **200** covariate-matched control perturbations (k = 200 nearest neighbours on
z-scored magnitude, breadth, donor-sign-consistency, guide-sign-concordance and
on-target LFC; seed 0). x-axis is the **conservative all-cell effect-vector reversal**.

**Effect sizes, denominators, uncertainty.**
- RICTOR observed reversal in this conservative substrate = **+0.131** (7,393-gene
  intersection).
- **7 / 200** matched perturbations exceed RICTOR.
- Matched percentile **96.5** (global percentile **97.9**).
- Empirical **p = 0.0398** (annotated as p = 0.040).
- **Wilson 95% CI 0.017–0.070**; Monte-Carlo bootstrap 95% CI 0.015–0.065; seed-stable p
  range [0.032, 0.042]; pooled p 0.034.

**Substrate note (important).** Panel B deliberately uses the **conservative all-cell
substrate (+0.131)**, not the responder-resolved +0.161 of Panel A, because the matched
null is defined in the all-cell space and the two substrates must be compared in the same
space. The +0.030 gap between substrates decomposes as −0.036 (gene-universe change) +
0.066 (responder→all-cell representation); the all-cell number is the conservative one.

**Caveat.** This is the **weakest/most marginal** of the RICTOR criteria. The nominal
matched-null significance is **not definitive**: with only 7/200 exceeding and a Wilson CI
reaching ~0.070, the result is best described as *nominally exceeding a
matched-perturbation null, with borderline finite-pool uncertainty*.

### Panel C — RICTOR guide / condition / donor robustness

**What is shown.** RICTOR reversal broken out across the two guides, the three activation
conditions, and the disease-donor leave-one-donor-out (LODO) folds, all in the primary
responder-resolved substrate (10,832 aligned genes).

**Effect sizes, denominators, uncertainty.**
- **RICTOR-1 +0.141** (Pearson p = 3.4e-49) and **RICTOR-2 +0.178** (p = 7.1e-78) —
  both guides positive (10,832 aligned genes each).
- Conditions: **Rest +0.153** (p = 6.7e-58), **Stim8hr +0.092** (p = 1.3e-21),
  **Stim48hr +0.042** (p = 1.1e-05) — positive in all three conditions.
- **Disease-donor LODO: 11 / 11 folds positive**, band **[0.154, 0.167]** (all-fold mean
  +0.159), across the 11 paired disease donors.

The panel shows the reversal is not driven by a single guide, a single condition, or a
single disease donor.

### Panel D — Leading edge: disease-UP genes RICTOR turns DOWN

**What is shown.** The per-gene RICTOR KD log2FC for individual disease-UP genes, ordered by
how strongly RICTOR knockdown pushes them down. Leading-edge pathogenic disease-UP genes
that RICTOR turns down include **CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, RGS1** (and
further chemokine/effector genes such as ITGA1, CCR2, XCL2, CCR5); **0** are reinforced.

**Effect sizes / denominators.** Values are RICTOR KD log2FC against disease log2FC from
`results/frozen/leading_edge.tsv` (e.g. CCL4 disease +3.08 / KD −2.11; CXCR6 disease +3.36
/ KD −1.50; IFNG disease +2.69 / KD −1.27; GZMB disease +3.12 / KD −0.53; PDCD1 disease
+2.43 / KD −0.54).

**Caveat (descriptive, not independently validated).** The panel axis is explicitly
labelled *"RICTOR KD log2FC (descriptive, not independently validated)."* This leading-edge
panel is an interpretive/mechanistic illustration of which pathogenic genes move; it is
**not** an independent statistical validation of the reversal and is not a
disease-vs-healthy contrast (the disease vector is synovium-vs-blood).

---

## Figure 3 — `figure_3_gate_matrix`

**Title on figure:** *Gate matrix — three axes: RICTOR is RETAIN biologically, external
same-disease concordance PASS, but STOP translationally (symbols + text, not colour alone).*

**What is shown.** A three-axis evidence-gate matrix. **Rows** are the three named candidates
plus two aggregate row-classes. **Columns** are grouped into four blocks separated by heavy
dividers: **Biological evidence** (8 gates), **External** (1 gate: external same-disease
concordance, GSE160097), **Translational readiness** (4 gates), and **Decision** (biological +
translational). Each cell carries a redundant glyph or short text so status is legible without
colour.

**Rows.** RICTOR, PAK2, RIPK1, *broad / essential hubs (aggregate)* (e.g. GNAS, STAT3,
SMARCB1, TET2), *immune-directional TFs, no modality (aggregate)* (e.g. KLF13, IRF9, ELF4).

**Biological-evidence gates.** measurable cellular effect · responder support · guide
concordance · perturbation-donor robustness · disease directionality · disease-donor LODO ·
matched-null support · confound resistance.

**External gate.** external same-disease concordance (GSE160097): **RICTOR PASS (`✓`)**;
PAK2 and RIPK1 **NOT_ESTABLISHED (`?`)** (near-zero external reversal); aggregates **NOT_EVALUATED
(`–`)**. This is external same-disease, paired-compartment *concordance* — not causal/perturbation
or therapeutic validation — and does **not** move the translational decision.

**Translational-readiness gates.** systemic safety · human-genetic efficacy · loss
constraint · selective modality.

**Decision columns.** biological decision · translational decision.

**Key cell statuses (verbatim from `results/frozen/gate_matrix.tsv`).**
- **RICTOR (the two-axis case):** biological gates all PASS (`✓`) except matched-null support
  **BORDERLINE (`~`)**. Translational gates: systemic safety **CELL_TYPE_CONFLICT (`⇄`)**,
  human-genetic efficacy **NO_SUPPORT (`∅`)**, loss constraint **SAFETY_HEADWIND (`▲`)**,
  selective modality **NONE_VALIDATED (`⊘`)**. Decisions: biological **RETAIN**,
  translational **STOP**.
- **PAK2:** PASS on technical/biological gates but **FAIL (`✗`)** on disease directionality,
  matched-null support and confound resistance → biological decision **REJECT**
  (translational not evaluated).
- **RIPK1:** biological decision **COMPARATOR**; passes human-genetic efficacy and selective
  modality (clinical-stage kinase inhibitors) but **FAIL** on directionality and systemic
  safety (LoF immunodeficiency).

**New glyphs.** `∅` no support · `▲` safety headwind · `⊘` none validated · `⇄` cell-type
conflict (in addition to `✓` pass, `✗` fail, `~` borderline, `?` not established, `–` not
evaluated, `△` translational gap).

**Interpretation.** The three axes are independent: RICTOR can be **RETAIN** on biological
evidence and **PASS** external same-disease concordance yet **STOP** on translational readiness
simultaneously. `–` means a gate was **not evaluated** for that row (the translational block is
evaluated only for the deep RICTOR audit), not that it was failed. RICTOR passing the biological
and external gates is **not** a validated-drug-target claim.

**Source data:** `figures/source_data/figure_3_gate_matrix.tsv`
(mirrors `results/frozen/gate_matrix.tsv`). Translational cells are sourced from the
completed audit in [../results/translational/](../results/translational/).

---

## Figure 4 — `figure_4_pak2_rejection`

**Title/footer on figure:** *PAK2 — a real perturbation hit is not sufficient for target
nomination; PAK2 passed technical validation but failed therapeutic validation →
REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL.*

**What is shown.** A two-block decision panel for the PAK2 deep candidate branch: a
**Technical validation — PASSED** block (5 rows, all `✓`) above a **Therapeutic validation —
FAILED** block (5 rows, `✗`/`?`). This figure is the concrete illustration of the central
message.

**Technical validation — PASSED (denominators/effect sizes).**
- On-target knockdown: **both guides ~83–86% KD** — PASS.
- Guide reproducibility: **concordance 0.85, 100% direction** — PASS.
- Donor reproducibility: **112-gene frozen responder programme, donor + LODO robust** —
  PASS.
- Real responder population: **Mixscape responder fraction 76.5%** — PASS.
- Reproducible programme: **frozen 112-gene responder signature** — PASS.
  (PAK2 is also `specific_non_toxic`.)

**Therapeutic validation — FAILED (denominators/effect sizes/uncertainty).**
- Inflammatory direction restored: **NF-κB Δ = −0.011, p = 0.05, negligible effect**, no
  donor-direction consistency — FAIL.
- Disease-state reversal: **+0.010, p = 0.297 (n.s.); 41st percentile** of the matched null
  — FAIL.
- External JIA enrichment: **FROZEN_UP and FROZEN_DOWN modules co-elevate (diverge = False)**
  → generic activation confound, disease_relevant = False — FAIL.
- Partial-inhibition sufficiency: **both guides similarly strong KD → NOT_ESTABLISHED (`?`)**
  (no strong-vs-weak titration axis).
- Safer druggable escape: **0 / 10 pass the veto stack** — FAIL.

**Interpretation.** PAK2 is a genuine, reproducible cellular hit that fails every
therapeutic-directionality test, so it is **REJECTED** as a target nomination. Public label:
**REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL** (frozen internal label
`REPRODUCIBLE_PAK2_RESPONDER_SIGNATURE_WITHOUT_THERAPEUTIC_RELEVANCE`).

**Caveat.** PAK2 is **not** an anti-inflammatory target. Prior PAK2 claims — JIA joint
enrichment as disease support, partial-inhibition sufficiency, a safer PAK2 neighbour, and a
PAK2–WASF2 therapeutic axis — are superseded and must not be presented as current (see
[Superseded results](SUPERSEDED_RESULTS.md), SUP-02 through SUP-05).

**Source data:** `figures/source_data/figure_4_pak2_rejection.tsv`.

---

## Supplementary figure — `supplementary_rictor_robustness`

**Title/footer on figure:** *RICTOR reversal across representations and controls — positive
on every track; adjusted-vector is same-cohort sensitivity, not independent replication.*

**What is shown.** A single-axis summary of RICTOR reversal (`−centered Pearson`) computed
across twelve different representations and controls, demonstrating the reversal is positive
on every track.

**Effect sizes / denominators (per track).**
- Primary raw-count vector **+0.161** (responder-resolved, 10,832 aligned genes).
- Adjusted-vector sensitivity **+0.147**.
- RICTOR guide 1 **+0.141**; RICTOR guide 2 **+0.178**.
- Disease-donor LODO (11 folds) **+0.159** (band [0.154, 0.167]).
- Responder-only mean **+0.054**.
- Condition Rest **+0.153**; Stim8hr **+0.092**; Stim48hr **+0.042**.
- Confound-removed (cell-cycle + activation + broad-downregulation) **+0.097**.
- Matched-null substrate **+0.131** (conservative all-cell, 7,393-gene intersection).

**Uncertainty / confound context.** Removing cell-cycle, activation, stress, apoptosis and
T-identity modules leaves the reversal essentially unchanged (per-module Δ within ±0.0012;
`results/frozen/confound_decomposition.tsv`). Removing the 780 strongly-KD-down genes drops
the reversal to **+0.093** — but those genes **include** the pathogenic disease-UP genes
(CXCR6, CCL4, IFNG), so that step removes real signal, not a confound. The combined
cell-cycle + activation + broad-downregulation removal (817 genes) gives **+0.097**.

**Provenance (every track resolves to an artifact).** All 11 tracks are read from the frozen
table [`results/frozen/rictor_robustness_tracks.tsv`](../results/frozen/rictor_robustness_tracks.tsv),
which carries a `source_artifact` column for each value (built by
`scripts/build_robustness_tracks.py`; guarded by `tests/test_figure_source_provenance.py`,
which also asserts the figure source-data mirrors this table). Nine tracks derive from other
committed frozen tables (`primary_comparison.tsv`, `rictor_lodo.tsv`, `confound_decomposition.tsv`).
**Two tracks — adjusted-vector sensitivity (+0.147) and responder-only mean (+0.054) — are
server-scale (`make full` / Level 3) narrative anchors that are not recomputed at Level 1**;
they are labelled as such in `source_artifact`, so no figure value is hard-coded.

**Caveats.**
- The **adjusted-vector sensitivity (+0.147)** is a **same-cohort sensitivity analysis, not
  independent biological replication** (same donors, same cohort).
- The historical RICTOR reversal of **~+0.43** is **superseded** (old
  covariate-adjusted/residency-removed 77-gene subset, inflated by frozen-subset + KD
  representation) and is replaced by +0.161 (primary) / +0.131 (null substrate). It must
  never be presented as a current result (see [Superseded results](SUPERSEDED_RESULTS.md),
  SUP-01).

**Source data:** `figures/source_data/supplementary_rictor_robustness.tsv`.

---

## Supplementary figure — `supplementary_gate_ablation`

**Title/footer on figure:** *Process ablation — what would survive if one gate were removed
(frozen decisions only; no threshold changes; not a causal-importance claim).*

**What is shown.** A process-ablation table: for each evidence gate, what class of
false-positive would survive if that single gate were removed from the pipeline. It
motivates why each gate exists, using only frozen decisions.

**Rows (gate removed → what would wrongly survive).**
- **therapeutic directionality removed →** a real, reproducible cellular hit with no disease
  reversal survives; example **PAK2** (passes every technical gate; without the
  directionality gate it would read as advanceable; frozen evidence: PAK2 reversal +0.010,
  p = 0.297).
- **broad-effect & essentiality controls removed →** broad chromatin/RNA/essential-machinery
  reversers survive; examples **GNAS, STAT3, SMARCB1, TET2** (high reversal driven by
  nonspecific broad suppression; frozen class SAFETY_CONSTRAINED).
- **modality review removed →** immune-directional but undruggable transcription factors
  survive; examples **KLF13, IRF9, ELF4** (real immune-directional reversal + immune
  genetics, but no credible small-molecule modality; frozen verdict NO_CREDIBLE_MODALITY).
- **finite-null uncertainty reporting removed →** the RICTOR matched-null significance would
  be read as decisive; example **RICTOR** (point estimate p = 0.040 looks firm, but the
  Wilson/bootstrap CI on 7/200 grazes 0.05–0.07).
- **confound decomposition removed →** a reversal could be mistaken for generic
  activation/broad suppression; example **RICTOR** (without module removal a reversal could
  be dismissed as, or inflated by, nonspecific suppression; cell-cycle/activation removal
  Δ ≈ 0).

**Effect sizes / uncertainty.** The frozen evidence column points each ablation row to its
supporting artifact (`primary_comparison.tsv`, `rejection_ledger.tsv`, `matched_null.tsv` +
`rictor_matched_null_values.tsv`, `confound_decomposition.tsv`).

**Caveat.** This is an illustration of **frozen decisions only, with no threshold changes,
and is not a causal-importance claim** — it shows which failure mode each gate catches, not
a re-ranking or a quantitative attribution of gate importance.

**Source data:** `figures/source_data/supplementary_gate_ablation.tsv`
(mirrors `results/frozen/gate_ablation.tsv`).

---

## What these figures do not claim

- RICTOR is **not** a validated drug target; no selective RICTOR (mTORC2 core scaffold)
  modality currently exists — this is the "modality gap".
- Systemic RICTOR inhibition is **not** shown to be safe (a mild donor-inconsistent early-tox
  apoptosis flag is present; T/Treg identity is preserved).
- The matched-null significance is **nominal**, not definitive; RICTOR satisfied seven strong
  convergence checks and nominally exceeded a matched-perturbation null, with borderline
  finite-pool uncertainty.
- PAK2 is **not** an anti-inflammatory target.
- Synovium-vs-blood is **not** disease-vs-healthy; the adjusted-vector sensitivity is **not**
  independent replication; **not** all 924 perturbations underwent deep validation.

See [Limitations](LIMITATIONS.md) and [Claims and evidence](CLAIMS_AND_EVIDENCE.md) for the
full statement of scope.
