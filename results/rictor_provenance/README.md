# results/rictor_provenance/

Curated, anonymized public artifacts documenting **where RICTOR came from** and how it was validated,
so that every public RICTOR claim resolves to evidence. Values are **extracted** from the genuine
private Level-3 artifacts (source sha256 in `result_manifest.json`); donor-pair IDs are anonymized to
`pair_N`; **no raw H5MU, private paths, or restricted data are redistributed**. Narrative +
answers: [`docs/RICTOR_ORIGIN_AND_DECISION_PATH.md`](../../docs/RICTOR_ORIGIN_AND_DECISION_PATH.md).

| file | contents |
|---|---|
| `screen8_nomination.tsv` | Screen 8 candidate metrics for RICTOR/PAK2/RIPK1/MALT1 (spec_t, disease-reversal mean, rank/920, prior_class, hard-filter pass) |
| `donor_validation.tsv` | RICTOR independent donor-pair recompute — 6 pairs, Th1_IFNG @ Stim48hr, comp-t (6/6 positive, min 1.59) |
| `guide_validation.tsv` | RICTOR both-guide recompute (guide_1/guide_2), driving program, all conditions |
| `ablation_validation.tsv` | RICTOR across the six ablation methods (all positive) |
| `provenance_ledger.tsv` | every audited claim + VERIFIED/PARTIALLY/CONTRADICTED status + source artifact |
| `result_manifest.json` | source-artifact sha256, source run commits, extraction note |

## Verified headline
- **Origin:** de novo nomination from the direct disease-rescue analysis (Screen 8) — `prior_class = none`, rank 307/920, spec_t 2.205, disease-reversal 0.673, above MALT1. Not literature, not manual, not post-hoc.
- **Independent validation:** 6/6 donor pairs @ Stim48hr (min comp-t 1.59; late-specific), both guides, 6/6 ablation methods.
- **Preserved caveats:** matched-null borderline (p ≈ 0.045–0.056); weaker than PAK2; modality gap (parked at 8D for druggability).

## Contradicted claims (not used publicly)
The values "RICTOR −0.350 / FDR 0.005" and "MALT1 −0.202 / FDR 0.019" are **not present** in any
artifact (0.005 and 0.019 are RICTOR's own Psoriasis/RA disease-reversal specificity p-values).
See `provenance_ledger.tsv` rows P1–P4.
