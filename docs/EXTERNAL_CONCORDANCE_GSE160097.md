# External same-disease concordance — GSE160097

**Evidence class:** `SAME_DISEASE_PAIRED_COMPARTMENT_CONCORDANCE_SUPPORTED`
**Cohort-independence:** `NO_OVERLAP_DETECTED_BUT_NOT_FULLY_VERIFIABLE`

> The frozen RICTOR-knockdown signature showed **external same-disease, paired-compartment transcriptional concordance** in GSE160097. This is **not** replicated therapeutic efficacy, therapeutic/causal replication, clinical validation, a validated drug target, an independent RICTOR *perturbation* experiment, or proof that RICTOR inhibition treats JIA.

## Dataset

- **GEO:** [GSE160097](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160097) · **PMID:** 33296081 (Maschmeyer et al., 2020).
- **Design:** 10x scRNA-seq (+ TCR) of **FACS-sorted memory T cells** from **paired synovial fluid (SF) and peripheral blood (PB)** of patients with juvenile idiopathic arthritis (JIA).
- **Primary population:** conventional memory CD4 T cells **Tcon (CD4⁺CD45RO⁺CD25⁻)** — the published sort and the direct analog of the internal *activated-memory* CD4 state. (Treg = CD4⁺CD45RO⁺CD127ˡᵒCD25⁺ used only as a sensitivity.)
- **Primary input:** **raw UMI counts** (10x `filtered_gene_bc_matrices` / `filtered_feature_bc_matrix`; hg19/GRCh37 reference; gene IDs are Ensembl — aligned natively to the KD vectors, no symbol mapping).

## Contract and method (frozen before scoring)

Contract: [`results/external_validation/gse160097/analysis_contract.json`](../results/external_validation/gse160097/analysis_contract.json).

- **Unit:** donor pair. **Contrast:** SF − PB within the same donor.
- **Disease vector (raw-count, paired):** for each donor *d*, pseudobulk = sum of raw UMI over that donor's QC'd (≥200 genes/cell) Tcon cells per compartment; `logFC_d = log2(CPM_SF+1) − log2(CPM_PB+1)`; `effect = mean over the 6 donor pairs of logFC_d` (each pair equal weight; no cell-count weighting; no pseudo-count reconstruction).
- **Score:** the public `perturbgate.reversal.reversal` (−centered Pearson; `min_shared=200`, `floor=0.10`). Positive = KD opposes the SF−PB joint programme.
- **Uncertainty:** donor-pair based only — paired leave-one-donor-pair-out and paired donor bootstrap. Gene-level Pearson p-values are **not** used as confirmatory evidence (genes are correlated, not independent replicates).

## Result

| candidate | external reversal | notes |
|---|--:|---|
| **RICTOR** | **+0.165** (Spearman +0.102) | internal reference **+0.161**; 14,806 aligned genes |
| PAK2 | +0.002 | does not reverse |
| RIPK1 | −0.007 | does not reverse |

- **Paired leave-one-donor-pair-out:** 6/6 positive, range **+0.147 … +0.177** ([`paired_lodo.tsv`](../results/external_validation/gse160097/paired_lodo.tsv)).
- **Paired donor bootstrap** (resamples the 6 pairs, seed 0, 1000 draws): median **+0.160**, 95% interval **+0.113 … +0.191**, **100% positive** ([`paired_bootstrap_summary.tsv`](../results/external_validation/gse160097/paired_bootstrap_summary.tsv)).
- **Treg sensitivity:** RICTOR **+0.165** (7 pairs).
- **Concentration / confound audit** ([`confound_sensitivity.tsv`](../results/external_validation/gse160097/confound_sensitivity.tsv), [`egress_sensitivity.tsv`](../results/external_validation/gse160097/egress_sensitivity.tsv)): no single gene (0.9%) or small leading edge (top-10 ≈ 4%) dominates; removing the top-25 genes leaves ≈ +0.132; the **KLF2/SELL/S1PR1/TCF7 egress module contributes < 1%** and removing it leaves ≈ +0.164. Major aligned drivers: **CXCR6, RGS1, IFNG, CCR5, CCR1, CCR2, XCL1, XCL2, GZMA, GZMB** — an inflammatory effector programme, not a generic egress module.

## Cohort-independence audit

Full table: [`cohort_independence_audit.tsv`](../results/external_validation/gse160097/cohort_independence_audit.tsv).

The internal disease-vector cohort is the CZ CELLxGENE JIA atlas (dataset `612b7bff…`, collection `10eb236d…`; Knight et al. 2026; GEO GSE278962/278968/278969), donor IDs `2518-xxx`/`2519-xxx`. GSE160097 is a separate accession/publication/lab-group with donor IDs "JIA patient 1..7", a different assay design, and (per the atlas title) a treatment-naive design that GSE160097 does not share. No shared donor identifier was found and the atlas does not list GSE160097 as a source.

**However**, both cohorts originate from the **Charité / DRFZ Berlin** institutional ecosystem, and both datasets are de-identified, so individual-patient non-overlap **cannot be fully verified**. We therefore report `NO_OVERLAP_DETECTED_BUT_NOT_FULLY_VERIFIABLE` and use the wording **"an external public JIA cohort with no detected donor overlap"** — never "an independent cohort".

## Reproduce

```bash
make external-gse160097          # offline: rebuild reversal + paired LODO/bootstrap + figure from committed derived aggregates
# or:
python -m perturbgate.external.gse160097
```

The offline default recomputes the external numbers from **committed, legally redistributable derived aggregates** — the per-gene disease vector and the per-donor-pair log2FC (`results/external_validation/gse160097/`) — and the committed KD vectors (`data/demo/kd_meta_*.tsv.gz`), using the same `perturbgate.reversal.reversal` function. Seed 0; 1000 bootstrap draws; validated against golden values in `tests/test_external_gse160097.py`.

### Full-data route (official public download; raw not redistributed)

`python -m perturbgate.external.gse160097 --download` rebuilds the raw-count paired pseudobulk from the official GEO files below. Raw 10x H5 files are **not** redistributed in this repository (see [DATA_LICENSES.md](DATA_LICENSES.md)); download them from GEO and verify sha256:

| GSM | patient | compartment | file | sha256 |
|---|---|---|---|---|
| GSM4859835 | JIA patient 1 | SF | `GSM4859835_PM1_CD4_SF_p1_filtered_gene_bc_matrices_h5.h5` | `a9d4a1317a78366840c11f3864e0a633b36c7f1f221eb985b09c7f05d46623be` |
| GSM4859836 | JIA patient 2 | SF | `GSM4859836_PM1_CD4_SF_p2_filtered_gene_bc_matrices_h5.h5` | `a89621dbb23fb7ffbfaaabeb33d809484a50f751b38160e19f5946deb61cfc05` |
| GSM4859837 | JIA patient 3 | SF | `GSM4859837_PM1_CD4_SF_p3_filtered_gene_bc_matrices_h5.h5` | `4205e7dd1dac60f4f633a63b27308175658fb50357d280f094c8fab29fc6517a` |
| GSM4859838 | JIA patient 4 | SF | `GSM4859838_PM1_CD4_SF_p4_filtered_gene_bc_matrices_h5.h5` | `a5f321ff381f4f6627dd23635294df1e08cd4107a970e180b95d86f9dc6f312e` |
| GSM4859839 | JIA patient 5 | SF | `GSM4859839_PM1_CD4_SF_p5_filtered_gene_bc_matrices_h5.h5` | `e852a9ece3b08c1a83228a7b08f8eaa518596eaee05e53ced9ee136fe6cb505e` |
| GSM4859840 | JIA patient 6 | SF | `GSM4859840_PM1_CD4_SF_p6_filtered_feature_bc_matrix.h5` | `05eead28b6147a62a02c2cd732f1d29074441cb8c420ca9cf315af6fb2513ecf` |
| GSM4859841 | JIA patient 7 | SF | `GSM4859841_PM1_CD4_SF_p7_filtered_feature_bc_matrix.h5` | `3ea483a3b9e25ccf4d018573cf6d03279e799ab8d358ab77b20b6de6e7f44985` |
| GSM4859842 | JIA patient 1 | PB | `GSM4859842_PM4_CD4_blood_p1_filtered_gene_bc_matrices_h5.h5` | `2ee65874775685d8d104e8472cb072721a776478450d3687bee6c240d796b717` |
| GSM4859843 | JIA patient 2 | PB | `GSM4859843_PM4_CD4_blood_p2_filtered_gene_bc_matrices_h5.h5` | `8f3848c7a57a94026865e0f7c736aeb53e439c905303a6efb930b89074e3adce` |
| GSM4859844 | JIA patient 4 | PB | `GSM4859844_PM4_CD4_blood_p4_filtered_gene_bc_matrices_h5.h5` | `2d50ac0f4f401929234d321bee508fc176353718ed109b4b397e0c241e129a7d` |
| GSM4859845 | JIA patient 5 | PB | `GSM4859845_PM4_CD4_blood_p5_filtered_gene_bc_matrices_h5.h5` | `096dce37c5517a0f4b42a7a623c477e6965a0bece5a2c89bc339a682e2f17d7c` |
| GSM4859846 | JIA patient 6 | PB | `GSM4859846_PM4_CD4_blood_p6_filtered_feature_bc_matrix.h5` | `622d65dcc663eb511aa9ae2fef7d1c633cb197219faebee8ae1fc52481c3c588` |
| GSM4859847 | JIA patient 7 | PB | `GSM4859847_PM4_CD4_blood_p7_filtered_feature_bc_matrix.h5` | `fe9df163f4f572873e8bb209c3e15d2db21bc4204ffedcc14c1873c0dfaa198b` |

Base URL pattern: `https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM4859nnn/<GSM>/suppl/<file>`. Patient 3 SF Tcon has no paired PB Tcon and is excluded from the primary (6 pairs). Series metadata: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160097/matrix/GSE160097_series_matrix.txt.gz`.

## Environment / reproducibility

Python ≥ 3.10; numpy, pandas, scipy, matplotlib; seeds — numpy global 0, bootstrap draws 0..999. Offline route runs on a laptop in seconds. Expected outputs: `results/external_validation/gse160097/recomputed/` + `figures/supplementary_external_jia_concordance.{png,svg}` + its source data. Golden values are asserted in `tests/test_external_gse160097.py`.

## Limitations

- Observational disease vector — a **compartment** contrast (SF vs blood), **not** disease-vs-healthy.
- **Six** donor pairs.
- **No external RICTOR perturbation** experiment (RICTOR was not knocked down in GSE160097).
- **No therapeutic validation.**
- Memory-CD4 population defined by **published FACS sorting**.
- Internal and external JIA cohorts share the **Charité/DRFZ Berlin** ecosystem → donor-level independence is **not fully verifiable**.
