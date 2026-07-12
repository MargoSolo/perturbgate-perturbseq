# RICTOR — translational-readiness verdict

> **Two independent axes. This verdict adds the second; it does not replace the first.**
>
> - **Biological evidence:** `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`
>   — retained disease-reversing mechanism hypothesis (unchanged).
> - **Translational readiness:** `NOT_ADVANCEABLE_WITH_CURRENT_EVIDENCE_AND_MODALITIES`
>   — **STOP**.

The computational disease-reversal result is **complete and unchanged**: on the
corrected donor-paired raw-count activated-memory JIA synovium-vs-blood vector,
RICTOR knockdown reverses the inflamed-joint CD4 direction at **+0.161**
(responder-resolved; matched-null substrate **+0.131**), with both guides positive,
11/11 disease-donor leave-one-out folds positive, all three conditions positive,
confound-resistant, matched percentile 96.5, and a finite matched-control pool
(7/200 exceed RICTOR; empirical p ≈ 0.040; uncertainty extending to ≈ 0.07). None
of those frozen numbers change here. The disease-reversal analysis is finished — it
is not pending and it is not assumed; it is demonstrated at the values above.

This document records the **separate translational-readiness audit**, which reaches
a **STOP** verdict on four independent pillars.

## 1. No validated selective modality

No validated RICTOR-selective small molecule, degrader, molecular glue, peptide, or
clinical-stage agent exists ([RICTOR_MODALITY_TABLE.tsv](RICTOR_MODALITY_TABLE.tsv)).

- The tool compound **JR-AB2-011** (PubChem **CID 138319699**; note CID 613034 is
  the *precursor* screening hit "CID613034", a different molecule) has **no
  validated target engagement**: its cellular effects **persist in CRISPR
  RICTOR-null cells** and it does not reduce AKT-Ser473 phosphorylation
  (Kořánová et al., *Pharmacol Rep* 2024, PMID 39259491) — i.e. it acts
  mTORC2-independently / off-target.
- ATP-competitive mTOR kinase inhibitors block mTORC2 kinase activity but are
  **not RICTOR-selective** (they also inhibit mTORC1).

## 2. No human-genetic efficacy support; strong loss constraint

([RICTOR_HUMAN_GENETICS.tsv](RICTOR_HUMAN_GENETICS.tsv))

- Open Targets shows **no genome-wide-significant common-variant association and no
  colocalization** linking RICTOR to rheumatoid arthritis, SLE, or JIA — the only
  RA/SLE signal is literature text-mining (partly from now-retracted papers).
  There is therefore **no efficacy-direction support** that lowering RICTOR is
  protective.
- **pQTL/eQTL caution:** RICTOR sits at 5p13.1 flanked by **OSMR** (overlaps its 5′
  end) and **FYB1/ADAP** (a T-cell adaptor); any locus signal nominally assigned to
  RICTOR should be treated as possible neighbour-gene misattribution absent formal
  colocalization.
- RICTOR is **loss-of-function-intolerant** (gnomAD pLI ≈ 1.0; LOEUF 0.155 in
  v2.1.1 / 0.289 in v4) — a safety headwind for durable inhibition.

## 3. Systemic safety is constrained (essentiality + opposing cell-type effects)

([RICTOR_SAFETY_LANDSCAPE.tsv](RICTOR_SAFETY_LANDSCAPE.tsv))

- Whole-body *Rictor* knockout is **embryonic lethal** (PMID 16962829, 17141160).
- Conditional knockouts reveal broad liabilities: **metabolic** (hepatic
  hyperglycemia/hyperinsulinemia/hypolipidemia, PMID 22521878), **cardiac**
  (contractile failure under pressure overload, PMID 26598511), and **developmental
  /vascular** (PMID 26635098).
- **Opposing immune-cell effects:** RICTOR is *required* for effector Th1/Th2
  differentiation (PMID 20620941) yet its activity *destabilizes* Foxp3/Treg
  (PMID 26437242) — so systemic inhibition pushes different CD4 states in opposite,
  potentially counterproductive directions (a cell-type conflict).

## 4. Retraction register — foundational evidence withdrawn

([RICTOR_PRIOR_ART_TABLE.tsv](RICTOR_PRIOR_ART_TABLE.tsv)) — **not used as positive evidence.**

| Retracted primary paper | Retraction notice (DOI / PMID / date) |
|---|---|
| Benavides-Serrato et al., *PLoS One* 2017 — JR-AB2-011 "specific blockade of Rictor-mTOR" (PMID 28453552; DOI 10.1371/journal.pone.0176599) | **10.1371/journal.pone.0291490** · PMID 37682814 · 2023-09-08 (figure-integrity) |
| Ai et al., *Rheumatology (Oxford)* 2025 — RICTOR-ASO attenuates SLE (incl. human PBMCs) (PMID 39656824; DOI 10.1093/rheumatology/keae662) | **10.1093/rheumatology/keaf391** · PMID 40966663 · 2025-11-01 (data miscalculation; human-efficacy figure) |

The two papers that most directly support "RICTOR/mTORC2 is a druggable node in
autoimmune disease" — the JR-AB2-011 founding paper and the only RICTOR-ASO
human-autoimmune-disease paper — are **both retracted**. Independent work further
shows JR-AB2-011 acts RICTOR-independently. Combined with pillars 1–3, the case for
lowering RICTOR in RA/JIA/SLE partly rested on withdrawn literature.

## Combined verdict

> RICTOR is internally supported as a disease-reversing mechanism hypothesis, but
> it is not currently advanceable as a conventional drug target because no
> validated selective modality exists, human genetics provides no efficacy support,
> and systemic safety is constrained by essentiality and opposing cell-type effects.

## Novelty boundary

We do **not** claim novelty for RICTOR/mTORC2 regulation of T-cell differentiation,
Tfh, Treg, or autoimmunity. The narrow claim is: *RICTOR-specific perturbation in
primary human CD4 T cells directionally reverses a donor-paired inflamed-joint
activated-memory transcriptional programme involving tissue-retention and
cytotoxic-effector genes, without detectable collapse of the Treg-identity score in
this dataset.* This is a **computational mechanism hypothesis, not functional
validation.**

## Future validation (plan only, not causal validation)

See [EXTERNAL_DATASET_SHORTLIST.tsv](EXTERNAL_DATASET_SHORTLIST.tsv). These are
observational datasets for *concordance* testing, not causal validation. Preferred
comparator: AMP RA Phase 1 (same-tissue RA-vs-OA). Public reconciliation:
[docs/TRANSLATIONAL_AUDIT_UPDATE.md](../../docs/TRANSLATIONAL_AUDIT_UPDATE.md).
