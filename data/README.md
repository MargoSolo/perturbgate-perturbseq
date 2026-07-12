# data/

Open, derived, redistributable inputs. **No raw single-cell data and no
controlled-access data live here** — only compact per-gene aggregate statistics
derived from the two open datasets (see
[`public_data_manifest.tsv`](public_data_manifest.tsv) and
[`../docs/DATA_LICENSES.md`](../docs/DATA_LICENSES.md)).

```
data/
├── public_data_manifest.tsv                     machine-readable provenance + checksums
├── schemas/                                      JSON schemas for the committed tables
├── demo/                                         Level-1 inputs (laptop, minutes)
│   ├── disease_vector_activated_memory.tsv.gz    JIA disease log2FC, 12,071 genes (CC-BY-4.0)
│   └── kd_meta_{RICTOR,PAK2,RIPK1}.tsv.gz         responder-DE KD log2FC, 18,130 genes (MIT)
├── reproduce/                                     Level-2 inputs (public derived matrices)
│   ├── pseudobulk_counts.parquet                 pseudobulk counts (MIT)
│   ├── pseudobulk_meta.tsv                        pseudobulk metadata
│   └── disease_perdonor_logfc_activated_memory.tsv.gz   per-donor disease log2FC for LODO (CC-BY-4.0)
└── full/                                          Level-3 downloads land here (gitignored)
```

- **demo/** is all `make demo` needs. It recomputes the RICTOR/PAK2/RIPK1 disease
  reversal from per-gene vectors and validates the headline values.
- **reproduce/** lets `make reproduce` recompute guide + leave-one-disease-donor-out
  robustness from pseudobulk counts.
- **full/** is empty and gitignored; `python scripts/download_open_data.py` populates
  it from the public sources for Level-3 reconstruction.

Every file's upstream source, license, redistribution status and checksum is in
[`public_data_manifest.tsv`](public_data_manifest.tsv).
