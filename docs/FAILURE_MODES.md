# Failure modes

This document records the analytical failure modes that the PerturbGate audit layer
**detected and corrected** during target nomination. It is written as a record of
falsification tests that fired — not as a debugging log — because each of these failure
modes, left uncorrected, would have converted a real cellular perturbation effect into an
overclaimed drug-target nomination.

> The audit layer detected analytical failure modes that could otherwise have produced an
> overclaimed target nomination.

The central premise of the project is that **a real perturbation effect is necessary but
not sufficient** for target nomination. Every failure mode below is a specific way in which
a genuine, reproducible effect can be *misread* as therapeutic support. PerturbGate's result
is a target-**nomination** decision, not a gene ranking, precisely because these ten checks
sit between "measurable effect" and "retained hypothesis."

For the pipeline decisions these checks feed, see [Methods](METHODS.md), the
[superseded-result ledger](SUPERSEDED_RESULTS.md), and the frozen artifacts under
[`results/frozen/`](../results/frozen/). Where a correction retired an earlier internal claim,
the superseded item ID (SUP-0x) is cited.

---

## Summary table

| # | Failure mode | What it would have produced | Where it was caught | Frozen evidence |
|---|--------------|-----------------------------|---------------------|-----------------|
| 1 | Unsigned enrichment read as disease reversal | False "disease-relevant" flag for PAK2 | Signed-direction / divergence test | SUP-02; `primary_comparison.tsv` |
| 2 | Biological residency removed as a nuisance | Inflated RICTOR reversal (~+0.43) | Confound decomposition | SUP-01; `confound_decomposition.tsv` |
| 3 | Gene-ID namespace mismatch | Phantom "safer neighbour" escape target | Namespace-corrected neighbour search | SUP-04; `rejection_ledger.tsv` |
| 4 | Incomplete essentiality / safety vetoes | Undervetted candidates advanced | Full external veto stack | `rejection_ledger.tsv`; `gate_matrix.tsv` |
| 5 | Broad transcriptional effect mimicking reversal | Non-specific hubs nominated | Biological-robustness stage (S1) | `candidate_funnel.tsv`; `rejection_ledger.tsv` |
| 6 | Guide concordance read as partial-inhibition evidence | Unsupported "partial PAK2 inhibition" claim | Titration-axis check | SUP-03; `rejection_ledger.tsv` |
| 7 | All-cell representation diluting responder effects | Understated (or mismatched) effect size | Two-substrate reconciliation | `primary_comparison.tsv`; `confound_decomposition.tsv` |
| 8 | Repeated Monte Carlo draws read as independent controls | Overstated null precision | Finite-pool vs resampling CI separation | `matched_null.tsv`; `rictor_matched_null_values.tsv` |
| 9 | Screen-wide ranking read as deep validation | PAK2 nominated on rank alone | Branching funnel, not linear funnel | `candidate_funnel.tsv` |
| 10 | Same-cohort sensitivity read as independent replication | Overstated RICTOR replication | Cohort-scope labelling | `rictor_lodo.tsv`; `primary_comparison.tsv` |

---

## 1. Unsigned enrichment mistaken for disease reversal

**The failure mode.** A gene programme can be strongly enriched in diseased tissue without
being *directionally* therapeutic. Raw enrichment tests are magnitude tests: they detect that
a module is elevated, not whether knocking down the target moves disease-up genes *down* and
disease-down genes *up*. Reading enrichment as reversal conflates "the target's programme is
active in disease" with "the target reverses disease."

**Detection.** The audit layer required *signed* directionality: disease-up and disease-down
modules must **diverge** under the perturbation, not co-move. For PAK2, the external JIA
synovial enrichment showed the `FROZEN_UP` and `FROZEN_DOWN` modules **co-elevating**
(`diverge = False`) — a generic activation signature, not a reversal signature. The signed
disease-reversal score for PAK2 was **+0.010 (centered-Pearson, p = 0.297, not significant)**,
against RICTOR's signed **+0.161 (p = 1.8e-63)**.

**Correction.** PAK2's external enrichment was reclassified `disease_relevant = False`
(SUP-02). Enrichment was retained only as a magnitude observation and never counted as
disease support. By contrast, RICTOR's reversal is a signed leading-edge effect: it turns
**down** the disease-up genes CXCL13, CXCR6, CCL4, IFNG, GZMB, PDCD1, RGS1 (0 reinforced).

---

## 2. Biological residency removed as a nuisance

**The failure mode.** In JIA, T cells that reside in the inflamed synovium carry a genuine
tissue-residency programme; that programme *is* part of the disease biology. Regressing
residency out as a "batch/nuisance" covariate — and restricting to a small covariate-adjusted
gene subset — removes real disease signal and can inflate an apparent reversal.

**Detection.** The earlier internal RICTOR result of **~+0.43** came from an old
covariate-adjusted, residency-removed **77-gene** subset combined with a responder-only
knockdown representation (SUP-01). The confound decomposition then showed *why* that number was
not trustworthy: removing the 780 strongly-knockdown-down genes dropped the reversal from
**+0.161 to +0.093** — but those 780 genes *include* the pathogenic disease-up genes CXCR6,
CCL4, and IFNG. Removing them removes **real signal, not confound**
([`confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv), row
`broad_downregulation`, delta -0.068).

**Correction.** The disease vector is defined on the **full transcriptome (12,071 genes)** with
**residency NOT regressed**, per-donor log2((CPM_syn+1)/(CPM_blood+1)) meta-analysed across 11
paired donors. The **~+0.43** figure is retired and appears only in an explicitly superseded
context; the authoritative values are **+0.161** (primary responder-resolved) and **+0.131**
(conservative all-cell null substrate). By construction, removing cell-cycle, activation,
stress, apoptosis, and T-identity genes leaves the reversal essentially unchanged
(deltas |Δ| ≤ 0.0012), confirming it is *not* a generic confound.

---

## 3. Gene-ID namespace mismatch

**The failure mode.** A search for a "safer druggable neighbour" of PAK2 (a target with a real
programme but a difficult modality) compared effect vectors across gene sets identified in
**different ID namespaces** (e.g. symbol vs Ensembl). A namespace mismatch silently drops or
mismaps genes, and can manufacture apparent neighbours that are artefacts of the join, not of
biology.

**Detection.** The original global-cosine neighbour search (returning candidates such as PTEN)
was flagged as resting on a **gene-ID namespace mismatch** (SUP-04). When the search was
repeated with namespaces reconciled, the apparent neighbours did not survive.

**Correction.** The namespace-corrected search found **no** safer, druggable, immune-directional
escape target. This is recorded as a negative result rather than deleted, and the "safer PAK2
neighbour" claim is superseded.

---

## 4. Incomplete essentiality / safety vetoes

**The failure mode.** A candidate can look attractive simply because it was never run through
the full external veto stack (essentiality, safety liabilities, tractability, credible
modality). Partial vetting lets undervetted candidates advance as if they had passed.

**Detection.** The neighbour-escape search combined the namespace bug above with **incomplete
essentiality/safety vetoes** (SUP-04). Re-running the complete veto stack changed the outcome:
across the ten neighbour candidates evaluated for PAK2, **0/10 passed the veto stack**. At the
screen level, the same external layer (stage S2) took the biologically robust shortlist of
**21** perturbations to **0 advanceable** — every one was safety-, essentiality-, or
modality-constrained
([`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv), stage S2).

**Correction.** Vetoes are applied as a complete stack and recorded per candidate in the
[rejection ledger](../results/frozen/rejection_ledger.tsv). Examples of the veto reasons:
broad/essential hubs (GNAS, STAT3, SMARCB1, TET2) flagged `SAFETY_CONSTRAINED`; immune-directional
but undruggable transcription factors (KLF13, IRF9, ELF4) flagged `NO_CREDIBLE_MODALITY`.

---

## 5. Broad transcriptional effects mimicking reversal

**The failure mode.** A perturbation that shifts *thousands* of genes will, by chance and by
sheer breadth, partially anti-correlate with almost any disease vector. Broad, non-specific
transcriptional effects can therefore mimic a targeted reversal, especially if the effect is
donor-unstable.

**Detection.** The biological-robustness stage (S1) tested donor-consistent subvectors,
bootstrap, and leading-edge jackknife. Of **208** convergent, FDR<0.10 screen hits, only **21**
survived; **187** were not advanced as **broad transcriptional / donor-unstable**
([`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv), stage S1). Perturbations that
reversed only through breadth were labelled `NONSPECIFIC_BROAD_REVERSER` (e.g. BRD1, SIN3A in the
[rejection ledger](../results/frozen/rejection_ledger.tsv)).

**Correction.** RICTOR was required to survive the confound-resistance test rather than rely on
breadth: removing cell-cycle, activation, stress, apoptosis, and T-identity gene sets left the
reversal at ~+0.16 (see failure mode 2), and its leading edge is a specific, coherent set of
pathogenic disease-up genes turned down (0 reinforced) — not a diffuse smear.

---

## 6. Guide concordance mistaken for partial-inhibition evidence

**The failure mode.** Two CRISPRi guides that agree with each other demonstrate a *reproducible*
on-target effect. They do **not** establish that *partial* target inhibition (the achievable
small-molecule regime) is sufficient — that requires a **strong-vs-weak titration axis**.
Reading high guide concordance as a dose-response argument is a category error.

**Detection.** For PAK2, both guides produced **similarly strong knockdown (~83-86% on-target)**
with **guide concordance 0.85 (100% direction agreement)**. That is excellent reproducibility,
but it means there is **no strong-vs-weak axis** to test partial inhibition (SUP-03). The claim
that "partial PAK2 inhibition is supported" was therefore not established by the data that
appeared to support it.

**Correction.** Partial-inhibition sufficiency for PAK2 is recorded as **NOT_ESTABLISHED**
([`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv)). Guide concordance is reported
only as technical reproducibility. Note the honest asymmetry: PAK2 **passed** technical
validation (on-target KD both guides ~83-86%; 112-gene frozen responder programme robust across
donor/guide/LODO; Mixscape responder fraction 76.5%; `specific_non_toxic`) and was still
**rejected** on therapeutic grounds — the defining illustration that a real effect is not
sufficient.

---

## 7. All-cell representation diluting responder-resolved effects

**The failure mode.** Averaging a knockdown effect over *all* cells — including the majority that
mount little response — dilutes a real effect that is concentrated in the responder
subpopulation. Conversely, silently *mixing* responder-resolved scores with all-cell scores
compares numbers computed in different spaces and produces a meaningless composite.

**Detection.** The two substrates were reconciled explicitly rather than blended. The **primary
responder-resolved** donor-random-effects meta knockdown vector gives reversal **+0.161**
(10,832 aligned genes); the **conservative all-cell effect-vector projection** gives **+0.131**
(7,393-gene intersection) and is used **only** to calibrate against the matched null in the same
space. The **+0.030** gap decomposes into **-0.036** (gene-universe difference) **+0.066**
(responder→all-cell representation) — i.e. the all-cell substrate is the *conservative* number,
and responder resolution recovers real signal (Mixscape responder fraction 76.5%).

**Correction.** Responder-resolved and all-cell scores are **never silently mixed**. The all-cell
number is quoted whenever a claim must sit in the null substrate's space; the responder-resolved
number is quoted as the primary effect size. Both are carried side by side in
[`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv).

---

## 8. Repeated Monte Carlo draws mistaken for independent controls

**The failure mode.** The matched-perturbation null is a **finite pool** of 200 covariate-matched
perturbations (k=200 nearest neighbours on magnitude, breadth, donor-sign consistency,
guide-sign concordance, and on-target LFC). Bootstrapping or reseeding that pool produces new
*draws*, but not new *controls*. Treating Monte Carlo resamples as if they were additional
independent controls understates the true finite-pool uncertainty.

**Detection.** The null was reported with **both** kinds of interval kept distinct. Against the
conservative all-cell substrate, RICTOR's reversal **+0.131** sits at percentile **96.5**
(global 97.9); **7 of 200** matched perturbations exceed it; empirical **p = 0.0398**. The
finite-pool **Wilson 95% CI is (0.017, 0.070)** and the **Monte Carlo bootstrap 95% CI is
(0.015, 0.065)**; the seed-stable p range is **[0.032, 0.042]**, pooled p 0.034. The Wilson
interval reaching ~0.070 is the honest finite-pool statement; the MC interval does not narrow it
by adding pseudo-controls
([`matched_null.tsv`](../results/frozen/matched_null.tsv),
[`rictor_matched_null_values.tsv`](../results/frozen/rictor_matched_null_values.tsv)).

**Correction.** This is why **criterion 8 is stated as the weakest/most marginal** of the
pre-specified checks and why the summary wording is deliberately bounded:

> RICTOR satisfied seven strong convergence checks and nominally exceeded a
> matched-perturbation null, with borderline finite-pool uncertainty.

We do **not** write "8/8 decisive criteria." The eight pre-specified criteria (fixed before
viewing the raw-count result) are: (1) centered-Pearson reversal > 0; (2) Spearman reversal > 0;
(3) ranked-GSEA reversal same direction; (4) both RICTOR guides positive (+0.141, +0.178);
(5) all 11 disease-donor leave-one-out folds positive (band +0.154..+0.167); (6) responder-only
support (93% of strata positive, all donors positive); (7) positive in all three conditions
(Rest +0.153, Stim8hr +0.092, Stim48hr +0.042); (8) above the matched null at the frozen point
estimate — the marginal one.

---

## 9. Screen-wide ranking mistaken for deep validation

**The failure mode.** A high rank in a genome-scale screen is a *hypothesis-generating* signal,
not a validated nomination. Presenting the screen as a single linear funnel in which the
top-ranked gene is "the winner" implies that every scored perturbation underwent every deep test —
which is false and inflates confidence in whatever sits on top.

**Detection.** The attrition is a **branching decision map, not a linear funnel**
([`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv)). At the screen level, **924**
perturbations were scored; **208** were convergent and FDR<0.10; **21** were biologically robust;
**0** were advanceable from the single-state screen (→ `NO_ROBUST_CANDIDATE`). The deep-candidate
branch is separate: PAK2 was **deep-validated and then REJECTED**, RICTOR was retained via a
**bounded pre-specified rescue**, and RIPK1 is a **comparator only**. PAK2's screen-level standing
did not, on its own, carry it through.

**Correction.** We explicitly do **not** claim that all 924 perturbations underwent deep
validation. Denominators trace to
[`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv),
[`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv), and
[`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv).
The controlled public labels are decisions, not ranks:
`DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` (RICTOR),
`REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` (PAK2),
`COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` (RIPK1).

---

## 10. Same-cohort sensitivity mistaken for independent replication

**The failure mode.** Re-analysing the *same* donors with an alternative processing choice
(e.g. a covariate-adjusted vector) is a **sensitivity analysis**. It tests robustness to
analytical choices; it does **not** constitute independent biological replication in a new
cohort. Labelling a same-cohort re-analysis as "replication" overstates external validity.

**Detection.** RICTOR's robustness evidence is explicitly scoped to one cohort. The **11/11
disease-donor leave-one-out folds** (band +0.154..+0.167) are leave-one-out *within* the same 11
paired JIA donors, and the Perturb-seq side rests on **4 donors** (6 leave-two-out pairs). The
adjusted-vector sensitivity is drawn from the same cohort as the primary vector.

**Correction.** The adjusted-vector sensitivity is **not** presented as independent biological
replication; "no independent replication" is carried as a principal limitation in
[`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv). Relatedly, we note that
synovium-vs-blood is **not** disease-vs-healthy. RICTOR is therefore retained as a mechanism
hypothesis with an unresolved modality gap (mTORC2 core scaffold; no selective small-molecule
modality), **not** as a validated drug target.

---

## What these corrections do and do not license

PerturbGate succeeded not because it found a positive hit, but because every retained claim
survived an explicit record of how competing claims failed. The corrections above **do**
support retaining RICTOR as a disease-reversing mechanism node and rejecting PAK2 as
therapeutically directional despite PAK2 being a real, reproducible cellular hit. They **do
not** license the following, which the project explicitly does not claim: that RICTOR is a
validated drug target; that systemic RICTOR inhibition is safe (a mild, donor-inconsistent early
apoptosis flag, +0.030, ≤33% strata consistent, is on record); that a selective RICTOR modality
exists; that synovium-vs-blood equals disease-vs-healthy; that the same-cohort sensitivity is
independent replication; that PAK2 is an anti-inflammatory target; or that nominal matched-null
significance is definitive.

See also: [Methods](METHODS.md) · [Superseded results](SUPERSEDED_RESULTS.md) ·
frozen artifacts in [`results/frozen/`](../results/frozen/).
