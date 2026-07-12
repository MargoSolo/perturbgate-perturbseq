# Reproducibility levels

PerturbGate ships three nested, honestly-scoped reproduction paths. Each is a
different contract: a different set of inputs, a different amount of compute, and
a different subset of results that is actually recomputed rather than read from
the frozen release. We keep them separate on purpose. A claim that a laptop
reproduces the entire genome-scale pipeline would be false; a claim that nothing
is reproducible without a server would be equally false. The three levels state
exactly where the boundary is.

This matters because the central result of PerturbGate is not a single positive
hit — it is an auditable record of *how competing claims failed*. A real
perturbation effect is necessary but not sufficient for target nomination, so the
value of the release is that every retained and every rejected claim resolves to a
committed artifact. Reproducibility here means being able to regenerate those
artifacts and re-derive the decision, at whatever depth your hardware allows.

All three levels are driven from the [Makefile](../Makefile) and also run as plain
commands for users without `make`. Every level uses `seed: 0`. Golden values,
schemas and forbidden-term audits are enforced by `make verify`.

| Level | Command | What it recomputes | Inputs | RAM | Runtime | Storage | Server | Tolerance vs frozen |
|------|---------|--------------------|--------|-----|---------|---------|--------|---------------------|
| 1 — demo | `make demo` | RICTOR/PAK2/RIPK1 disease-state reversal; regenerates tables + figures; validates headline golden values | `data/demo/*.tsv.gz` (committed, ~0.2 MB each) | ~2 GB | < 2 min | negligible | no | 1e-3 |
| 2 — analytical reproduction | `make reproduce` | RICTOR guide-separate reversal and leave-one-disease-donor-out robustness from committed pseudobulk | `data/reproduce/` (pseudobulk parquet ~15 MB) + `data/demo/` | ~4 GB | < 5 min | ~20 MB | no | 5e-3 |
| 3 — full open-data | `make full` | disease vector, genome-scale effect vectors, functional table, then all scoring / robustness / null / figures | open JIA h5ad + primary Perturb-seq (downloaded) | ~128 GB | several hours | ~60 GB | yes (high-memory) | verify against frozen |

---

## Level 1 — demo (artifact reproducibility)

**Command:** `make demo` (equivalently `python -m perturbgate.cli demo`).
**Config:** [`configs/demo.yaml`](../configs/demo.yaml).

**What it recomputes.** Level 1 recomputes the headline disease-state reversal for
the three comparison targets directly from compact, legally redistributable
per-gene vectors, then regenerates the public tables, the claim ledger and all
figures, and validates the recomputed headline numbers against the frozen golden
values within a tolerance of `1e-3`.

**Inputs (all committed, no download, no credentials):**

- `data/demo/disease_vector_activated_memory.tsv.gz` — the JIA
  synovium-vs-blood activated-memory CD4 disease-direction vector
  (md5 `2b18d92684db1f70b637e1f098374c7e`; 12071 genes; derived, CC-BY-4.0).
- `data/demo/kd_meta_{RICTOR,PAK2,RIPK1}.tsv.gz` — per-gene responder-DE
  knockdown log2FC vectors (derived, MIT).
- `results/frozen/rictor_matched_null_values.tsv` — the pre-computed 200-member
  matched-null distribution, so the demo can position RICTOR against it without
  rebuilding the genome-scale substrate.

**Outputs:** `results/demo/reversal_recomputed.tsv`,
`results/demo/matched_null_recomputed.json`, `results/demo/demo_summary.json`, and
`figures/*.png` / `figures/*.svg` (for example
`figure_1_target_attrition`, `figure_2_directionality_and_null`,
`figure_3_gate_matrix`, `figure_4_pak2_rejection`).

**Headline values this level reproduces** (authoritative, from
[`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv)):
RICTOR responder-resolved reversal **+0.161** (centered-Pearson, ~10832 aligned
genes); PAK2 **+0.010** (not significant, p = 0.297); RIPK1 **+0.038** (weak and
incoherent, both GSEA NES negative). The matched-null positioning it reproduces:
RICTOR **7 of 200** matched perturbations exceed the observed reversal, empirical
p = 0.0398, Wilson 95% CI (0.017, 0.070), percentile 96.5 (global 97.9); PAK2 41st
and RIPK1 42nd percentile.

**Resources:** ~2 GB RAM, under two minutes, ordinary laptop, no server, no
private data.

**Not recomputed at Level 1.** The matched-null distribution is *read* from the
frozen values, not regenerated (regeneration is a Level-3 server task); guide and
leave-one-donor-out robustness are the subject of Level 2.

---

## Level 2 — analytical reproduction

**Command:** `make reproduce` (equivalently `python -m perturbgate.cli reproduce`).
**Config:** [`configs/reproduce.yaml`](../configs/reproduce.yaml).

**What it recomputes.** Level 2 goes one layer deeper than the demo: it recomputes
the two decision-critical RICTOR robustness axes — guide-separate reversal and
leave-one-disease-donor-out (LODO) — from the committed donor-paired pseudobulk,
then compares them to the frozen tables with a documented floating-point tolerance
of `5e-3`.

**Inputs (all committed):**

- `data/reproduce/pseudobulk_counts.parquet` (~15 MB) and
  `data/reproduce/pseudobulk_meta.tsv` — donor-paired raw-count pseudobulk.
- `data/reproduce/disease_perdonor_logfc_activated_memory.tsv.gz` — per-donor
  disease log2FC used for LODO folds.
- `data/demo/disease_vector_activated_memory.tsv.gz` and
  `data/demo/kd_meta_RICTOR.tsv.gz`.

**Outputs:** `results/reproduced/rictor_guides.tsv` and
`results/reproduced/rictor_lodo.tsv`, compared against
[`results/frozen/rictor_guides.tsv`](../results/frozen/rictor_guides.tsv) and
`rictor_lodo.tsv`.

**Values this level reproduces:** both RICTOR guides positive (RICTOR-1 +0.141,
RICTOR-2 +0.178) and all 11 of 11 disease-donor LODO folds positive
(band +0.154..+0.167).

**Resources:** ~4 GB RAM, under five minutes, no server.

### What is honestly NOT reproduced at Level 2

Level 2 deliberately does not reconstruct two axes, because each needs an input
that is not shipped at this level (see `not_reproduced_here` in
[`configs/reproduce.yaml`](../configs/reproduce.yaml)):

- **Condition-level reversal** (Rest +0.153, Stim8hr +0.092, Stim48hr +0.042)
  is not recomputed here — it requires the per-condition responder-DE meta
  vectors, which are not among the Level-2 committed matrices.
- **The matched-perturbation null** (the finite-pool calibration behind
  criterion 8) is not recomputed here — it requires the genome-scale
  effect-vector substrate (~124 MB), which is a Level-3 server build, not a
  committed Level-2 input.

At Level 2 those two results remain sourced from the frozen release; only guide
and LODO robustness are actually re-derived. This is why RICTOR's overall standing
is stated as **seven strong convergence checks plus a matched-perturbation null it
nominally exceeded, with borderline finite-pool uncertainty** — Level 2 verifies
the strong convergence checks that it can recompute, and does not silently claim
to have re-derived the weakest (criterion 8) axis.

---

## Level 3 — full open-data reconstruction

**Command:** `make full` (equivalently `python scripts/run_full_pipeline.py`).
**Config:** [`configs/full.yaml`](../configs/full.yaml).
**Download helper:** `python scripts/download_open_data.py` (add `--execute` for
the compact route).

**What it recomputes.** Level 3 reconstructs the analysis from the two open
primary datasets, then reruns everything:

1. Download the open data — the JIA synovial atlas h5ad from CZ CELLxGENE
   (collection `10eb236d-d42d-45b8-8363-c2dcf865f388`, CC-BY-4.0, ~1–2 GB, no
   registration) and the primary Human CD4+ T-cell Perturb-seq processed release
   from the CZI Virtual Cell Models anonymous S3 (`s3://genome-scale-tcell-perturb-seq/`,
   MIT; raw at GEO GSE314342 / SRA SRP643211).
2. Rebuild the donor-paired raw-count disease vector, the genome-scale effect
   vectors, and the functional table.
3. Rerun scoring, guide/donor/condition robustness, matched-null calibration and
   figure generation, and verify the reconstruction against the frozen artifacts.

Server roots are supplied through the `SERVER_DATA_ROOT` and
`SERVER_RESULTS_ROOT` environment variables; there are no hardcoded paths. If those
roots are not configured, `make full` prints exactly what is needed and exits
without pretending a laptop can do the work.

**Stages that are genuinely server-scale** (from `configs/full.yaml`):

- building the disease vector from the JIA h5ad (raw-count donor-paired pseudobulk
  across the 11 paired disease donors);
- building the genome-scale effect vectors (knockdown-vs-control log2FC per
  perturbation per condition);
- the matched-perturbation null over all perturbations.

**Resources:** ~128 GB RAM, ~16 CPU cores, ~60 GB working storage, several hours,
high-memory server required.

### Honest Level-3 blockers and boundaries

We do not claim that Level 3 reproduces the analysis from raw sequencing.

- **Entry point is processed open data, not FASTQ.** The reconstruction starts
  from the processed CZI VCP objects and the CELLxGENE h5ad. Re-deriving those
  processed objects from raw reads (GEO GSE314342 / SRA SRP643211) is upstream of
  this pipeline and is not part of the reproducibility guarantee.
- **Raw single-cell data is not redistributed in this repository.** Only per-gene
  aggregate derived vectors are committed (`raw_data_in_repo = no` throughout
  [`data/public_data_manifest.tsv`](../data/public_data_manifest.tsv)); Level 3
  rebuilds the larger substrates locally from the public sources under their
  licenses (MIT and CC-BY-4.0, redistribution of derived aggregates permitted with
  attribution).
- **External-source dependency.** Level 3 depends on the continued public
  availability of the anonymous S3 route and the CELLxGENE h5ad. If a required
  processed input cannot be rebuilt from a public source under its license, that
  limitation is stated prominently and Levels 1–2 remain the honest, self-contained
  reproducibility guarantee (`blocked_reproduction_note` in `configs/full.yaml`).
- **Same-cohort, not independent replication.** Reconstruction re-derives the same
  result from the same two cohorts. It is not independent biological replication,
  and the synovium-vs-blood contrast is not disease-vs-healthy. The superseded
  adjusted-vector sensitivity analysis is likewise same-cohort — see
  [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md).

---

## Two substrates — do not mix them

Two reversal substrates appear in the release and must never be silently combined:

- the **primary** responder-resolved donor random-effects meta knockdown vector
  (reversal **+0.161**, ~10832 aligned genes), used for the headline and for the
  strong convergence checks; and
- the **conservative** all-cell effect-vector projection (reversal **+0.131**,
  7393-gene intersection), used *only* to calibrate RICTOR against the
  matched-perturbation null in the same feature space.

The +0.030 gap between them decomposes into −0.036 from the gene universe and
+0.066 from the responder→all-cell representation; the all-cell number is the more
conservative one. Level 1 reports the primary substrate; the matched-null
positioning (Level 1 read, Level 3 recomputed) is in the conservative substrate.
See [METHODS.md](METHODS.md) and
[`results/frozen/confound_decomposition.tsv`](../results/frozen/confound_decomposition.tsv).

---

## What none of these levels claim

Reproducing the pipeline reproduces the *analysis and its decision record*, not a
therapeutic conclusion. Independent of level:

- RICTOR is a
  `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`, **not** a validated drug
  target; systemic RICTOR inhibition is not shown to be safe, and no selective
  small-molecule RICTOR modality currently exists (the modality gap).
- PAK2 is a
  `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` — a real, reproducible
  responder signature that is not disease-directional; it is not an
  anti-inflammatory target.
- RIPK1 is a
  `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS`, included only as a
  benchmark comparator.
- Not all 924 screened perturbations underwent every deep test — the funnel is a
  branching decision map, not a linear pass through all deep gates (see
  [`results/frozen/candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv)).
- The matched-null significance is nominal, not definitive: 7 of 200 matched
  perturbations exceed RICTOR (empirical p = 0.0398, Wilson 95% CI up to ~0.070).

See also: [REPRODUCIBILITY.md](REPRODUCIBILITY.md) (command reference),
[METHODS.md](METHODS.md), [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md),
[DATA_LICENSES.md](DATA_LICENSES.md), and
[SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md).
