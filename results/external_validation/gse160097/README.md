# results/external_validation/gse160097/

Curated public artifacts for the **GSE160097 external same-disease concordance** test
(paired JIA synovial-fluid vs blood memory CD4). External-only; the frozen internal
results under `results/frozen/` are unchanged. Full write-up:
[docs/EXTERNAL_CONCORDANCE_GSE160097.md](../../../docs/EXTERNAL_CONCORDANCE_GSE160097.md).

- **Evidence class:** `SAME_DISEASE_PAIRED_COMPARTMENT_CONCORDANCE_SUPPORTED`
- **Cohort-independence:** `NO_OVERLAP_DETECTED_BUT_NOT_FULLY_VERIFIABLE` ("external public JIA cohort with no detected donor overlap"; not "independent").
- **Headline:** RICTOR external reversal **+0.165** (internal reference +0.161); 6 donor pairs; 6/6 positive leave-one-pair-out; paired bootstrap 95% CI +0.113…+0.191 (100% positive); PAK2 +0.002, RIPK1 −0.007.

## Files

| file | contents |
|---|---|
| `analysis_contract.json` | frozen contract (population, contrast, score, universe, decision rules) |
| `cohort_independence_audit.tsv` | disjoint-identifier audit + verdict |
| `donor_accounting.tsv` | per-donor Tcon cells (SF/PB), QC, pair-used flag |
| `candidate_external_concordance.tsv` | RICTOR/PAK2/RIPK1 reversal scores |
| `paired_lodo.tsv` | leave-one-donor-pair-out (all 3 candidates) |
| `paired_bootstrap_summary.tsv` | paired donor bootstrap (median, 95% CI, frac-positive) |
| `leading_edge.tsv` | top reversal-contributing genes |
| `confound_sensitivity.tsv` | gene-class contribution + reversal-after-removal |
| `egress_sensitivity.tsv` | egress-module vs inflamed-effector decomposition |
| `gene_universe_audit.tsv` | KD ∩ disease alignment per candidate |
| `result_manifest.json` | claim, result, checksums, provenance |
| `gse160097_sf_vs_pb_cd4mem_disease_vector.tsv` | derived aggregate disease vector (offline reproduction input) |
| `donor_paired_logfc_tcon.tsv.gz` | derived per-donor-pair log2FC (offline LODO/bootstrap input) |
| `recomputed/` | written by `make external-gse160097` |

Raw 10x H5 files are **not** redistributed here; see the official download route + checksums in
[docs/EXTERNAL_CONCORDANCE_GSE160097.md](../../../docs/EXTERNAL_CONCORDANCE_GSE160097.md).

## Reproduce

```bash
make external-gse160097   # or: python -m perturbgate.external.gse160097
```
