# RICTOR — origin and decision path (provenance-reconstructed)

This document records the **evidence-reconstructed** origin and decision path of RICTOR, so that
the public description cannot be misread as a post-hoc rescue that appeared after the screen-wide
"0 advanceable targets". Every value here traces to a source artifact; the full audit with
`VERIFIED / PARTIALLY_VERIFIED / CONTRADICTED / UNVERIFIED` status per claim is in
[`results/rictor_provenance/provenance_ledger.tsv`](../results/rictor_provenance/provenance_ledger.tsv).

## One-paragraph origin

**RICTOR was nominated directly by the real-data direct disease-rescue analysis** (the internal
"Screen 8" competitive-specificity + hard-filter + disease-reversal pipeline over the genome-scale
CD4 Perturb-seq substrate). It emerged as a **de novo** candidate (`prior_class = none` — *not* from
literature or the effect-blind prior, *not* a manual pick), ranked **307 of 920** with competitive
specificity-t **2.205** (driving program Th1/IFN-γ at Stim48hr), the **broadest disease-reversal
projection in the panel (0.673)**, identity preserved, and **above the MALT1 fallback** on rank,
specificity and disease-reversal. It was then **independently recomputed on the server** from
donor- and guide-resolved source artifacts (`by_donors.h5mu`, `by_guide.h5mu`): **6/6 donor pairs at
the driving Stim48hr (minimum comp-t 1.59)**, **both guides** suppressing, survival across **all six
ablation methods**, with clean 8D data gates. Only afterwards did the deeper analyses add the internal
disease-reversal score (**+0.161**), external same-disease concordance in GSE160097 (**+0.165**), and
the translational red-team (genetics null, modality gap, safety conflict, retracted prior art).

## Separated claims (do not merge into "validated drug target")

| Axis | Status |
|---|---|
| **Discovery** | `SCREEN8_DIRECT_DISEASE_RESCUE_NOMINATION` |
| **Technical validation** | `DONOR_GUIDE_ABLATION_SUPPORTED` |
| **Internal biological evidence** | `DISEASE_REVERSAL_SUPPORTED` |
| **External evidence** | `SAME_DISEASE_PAIRED_COMPARTMENT_CONCORDANCE_SUPPORTED` |
| **Translational readiness** | `NOT_ADVANCEABLE_WITH_CURRENT_EVIDENCE_AND_MODALITIES` |

## Verified decision path (branched, not linear)

```
Genome-scale CD4 Perturb-seq substrate (924 perturbations with usable effect vectors)
├── Screen-wide general target pipeline
│     924 → 208 (biological robustness) → 21 (safety/tractability) → 0 advanceable drug targets
│     ("0" = 0 candidates that passed translational readiness, not 0 biologically-supported hypotheses)
└── Direct disease-rescue analysis ("Screen 8": competitive-specificity + hard filters + disease-reversal)
      ├── PAK2   — most specific de novo node (spec_t 4.745); nominated; Treg-tolerance + modality liabilities
      ├── RICTOR — de novo nomination (spec_t 2.205; disease-reversal 0.673; rank 307; beats MALT1)
      │     ├── independent server recompute: 6/6 donors @ Stim48hr (min comp-t 1.59), both guides, 6/6 ablations
      │     ├── internal disease reversal +0.161 (corrected raw-count JIA vector) + guide/donor/condition/confound/matched-null
      │     ├── external same-disease concordance +0.165 (GSE160097)
      │     └── translational STOP (genetics null, modality gap, safety conflict)
      ├── RIPK1  — known clinically-druggable translational anchor / comparator (prior_class canonical_activator)
      └── MALT1  — demoted fallback (spec_t 1.389; broad/non-specific)
```

## Screen-8 → funnel relationship (answered)

- **From which artifact did RICTOR emerge?** `table_screen8A_all_candidates.csv` (candidate row, rank 307/920), carried through `table_screen8B_disease_projection_all.csv` (disease-reversal 0.673), `rictor_ablation_robustness.csv`, `rictor_8d_hardening.csv`, and nominated as a lead in `screen8_project_summary.md`.
- **Nomination rule:** competitive gene-set specificity-t (a program's KD suppression vs the perturbation's own genome-wide background) **> 2**, plus hard identity/toxicity/donor/direction filters, plus a disease-reversal projection and triangulation against MALT1. RICTOR passed this rule de novo.
- **Other genes from the same rule/analysis:** PAK2 (nominated), RIPK1 (comparator/anchor), MALT1 (fallback), plus the broader 8D candidate set (PSMB9, GPR15, WNK1, NFKB1, WASF2, EP300, …).
- **Was PAK2 nominated by the same rule?** Yes — same Screen 8 competitive-specificity rule (spec_t 4.745), independently.
- **MALT1 role:** fixed triangulation **fallback/comparator** (spec_t 1.389) that the specific nodes had to beat; not a nomination.
- **RIPK1 role:** known clinically-druggable **translational anchor / benchmark comparator**, not a de novo nomination by this test.
- **How does 924 → 208 → 21 → 0 relate to Screen 8?** Same genome-scale substrate; the funnel is the *screen-wide general-target* pipeline (ends in 0 **advanceable** targets), while Screen 8 is the *direct disease-rescue* branch that did surface mechanism leads (PAK2, RICTOR). RICTOR is one of the 924; it is **not** post-funnel and **not** manual.
- **What does "0" mean?** Zero candidates that passed **translational readiness** (advanceable drug), **not** zero biologically-supported hypotheses.

## Sign-convention note (important)

The scores below are **different metric definitions** and are **not directly comparable as effect
sizes**, though they express a **consistent biological direction** (RICTOR KD suppresses the
pathogenic program / reverses the disease signature):

- Screen 8 **competitive specificity-t** and **comp-t** (positive = program suppressed vs background).
- Screen 8 **disease-reversal projection** (0..1, higher = more reversal).
- Later **reversal score** `−centered Pearson(KD, disease)` (positive = KD opposes disease); internal **+0.161**, external **+0.165**.
- Per-donor **program mean log2FC** (negative = KD lowers the program).

## Discrepancies preserved (not smoothed over)

1. **8D call vs project summary.** `rictor_8d_hardening.csv` records `screen8D_final_call = PARK`
   (no clinical-precedence druggability), while the authoritative `screen8_project_summary.md`
   elevates RICTOR to a **PRIMARY LEAD** ("FULLY HARDENED, indep server recompute") with an explicit
   modality-gap caveat; an intermediate `verdict_screen8.md` omits RICTOR from its final roles. The
   reconciliation: RICTOR's **data/biology** gates passed and it was nominated as a lead, but its
   **druggability** was parked — i.e. the modality gap was present from the start.
2. **Matched-null is fragile.** The covariate-matched null is **borderline** (p ≈ 0.045–0.056; only
   ~12% of 200 fold-splits < 0.05) — significant but not stably so after covariate adjustment.
3. **RICTOR is weaker than PAK2** (spec_t 2.21 vs 4.75; ablation rank 86 vs 7).

## CONTRADICTED / UNVERIFIED numeric claims (must not be used publicly)

- "RICTOR pathogenic-program suppression **−0.350**" and "MALT1 **−0.202**" — **not present** in any
  artifact. Real metrics: RICTOR spec_t **2.205** / disease-reversal **0.673**; MALT1 **1.389** / **0.544**.
- "RICTOR **FDR 0.005**" and "MALT1 **FDR 0.019**" — **mislabeled**. `0.005` and `0.019` are RICTOR's own
  disease-reversal **specificity p-values for Psoriasis and RA**, not FDRs on a −0.350 suppression.

Full evidence: [`results/rictor_provenance/`](../results/rictor_provenance/) and the audit under
`audit/rictor_provenance/`.
