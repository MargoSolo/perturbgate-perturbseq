# Search log — RICTOR / Screen 8 provenance

**Workspace searched:** private research workspace (`48h_target_validation/`,
`outputs/screen8/`, `server-results/`, `src/`, `tests/`, `git log --all`) and the public
`perturbgate-perturbseq` repository. File names and file contents both searched.

## Terms
RICTOR · MALT1 · PAK2 · RIPK1 · Screen 8 · screen8 · direct rescue · direct_rescue · disease reversal ·
disease_reversal · pathogenic suppression · pathogenic_suppression · FINAL_VERDICT · candidate-scored ·
unverified · 8A · 8B · 8C · 8D · by_donors · by_guide · h5mu · extract_rictor · comp-t · comp_t ·
Th1_IFNG · Stim48hr · ablation · Treg · identity · growth arrest · global collapse · focal ·
program selective · effect vector · effect_vector

## Primary-evidence artifacts located
- `outputs/screen8/tables/table_screen8A_all_candidates.csv` — RICTOR candidate row (spec_t 2.205, rank 307, prior_class none, passes_hard_filters True).
- `outputs/screen8/tables/table_screen8B_disease_projection_all.csv` — RICTOR disease_reversal_mean 0.673 (> MALT1 0.544).
- `outputs/screen8/tables/table_screen8D_malt1_comparison.csv` — triangulation vs MALT1 (nominates PAK2/RIPK1; RICTOR absent from this table).
- `outputs/screen8/rictor_8d_hardening.csv` — Th1_IFNG/Stim48hr, identity preserved, no global collapse, screen8D_final_call PARK, data_gates_pass True.
- `outputs/screen8/rictor_ablation_robustness.csv` — six ablation methods (A…F), all positive.
- `server-validation/rictor_donorpair_validation.csv` — 6 donor pairs @ Stim48hr, 6/6 positive, min comp-t 1.586.
- `server-validation/rictor_guide_validation.csv` — guide_1/guide_2 comp-t across conditions.
- `src/screen8/extract_rictor_donor_guide.py (server-side)` — opens `GWCD4i.DE_stats.by_donors.h5mu` + `by_guide.h5mu`.
- `48h_target_validation/results/stats/rictor_statistical_verdict.md` — 6/6 (min 1.59), guides, ablation, disease-reversal specificity (Pso 0.005, RA 0.019, IBD 0.047), borderline matched null.
- `outputs/screen8/screen8_project_summary.md` — **authoritative**: RICTOR = PRIMARY LEAD, FULLY HARDENED, nominated with PAK2, beats MALT1.
- `outputs/screen8/verdict_screen8.md` — intermediate verdict (omits RICTOR from final roles → discrepancy).

## Not found / negative results
- `−0.350` (RICTOR pathogenic suppression) and `−0.202` (MALT1) — **not present** in any artifact.
- No deleted/renamed Screen 8 or RICTOR artifacts in `git log --all --diff-filter=D` (nothing hidden).
- The PAK2/RIPK1 `screen8_donorpair_validation.csv` / `screen8_guide_validation.csv` contain **no RICTOR rows** — RICTOR's donor/guide recompute lives in the separate `rictor_donorpair_validation.csv` / `rictor_guide_validation.csv` (located).

## Raw data NOT redistributed
`GWCD4i.DE_stats.by_donors.h5mu` / `by_guide.h5mu` (server-side raw donor/guide DE) were read for
provenance only; not copied to the public repo. Only derived, anonymized summaries were curated.
