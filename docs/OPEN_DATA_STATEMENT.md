# Open-data statement

TargetGate depends only on **open data**. No proprietary dataset, hidden API,
private connector, or credential is a required dependency of the demo, the
analytical reproduction, continuous integration, or the central public figures.

## The two primary datasets

1. **Primary Human CD4+ T Cell Perturb-seq** — Marson lab (Gladstone/UCSF) and
   Pritchard lab (Stanford), on the CZI Virtual Cells Platform. bioRxiv DOI
   [10.64898/2025.12.23.696273](https://doi.org/10.64898/2025.12.23.696273).
   Processed data are anonymously downloadable (no registration) from the public S3
   bucket `s3://genome-scale-tcell-perturb-seq/`; raw sequencing is public (GEO
   GSE314342 / SRA SRP643211). **License: MIT.**

2. **JIA synovial single-cell atlas ("Integrated global cells")** — Knight et al.,
   bioRxiv DOI [10.64898/2026.05.01.716870](https://doi.org/10.64898/2026.05.01.716870),
   with the synovial-tissue layer from Bolton/Mahony et al., *Sci Transl Med* 2025,
   DOI [10.1126/scitranslmed.adt6050](https://doi.org/10.1126/scitranslmed.adt6050).
   CZ CELLxGENE Discover collection `10eb236d-d42d-45b8-8363-c2dcf865f388`, fully
   open, no registration. **License: CC-BY-4.0** (CELLxGENE platform-wide).

## What this repository redistributes

Only **derived, per-gene aggregate statistics** — log2 fold changes, correlations,
ranks — are committed here (`data/demo/`, `data/reproduce/`, `results/frozen/`). No
single-cell matrices and no donor-identifiable data are included. Redistribution of
these derivatives is permitted:

- Perturb-seq derivatives under **MIT** (with attribution and the CZI Virtual Cell
  Models Acceptable Use Policy);
- JIA derivatives under **CC-BY-4.0** (with attribution to the original contributors).

This project does **not** relicense upstream data; derived-data redistribution
follows the source terms. Literature and database content are **cited, not
republished**. AI-produced literature reports are working notes, not evidence: every
public biological or translational statement resolves to a primary paper, official
database, or data artifact.

## Controlled access

No controlled-access dataset is required for `make demo`, `make reproduce`, CI, or
the central figures. Full raw-data reconstruction (`make full`) reads only the public
sources above.

See [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) for exact download routes,
[DATA_LICENSES.md](DATA_LICENSES.md) for license verification, and
[`../data/public_data_manifest.tsv`](../data/public_data_manifest.tsv) for the
machine-readable manifest with checksums.
