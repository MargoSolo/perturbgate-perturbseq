# Claims and evidence

Every headline claim in PerturbGate resolves to a supporting artifact. This document
is the human-readable companion to [`results/frozen/claims.json`](../results/frozen/claims.json);
`perturbgate verify` fails if any claim's `supporting_artifacts` are missing on disk
(see `src/perturbgate/claim_ledger.py`, `tests/test_frozen_results.py`). No public
claim is allowed to exist without an artifact.

Effect sizes, denominators and uncertainty are reported — never a p-value alone.

---

## CLAIM-RICTOR-01 — retained mechanism hypothesis

> RICTOR knockdown reverses the corrected activated-memory JIA synovium-vs-blood
> disease direction at **+0.161** centered-Pearson (r² ≈ 2.6%); it is retained as a
> **disease-reversing mechanism node with a modality gap**, not a validated drug
> target.

- **Type:** mechanism hypothesis · **Evidence status:** supported (bounded) · **Depth:** DEEP
- **Metrics:** primary reversal +0.161 (p=1.8e-63); guides +0.141 / +0.178; disease-donor
  LODO 11/11 positive; conditions +0.153 / +0.092 / +0.042; matched percentile 96.5;
  matched empirical p 0.0398.
- **Denominator:** 10,832 aligned genes; 11 paired disease donors; 924-perturbation
  matched pool (k=200).
- **Uncertainty:** matched-null 95% CI (Wilson) 0.017–0.070; finite pool of 200 controls.
- **Limitations:** matched-null is the weakest of the eight criteria; synovium-vs-blood
  is not disease-vs-healthy; no independent same-tissue replication; no selective
  small-molecule modality (modality gap).
- **Supersedes:** SUP-01 (old +0.43).
- **Artifacts:** `primary_comparison.tsv`, `rictor_guides.tsv`, `rictor_lodo.tsv`,
  `rictor_conditions.tsv`, `matched_null.tsv`, `confound_decomposition.tsv`.

## CLAIM-PAK2-01 — negative result (rejected)

> PAK2 is a real, reproducible CD4 T-cell perturbation hit that is **not
> therapeutically directional**: it does not reverse the disease state (+0.010,
> p=0.297, n.s.), its apparent external JIA enrichment is activation-confounded, and
> partial-inhibition sufficiency was not established. PAK2 is **rejected** as a target
> nomination.

- **Type:** negative result · **Evidence status:** rejected after deep validation · **Depth:** DEEP
- **Metrics:** primary reversal +0.010 (p=0.297); matched percentile 41.3; responder
  fraction 0.765; guide concordance 0.85; knockdown ≈ 83–86%.
- **Denominator:** 10,832 aligned genes; responder Mixscape on 11/12 retained subsets;
  112-gene frozen programme.
- **Uncertainty:** the cellular effect is real and reproducible; the therapeutic
  direction is *absent*, not merely weak.
- **Supersedes:** SUP-02, SUP-03, SUP-04, SUP-05.
- **Artifacts:** `primary_comparison.tsv`, `matched_null.tsv`, `rejection_ledger.tsv`.

## CLAIM-RIPK1-01 — comparator

> RIPK1 is retained only as a **comparator** that is not directionally supported by
> this disease-reversal test (+0.038, incoherent GSEA, matched-null 42nd percentile).

- **Type:** comparator · **Evidence status:** not directionally supported · **Depth:** DEEP
- **Metrics:** primary reversal +0.038; GSEA reversal +0.100 (incoherent); matched
  percentile 42.2.
- **Denominator:** 10,832 aligned genes; single-condition (Stim48hr) coverage only.
- **Uncertainty:** benchmark comparator; neither nominated nor rejected by this test.
- **Artifacts:** `primary_comparison.tsv`, `matched_null.tsv`.

## CLAIM-PROCESS-01 — the process is the contribution

> PerturbGate preserves negative and superseded results: candidate attrition, detected
> confounds, and corrected interpretations are first-class, auditable outputs, not
> hidden debugging history.

- **Type:** process · **Evidence status:** supported · **Depth:** ARTIFACT
- **Metrics:** 924 perturbations; 6 documented decision stages; 5 superseded claims.
- **Artifacts:** `candidate_funnel.tsv`, `rejection_ledger.tsv`, `gate_ablation.tsv`,
  `superseded_claims.json`.

---

## Controlled public labels

Only these labels may carry a public decision:

| Entity | Label |
|---|---|
| RICTOR | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` |
| PAK2 | `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` |
| RIPK1 | `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` |

See [ANALYSIS_CONTRACT.md](ANALYSIS_CONTRACT.md) for the full vocabulary and the
confirmatory/exploratory boundary, and [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md)
for the registry of corrected claims.
