# Data availability

All data are open. The machine-readable manifest is
[`../data/public_data_manifest.tsv`](../data/public_data_manifest.tsv). The helper
`python scripts/download_open_data.py` prints (and, with `--execute`, runs) the exact
routes below.

## 1. Primary Human CD4+ T Cell Perturb-seq

| Field | Value |
|---|---|
| Source | Marson lab (Gladstone/UCSF) + Pritchard lab (Stanford) |
| Publication | Zhu R, Dann E, … Pritchard JK, Marson A. bioRxiv 2025 |
| DOI | [10.64898/2025.12.23.696273](https://doi.org/10.64898/2025.12.23.696273) |
| Landing page | https://virtualcellmodels.cziscience.com/dataset/genome-scale-tcell-perturb-seq |
| Processed data | `s3://genome-scale-tcell-perturb-seq/marson2025_data/` (anonymous S3) |
| Raw sequencing | GEO GSE314342 / SRA SRP643211 |
| Analysis code | https://github.com/emdann/GWT_perturbseq_analysis_2025 |
| Registration | Not required for the processed S3 bucket |
| License | MIT (+ CZI Virtual Cell Models Acceptable Use Policy) |

```bash
aws s3 cp --no-sign-request --recursive \
  s3://genome-scale-tcell-perturb-seq/marson2025_data/ data/full/perturbseq/
```

Used here for: the genome-scale perturbation effect vectors and the responder-DE
knockdown vectors, from which the committed per-gene aggregate KD vectors are derived.

## 2. JIA synovial single-cell atlas ("Integrated global cells")

| Field | Value |
|---|---|
| Source | Charité Berlin (Knight / Romagnani); synovial-tissue layer Bolton/Mahony et al. |
| Publication | Knight OC et al. bioRxiv 2026; companion Bolton C, Mahony CB et al. *Sci Transl Med* 2025 |
| DOI | [10.64898/2026.05.01.716870](https://doi.org/10.64898/2026.05.01.716870) · companion [10.1126/scitranslmed.adt6050](https://doi.org/10.1126/scitranslmed.adt6050) |
| Collection | https://cellxgene.cziscience.com/collections/10eb236d-d42d-45b8-8363-c2dcf865f388 |
| h5ad | https://datasets.cellxgene.cziscience.com/f758894c-14bc-4bfe-94dd-16dd9945f7d3.h5ad |
| Registration | Not required |
| License | CC-BY-4.0 (CZ CELLxGENE Discover) |

```bash
curl -L -o data/full/jia_synovial_integrated.h5ad \
  https://datasets.cellxgene.cziscience.com/f758894c-14bc-4bfe-94dd-16dd9945f7d3.h5ad
```

Used here for: the donor-paired synovium-vs-blood disease-direction vector
(activated-memory CD4, 11 paired donors), committed as per-gene aggregate log2FC.

## 3. GSE160097 — external same-disease concordance cohort

| Field | Value |
|---|---|
| Source | DRFZ / Charité Berlin (Maschmeyer, Mashreghi, Radbruch et al.) |
| Publication | Maschmeyer et al., *Eur J Immunol* 2021;51(4):915-929 (PMID 33296081; DOI 10.1002/eji.202048797) |
| Accession | [GEO GSE160097](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160097) |
| Data type | 10x scRNA-seq of FACS-sorted memory CD4 Tcon/Treg (+ CD8), paired synovial fluid & blood |
| Registration | Not required (public GEO) |
| License | **Not explicitly stated** (GEO deposit); raw **not** redistributed here |

Per-sample 10x H5 (raw UMI) download route and per-file **sha256** are in
[EXTERNAL_CONCORDANCE_GSE160097.md](EXTERNAL_CONCORDANCE_GSE160097.md); rebuild with
`python -m perturbgate.external.gse160097 --download`. Base URL:
`https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM4859nnn/<GSM>/suppl/<file>`.

Used here for: the external same-disease **synovial-fluid-minus-blood** memory-CD4
concordance test. Only **derived aggregate summaries** (per-gene disease vector +
six per-donor-pair log2FC) are committed, under
[`results/external_validation/gse160097/`](../results/external_validation/gse160097/).

## Derived data committed in this repository

| File | Derived from | Content | License |
|---|---|---|---|
| `data/demo/disease_vector_activated_memory.tsv.gz` | JIA atlas (2) | per-gene disease log2FC (12,071 genes) | CC-BY-4.0 |
| `data/demo/kd_meta_{RICTOR,PAK2,RIPK1}.tsv.gz` | Perturb-seq (1) | per-gene responder-DE KD log2FC (18,130 genes) | MIT |
| `data/reproduce/pseudobulk_counts.parquet` + meta | Perturb-seq (1) | pseudobulk counts for Level-2 robustness | MIT |
| `data/reproduce/disease_perdonor_logfc_activated_memory.tsv.gz` | JIA atlas (2) | per-donor disease log2FC for LODO | CC-BY-4.0 |
| `results/frozen/*.tsv` | both | aggregate reversal / null / robustness tables | see per-file provenance |

Checksums for all committed derived data are in
[`../data/public_data_manifest.tsv`](../data/public_data_manifest.tsv) and
`results/frozen/results_manifest.json`.

## Uncertainty note

The JIA dataset's per-dataset license field is null in the CELLxGENE curation API;
we rely on the **platform-wide CC-BY-4.0** policy that CELLxGENE applies to all
published datasets (see [DATA_LICENSES.md](DATA_LICENSES.md)). If a future check
finds a stricter per-dataset term, the committed JIA-derived aggregates would need to
be re-evaluated; the download-and-derive route is provided regardless.
