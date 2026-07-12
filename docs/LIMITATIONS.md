# Limitations

PerturbGate is a hackathon-scale, single-cohort analysis. Its conclusions are
deliberately bounded. The principal limitations below are the reason RICTOR is
retained only as a *mechanism node*, not a validated target.

## Statistical

1. **Thin matched-null margin (the weakest of the eight criteria).** RICTOR's
   matched-perturbation null draws on only **200 unique matched controls**, of which
   **7 exceed RICTOR** (empirical p ≈ 0.040). The finite-pool uncertainty is real:
   the Wilson 95% CI on 7/200 reaches ≈ 0.070 and the Monte-Carlo bootstrap CI ≈
   0.065. Additional Monte-Carlo draws resample the same 200 controls and cannot
   shrink this. We therefore report "seven strong convergence checks and a nominal
   matched-null pass with borderline finite-pool uncertainty" — never "8/8 decisive".

2. **Modest effect size.** The primary reversal is +0.161 (r² ≈ 2.6%). It is highly
   robust in direction, but small in magnitude.

3. **Disease-vector cohorts and the external concordance.** The internal
   disease-donor statistics come from one JIA atlas (11 paired donors); its
   leave-one-donor-out is within-cohort robustness. An **external same-disease
   concordance** test (GSE160097; 6 donor pairs; RICTOR +0.165 vs internal +0.161;
   6/6 paired leave-one-donor-pair-out; paired bootstrap excluding zero) reproduces
   the direction in a second JIA cohort — but it is **bounded**: it is an
   **observational** disease vector (a synovial-fluid-vs-blood *compartment* contrast,
   not disease-vs-healthy), rests on **six donor pairs**, involves **no external
   RICTOR perturbation** and **no therapeutic validation**, defines the memory-CD4
   population by **published FACS sorting**, and is `NO_OVERLAP_DETECTED_BUT_NOT_FULLY_VERIFIABLE`
   for cohort-independence (the two JIA cohorts share the Charité/DRFZ Berlin
   ecosystem; reported as *external*, not *independent*). It is external same-disease
   *concordance*, not cross-cohort *causal/perturbation replication*. See
   [EXTERNAL_CONCORDANCE_GSE160097.md](EXTERNAL_CONCORDANCE_GSE160097.md).

## Biological / design

4. **Disease surrogate, not disease-vs-healthy.** The disease direction is
   **synovium (tissue + fluid) vs peripheral blood** within JIA patients — an
   inflamed-site-vs-circulation contrast, not diseased-vs-healthy tissue and not
   adult rheumatoid arthritis. Compartment and disease effects are partially
   confounded by construction.

5. **Same-cohort sensitivity is not independent replication.** RICTOR is positive on
   both the primary raw-count vector (+0.161) and the old covariate-adjusted vector
   (+0.147), but both derive from the same cohort. This is a sensitivity analysis,
   not biological replication.

6. **Two substrates, one signal.** The primary responder-resolved reversal (+0.161)
   and the conservative all-cell null-substrate projection (+0.131) are the same
   directional effect measured in two deliberately different spaces (see
   [Methods](METHODS.md)). We never mix them silently, but the difference is a
   representation effect a reader must keep in mind.

7. **Not all 924 perturbations were deep-validated.** The screen scored 924
   perturbations; only a small shortlist underwent biological-robustness analysis and
   only selected leads underwent responder/guide/donor/disease-level deep validation.
   Screen-level status is not a deep-validation verdict.

## Translational — now audited (STOP)

The translational-readiness audit is **complete** and yields a **STOP** verdict,
`NOT_ADVANCEABLE_WITH_CURRENT_EVIDENCE_AND_MODALITIES`
([TRANSLATIONAL_AUDIT_UPDATE.md](TRANSLATIONAL_AUDIT_UPDATE.md);
[verdict + tables](../results/translational/)). This is a limitation of RICTOR as a
*target*, not of the biological result.

8. **Modality gap (RICTOR).** No validated RICTOR-selective small molecule, degrader,
   glue, peptide, or clinical modality exists; the JR-AB2-011 tool compound acts
   RICTOR-independently (off-target). We do **not** claim a druggable route exists.

9. **Systemic safety constrained (RICTOR).** RICTOR is loss-of-function-intolerant
   (embryonic-lethal knockout; metabolic/cardiac/developmental liabilities) and its
   immune effects oppose across cell types (required for effector Th but destabilizes
   Treg). Systemic-inhibition safety is not established.

10. **No human-genetic efficacy support (RICTOR).** No GWAS/colocalization links
    RICTOR to RA/SLE/JIA, and the 5p13.1 locus is confounded by neighbour genes
    (OSMR, FYB1). The one genuinely open item is **independent same-tissue
    replication**, scoped as a future-validation plan.

## Scope of what we do not claim

We do **not** claim that RICTOR is a validated drug target, that systemic RICTOR
inhibition is safe, that a selective RICTOR modality exists, that PAK2 is an
anti-inflammatory target, or that the nominal matched-null significance is
definitive. See the "What we do not claim" box in the [README](../README.md) and the
[manuscript roadmap](MANUSCRIPT_ROADMAP.md) for the analyses required to move any of
these from *bounded* to *established*.
