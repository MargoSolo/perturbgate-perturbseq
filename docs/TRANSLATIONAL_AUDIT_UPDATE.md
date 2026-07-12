# Translational audit update (final release)

This is a narrow, final-release reconciliation of the completed RICTOR
translational-readiness audit with the frozen computational result. **No frozen
computational value, threshold, classification, disease vector, or primary result
changed.** The disease-reversal analysis is **complete** — it is not pending and
not assumed.

## Two axes, stated explicitly

| Axis | Verdict | Meaning |
|---|---|---|
| **Biological evidence** | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` | Retained disease-reversing mechanism hypothesis (unchanged). |
| **Translational readiness** | `NOT_ADVANCEABLE_WITH_CURRENT_EVIDENCE_AND_MODALITIES` | **STOP** — not advanceable as a conventional drug target with current evidence and modalities. |

The biological classification is **not** replaced or erased by the translational
STOP. RICTOR remains a retained mechanism hypothesis on the computational axis; it
is simultaneously stopped on the translational axis. Both are true at once — that
is the point.

## What the completed audit adds

The disease-reversal result stands: **+0.161** responder-resolved reversal (matched
substrate +0.131), both guides positive, 11/11 disease-donor leave-one-out folds
positive, all three conditions positive, confound-resistant, matched percentile
96.5, finite matched-control pool (7/200 exceed RICTOR; empirical p ≈ 0.040;
uncertainty to ≈ 0.07). See [RESULTS.md](RESULTS.md) and
[results/frozen/primary_comparison.tsv](../results/frozen/primary_comparison.tsv).

The translational audit then asked a separate question — *is this advanceable?* —
and answered **no**, on four independent pillars (full detail + verified PMIDs/DOIs
in [results/translational/](../results/translational/) and the
[verdict](../results/translational/RICTOR_TRANSLATIONAL_VERDICT.md)):

1. **No validated selective modality.** No RICTOR-selective small molecule,
   degrader, glue, peptide, or clinical agent. The tool compound JR-AB2-011
   (PubChem CID 138319699; the precursor screening hit is the different CID 613034)
   acts **RICTOR-independently / off-target** — its effects persist in CRISPR
   RICTOR-null cells (PMID 39259491).
2. **No human-genetic efficacy support.** Open Targets shows no GWAS/colocalization
   linking RICTOR to RA, SLE, or JIA; the locus (5p13.1) is confounded by neighbour
   genes **OSMR** and **FYB1/ADAP**. RICTOR is loss-of-function-intolerant
   (gnomAD pLI ≈ 1.0; LOEUF 0.155/0.289) — a safety headwind.
3. **Constrained systemic safety.** Whole-body knockout is embryonic lethal;
   conditional knockouts show metabolic, cardiac, and developmental liabilities;
   and immune effects are **opposing across cell types** (RICTOR is required for
   effector Th1/Th2 yet destabilizes Foxp3/Treg).
4. **Foundational evidence retracted.** The JR-AB2-011 founding paper
   (retraction DOI `10.1371/journal.pone.0291490`) and the only RICTOR-ASO human
   autoimmune-disease paper (retraction DOI `10.1093/rheumatology/keaf391`) are
   **both retracted** — and are used here **only** as do-not-use entries.

## Combined statement

> RICTOR is internally supported as a disease-reversing mechanism hypothesis, but
> it is not currently advanceable as a conventional drug target because no
> validated selective modality exists, human genetics provides no efficacy support,
> and systemic safety is constrained by essentiality and opposing cell-type effects.

## Novelty boundary

We do not claim novelty for RICTOR/mTORC2 regulation of T-cell differentiation,
Tfh, Treg, or autoimmunity. The narrow claim is a **computational mechanism
hypothesis, not functional validation**: RICTOR-specific perturbation in primary
human CD4 T cells directionally reverses a donor-paired inflamed-joint
activated-memory transcriptional programme (tissue-retention and cytotoxic-effector
genes) without detectable collapse of the Treg-identity score in this dataset.

## How Claude Science contributed (and its limits)

Claude Science identified and verified two RICTOR-relevant retraction chains,
distinguished vendor-labelled compounds from validated target engagement, detected
neighbour-gene pQTL misattribution, and preserved a human-genetics efficacy null
rather than converting it into support. Every public statement here resolves to a
primary paper, an official database (PubMed / PubChem / gnomAD / Open Targets), or a
data artifact — not to AI output. Identifiers are checked by
`scripts/check_references.py`.

## Future validation (plan only — not causal validation)

The external datasets in
[EXTERNAL_DATASET_SHORTLIST.tsv](../results/translational/EXTERNAL_DATASET_SHORTLIST.tsv)
are observational and would provide **concordance** tests, not causal validation.
Preferred same-tissue comparator: AMP RA Phase 1 (RA-vs-OA); fastest orthogonal CD4
test: GSE118209. See also [TRANSLATIONAL_CONTEXT.md](TRANSLATIONAL_CONTEXT.md) and
[MANUSCRIPT_ROADMAP.md](MANUSCRIPT_ROADMAP.md).
