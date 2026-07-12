# Source snapshot

This public repository is a clean, anonymised package built from a private research
working tree. This file maps each public scientific artifact to its source, using
**repository-relative source paths only** — no private absolute paths, hostnames,
usernames, or compute-environment details are exposed here or anywhere in the repo.

The anonymised transform that produced the mechanical artifacts is
`scripts/build_public_inputs.py` (reads generic `SERVER_*` environment roots); the
curated artifacts are produced by `scripts/build_curated_frozen.py`.

## Authoritative source commits (private tree)

| Layer | Commit(s) | Role |
|---|---|---|
| RICTOR primary result | `6c0515d`, `adf5b23` | bounded raw-count disease-reversal rescue (authoritative) |
| PAK2 final decision | `b9b89a9`, `0067ed2` | technical validation + therapeutic rejection |
| Broad screen / attrition | `fa76791`, `febec10` | screen-level rankings, attrition, provenance checksums |

Authoritative primary disease-vector checksum (md5):
`2b18d92684db1f70b637e1f098374c7e`.

## Public artifact → private source

| Public artifact | Source (repo-relative) |
|---|---|
| `data/demo/disease_vector_activated_memory.tsv.gz` | `results/rictor_rescue/disease_vector_rawcount_full.tsv` (state=activated_memory) |
| `data/demo/kd_meta_{RICTOR,PAK2,RIPK1}.tsv.gz` | `inputs/responder_de/freeze/meta_{target}_overall.tsv` |
| `data/reproduce/pseudobulk_counts.parquet` + `pseudobulk_meta.tsv` | `inputs/responder_de/` |
| `data/reproduce/disease_perdonor_logfc_activated_memory.tsv.gz` | `results/rictor_rescue/disease_perdonor_logfc_activated_memory.tsv` |
| `results/frozen/rictor_guides.tsv` | `results/rictor_rescue/guides.tsv` |
| `results/frozen/rictor_lodo.tsv` | `results/rictor_rescue/lodo.tsv` |
| `results/frozen/rictor_conditions.tsv` | `results/rictor_rescue/condition.tsv` |
| `results/frozen/matched_null.tsv` | `results/rictor_rescue/matched_null.tsv` |
| `results/frozen/rictor_matched_null_values.tsv` | recomputed from the genome-scale effect-vector substrate |
| `results/frozen/confound_decomposition.tsv` | `results/rictor_rescue/confound_decomposition.tsv` |
| `results/frozen/safety_summary.tsv` | `results/rictor_rescue/rictor_rescue_verdict.json` (safety block) |
| `results/frozen/leading_edge.tsv` | `results/rictor_rescue/leading_edge_reversed.tsv` |
| `results/frozen/all_perturbations_authoritative_reversal.tsv` | `results/rescue_screen/reversal_screen_full.tsv` + `REJECTION_LEDGER.tsv` |
| `results/frozen/rejection_ledger.tsv` | `results/rescue_screen/REJECTION_LEDGER.tsv` + deep-target decisions |
| `results/frozen/primary_comparison.tsv` | curated from `reversal_primary.tsv`, `matched_null.tsv`, PAK2 decision files |
| `results/frozen/candidate_funnel.tsv`, `gate_matrix.tsv`, `gate_ablation.tsv` | curated from the screen + deep-validation verdicts |
| `results/frozen/claims.json`, `superseded_claims.json`, `analysis_contract.json` | curated (this release) |

## Provenance code (private tree)

- `src/branch_rictor_rescue/{build_disease_vector_rawcount,score_rictor_rescue,finalize_verdict,calibration_audit}.py`
- `src/branch_disease_reversal/rescue_screen.py` and related screen scripts

The public `src/targetgate/` package re-implements the decision layer (reversal
scoring, calibration, robustness, decision gate) so that Levels 1–2 recompute the
headline values from the committed compact inputs. The recomputed RICTOR substrate
reversal reproduces the authoritative +0.1314 (7/200 exceed) bit-for-bit, and the
demo reproduces the primary +0.1606 within tolerance.

## What was deliberately excluded

Failed jobs, debugging logs, scratch files, structural-modelling (AlphaFold)
artifacts, controlled-access or cell-level data, and all compute-environment details
(cluster name, hostnames, usernames, home paths, scheduler ids, container images)
were **not** copied. See [docs/SUPERSEDED_RESULTS.md](docs/SUPERSEDED_RESULTS.md) for
interpretations that were superseded and why.
