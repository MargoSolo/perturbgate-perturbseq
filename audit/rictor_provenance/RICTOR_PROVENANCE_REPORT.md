# RICTOR provenance reconstruction — audit report

Strict, evidence-based reconstruction of RICTOR's origin, validation, and interpretation from the
real project artifacts (private research workspace) before any public documentation was changed.
Per-claim ledger: [`RICTOR_PROVENANCE_LEDGER.tsv`](RICTOR_PROVENANCE_LEDGER.tsv) (33 claims: 28
VERIFIED, 1 PARTIALLY_VERIFIED, 4 CONTRADICTED). Curated public artifacts:
[`../../results/rictor_provenance/`](../../results/rictor_provenance/). Corrected public narrative:
[`../../docs/RICTOR_ORIGIN_AND_DECISION_PATH.md`](../../docs/RICTOR_ORIGIN_AND_DECISION_PATH.md).

## Method
Searched the private workspace (`48h_target_validation/`, `outputs/screen8/`, `server-results/`, scripts,
verdicts, and `git log --all`) for the terms in `search_log.md`. Read the actual Screen 8 candidate
tables (8A/8B/8C/8D), the RICTOR-specific 8D hardening and ablation tables, the server donor/guide
recompute CSVs, the RICTOR statistical verdict, and the authoritative Screen 8 project summary.
No file, value, date, or count was invented; discrepancies are preserved.

## Verified origin (the core fact)
**RICTOR was nominated de novo by the real-data direct disease-rescue analysis (internal "Screen 8").**
It is a genuine screen candidate (`table_screen8A_all_candidates.csv`, `prior_class = none` — not from
literature/effect-blind prior, not manual, not post-hoc), competitive specificity-t **2.205** (Th1/IFN-γ,
Stim48hr), disease-reversal projection **0.673** (broadest in panel), rank **307/920**, identity
preserved, **above the MALT1 fallback**. Independently recomputed on the server from
`by_donors.h5mu`/`by_guide.h5mu` via `extract_rictor_donor_guide.py (server-side)`: **6/6 donor pairs @ Stim48hr (min
comp-t 1.586)**, both guides (g1 1.45 / g2 2.74), survives **all six ablation methods**. Elevated to a
Screen 8 **PRIMARY LEAD** in `screen8_project_summary.md`. The Stage-3 questions (nomination rule,
other candidates, PAK2/MALT1/RIPK1 roles, funnel relationship, meaning of "0") are answered in
`docs/RICTOR_ORIGIN_AND_DECISION_PATH.md`.

## Discrepancies preserved
1. **8D call vs project summary.** `rictor_8d_hardening.csv` → `screen8D_final_call = PARK` (druggability);
   `screen8_project_summary.md` → RICTOR **PRIMARY LEAD**; intermediate `verdict_screen8.md` omits RICTOR
   from final roles. Reconciliation: data/biology gates passed and RICTOR was nominated as a lead; the
   **druggability was parked** (modality gap present from the start).
2. **Matched-null fragile** — covariate-matched null p ≈ 0.045–0.056; only ~12% of 200 fold-splits < 0.05.
3. **RICTOR weaker than PAK2** — spec_t 2.21 vs 4.75; ablation rank 86 vs 7.

## CONTRADICTED / UNVERIFIED (excluded from public claims)
| prompt claim | verdict | reality |
|---|---|---|
| RICTOR pathogenic suppression **−0.350** | CONTRADICTED | not present; real = spec_t 2.205 / disease-reversal 0.673 / per-donor program log2FC ≈ −0.26 |
| MALT1 **−0.202** | CONTRADICTED | not present; real MALT1 = spec_t 1.389 / disease-reversal 0.544 |
| RICTOR **FDR 0.005** | CONTRADICTED | 0.005 = RICTOR's **Psoriasis** disease-reversal specificity p (not an FDR on −0.350) |
| MALT1 **FDR 0.019** | CONTRADICTED | 0.019 = RICTOR's **RA** disease-reversal specificity p (not MALT1's FDR) |

## Unresolved / partially-verified
- **A8 Treg-safer** is `PARTIALLY_VERIFIED` — an **external-literature** label (mTORC2/Rictor loss favours
  Foxp3⁺ Treg), not measured in-screen.
- **A11 lead-vs-park discrepancy** is real and preserved (not resolved to a single call).
- The prompt's exact `−0.350 / −0.202` remain **UNVERIFIED** (no artifact); they are not used publicly.

## Boundaries respected
No AMP Phase 1 content was added publicly. No raw H5MU / private paths / cluster names / usernames /
job IDs / credentials were committed. Frozen scientific values (+0.161, +0.165, matched-null, counts)
were **not** changed — only provenance/interpretation text and new curated provenance artifacts were added.
