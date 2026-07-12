# Reproducibility

This document is the operational guide to re-deriving every public result in
**PerturbGate — Evidence-Gated Pipeline for T-cell Perturb-seq Mechanism
Hypotheses** (version 1.0.0, frozen hackathon release, 2026-07-13). It gives the
exact commands (both the `make` targets and their plain-`python` equivalents),
the measured resource envelope for each level, the golden-value tolerances that
gate a passing run, what `results/frozen/results_manifest.json` records, and how
`verify` prevents a superseded value from silently re-entering the public
outputs.

The pipeline is deliberately layered into three reproducibility levels so that
the central scientific claims can be checked on a laptop in minutes, while the
full server-scale reconstruction remains available and honestly bounded. All
level definitions live in [`configs/demo.yaml`](../configs/demo.yaml),
[`configs/reproduce.yaml`](../configs/reproduce.yaml) and
[`configs/full.yaml`](../configs/full.yaml); the numbers quoted here are read
from those configs and from the frozen artifacts under `results/frozen/`.

For the scientific rationale behind each check, see [Methods](METHODS.md); for
the three-level design and its honest limits, see
[Reproducibility levels](REPRODUCIBILITY_LEVELS.md); for the analysis contract
and controlled vocabulary, see [Analysis contract](ANALYSIS_CONTRACT.md); for
what was corrected and why, see [Superseded results](SUPERSEDED_RESULTS.md).

---

## 1. Quick start

```bash
make setup      # install the package (+ dev tools) in editable mode
make demo       # Level 1: recompute headline reversal from compact inputs (minutes)
make verify     # full gate: schemas + golden values + claims + funnel + superseded guard + tests
```

`make demo` is sufficient to confirm the headline RICTOR/PAK2/RIPK1 result on a
normal laptop with no server access and no private data. `make verify` is the
composite release gate and is what a reviewer should run to certify a checkout.

---

## 2. Commands

The `Makefile` is the primary user interface. Every target is a thin wrapper
around a plain command so the pipeline is fully usable without `make`. The
`Makefile` exports `PYTHONPATH=src`; after `make setup` (an editable install)
the `perturbgate` package is importable directly, so the plain commands below
work from the repository root. If you run from a source checkout **without**
installing, prefix each plain command with `PYTHONPATH=src` (POSIX) or set
`$env:PYTHONPATH="src"` (Windows PowerShell) first.

| Target | `make` command | Plain equivalent | What it does |
| --- | --- | --- | --- |
| Setup | `make setup` | `python -m pip install -e ".[dev]"` | Editable install with dev tools (ruff, pytest). |
| Demo | `make demo` | `python -m perturbgate.cli demo` | Level 1: recompute reversal from `data/demo/*.tsv.gz`, regenerate figures, validate golden values. |
| Reproduce | `make reproduce` | `python -m perturbgate.cli reproduce` | Level 2: recompute guide + LODO robustness from `data/reproduce/`, compare to frozen at 5e-3. |
| Full | `make full` | `python scripts/run_full_pipeline.py` | Level 3: rebuild from open raw data (server-scale). |
| Figures | `make figures` | `python -m perturbgate.cli figures` | Regenerate all figures (`.png` + `.svg`) and their source-data TSVs. |
| Manifest | `make manifest` | `python -m perturbgate.cli manifest` | Rewrite `results/frozen/results_manifest.json` (sha256 checksums). |
| Verify | `make verify` | see composite below | Schemas + golden + claims + funnel + superseded guard + tests + audit. |
| Test | `make test` | `pytest` | Run the test suite. |
| Lint | `make lint` | `ruff check src scripts tests` | Static checks. |

### The composite `verify` gate

`make verify` runs, in order:

```bash
python -m perturbgate.cli demo        # regenerate demo outputs (also runs golden checks)
python -m perturbgate.cli figures     # regenerate all figures + source data
python -m perturbgate.cli manifest    # rewrite the checksum manifest
python -m perturbgate.cli verify      # schemas + golden + claims + funnel + superseded guard
pytest -q                            # test suite
python scripts/public_readiness_audit.py   # scan for private/superseded/forbidden content
```

`make release-check` runs `lint` then `verify` and is the gate required before
public approval.

---

## 3. Reproducibility levels and measured resource needs

Each level is self-describing in its config file (`level`, `inputs`, `outputs`,
`tolerance`, `seed`, `resources`). The resource figures below are the declared,
measured envelopes from those configs. The global random seed is `0` at every
level.

### Level 1 — `make demo` (artifact reproduction)

Runs on a normal laptop in minutes, with no server, no private data and no
credentials. It recomputes the RICTOR/PAK2/RIPK1 disease-state reversal from
compact, legally redistributable inputs (`data/demo/*.tsv.gz`), regenerates the
public tables and figures, and validates the headline values against the frozen
golden numbers.

- **Inputs:** `data/demo/disease_vector_activated_memory.tsv.gz`,
  `data/demo/kd_meta_{RICTOR,PAK2,RIPK1}.tsv.gz`, and the frozen matched-null
  values `results/frozen/rictor_matched_null_values.tsv`.
- **Outputs:** `results/demo/reversal_recomputed.tsv`,
  `results/demo/matched_null_recomputed.json`,
  `results/demo/demo_summary.json`, and all `figures/*.png` / `figures/*.svg`.
- **Tolerance:** `1.0e-3` (absolute, `|recomputed − frozen golden|`).
- **Resources (measured):** ~2 GB RAM, runtime < 2 minutes, no server.

### Level 2 — `make reproduce` (analytical reproduction)

Recomputes the decision-critical RICTOR robustness axes — guide-separate
reversal and leave-one-disease-donor-out (LODO) — from the shipped Level-2
derived matrices, then compares to the frozen tables with a documented
floating-point tolerance.

- **Inputs:** `data/reproduce/pseudobulk_counts.parquet`,
  `data/reproduce/pseudobulk_meta.tsv`,
  `data/reproduce/disease_perdonor_logfc_activated_memory.tsv.gz`, plus the
  demo disease vector and RICTOR KD meta.
- **Outputs:** `results/reproduced/rictor_guides.tsv`,
  `results/reproduced/rictor_lodo.tsv`.
- **Compared to:** `results/frozen/rictor_guides.tsv`.
- **Tolerance:** `5.0e-3` (absolute, per-guide reversal).
- **Resources (measured):** ~4 GB RAM, runtime < 5 minutes, no server.
- **Not reproduced at this level (documented honestly in the config):** the
  per-condition split needs the per-condition responder-DE meta vectors, and the
  matched-perturbation null needs the genome-scale effect-vector substrate
  (~124 MB). Both are Level-3 inputs.

### Level 3 — `make full` (full open-data reproduction)

Reconstructs the analysis from the open primary data: the JIA synovial atlas
(CZ CELLxGENE) and the primary human CD4+ T-cell Perturb-seq release. It
verifies checksums, rebuilds the donor-paired disease vector and the
genome-scale effect vectors, and reruns scoring, robustness, null calibration
and figures. This is server-scale and may take hours.

- **Open data (public, no registration for the processed routes):**
  - Primary Human CD4+ T Cell Perturb-seq (Marson lab + Pritchard lab),
    DOI `10.64898/2025.12.23.696273`; processed
    `s3://genome-scale-tcell-perturb-seq/marson2025_data/`; raw GEO `GSE314342`
    / SRA `SRP643211`; License MIT (redistribution permitted with attribution).
  - JIA synovial single-cell atlas "Integrated global cells", DOI
    `10.64898/2026.05.01.716870`; CZ CELLxGENE collection
    `10eb236d-d42d-45b8-8363-c2dcf865f388`; License CC-BY-4.0. Fully open, no
    registration.
- **Server-scale stages:** building the disease vector from the JIA h5ad
  (raw-count donor-paired pseudobulk); building the genome-scale effect vectors
  (KD-vs-NTC log2FC per perturbation per condition); and the
  matched-perturbation null over all perturbations.
- **Environment:** configure `SERVER_DATA_ROOT` (the genome-scale effect-vector
  substrate + functional table) and `SERVER_RESULTS_ROOT` (where reconstructed
  results are written) to your own compute environment. No internal paths are
  hardcoded.
- **Resources (declared):** ~128 GB RAM, 16 CPU cores, ~60 GB storage, several
  hours, server required.
- **Honest limitation:** if a required processed input cannot be rebuilt from a
  public source under its license, that limitation is stated prominently and
  Levels 1–2 remain the honest reproducibility guarantee. Derived per-gene
  aggregate vectors are committed to the repository, so Levels 1–2 never depend
  on rebuilding the upstream single-cell data. See
  [Reproducibility levels](REPRODUCIBILITY_LEVELS.md) and
  [`data/public_data_manifest.tsv`](../data/public_data_manifest.tsv).

---

## 4. Golden values and tolerances

The frozen headline values ("golden values") are held in `src/perturbgate` and
sourced from `results/frozen/`. `make demo` and `make verify` recompute each
value from the compact committed inputs and require the recomputed number to
fall within the level tolerance of the golden value. A mismatch fails the run.

- **Demo / verify tolerance:** `1e-3` (absolute).
- **Reproduce tolerance:** `5e-3` (absolute, per-guide reversal).

The golden values checked on every demo/verify run (all recomputed from
`data/demo/` inputs, seed `0`):

| Quantity | Golden value |
| --- | --- |
| RICTOR reversal (centered-Pearson, primary responder-resolved) | +0.1606 |
| RICTOR reversal (Spearman) | +0.100 |
| RICTOR aligned genes | 10832 |
| PAK2 reversal (centered-Pearson) | +0.010 |
| RIPK1 reversal (centered-Pearson) | +0.038 |
| RICTOR matched-null observed (conservative all-cell substrate) | +0.1314 |
| RICTOR matched-null exceedances / pool | 7 / 200 |
| RICTOR matched-null empirical p | 0.0398 |

Two points of scientific hygiene are enforced by the numbers above and must not
be blurred:

1. **Two substrates, never silently mixed.** The RICTOR reversal golden value
   (+0.161, 10832 aligned genes) is the **primary responder-resolved** donor
   random-effects meta KD vector. The matched-null observed value (+0.131,
   7393-gene intersection) is the **conservative all-cell effect-vector
   projection**, used *only* to calibrate RICTOR against the matched-perturbation
   null in the same feature space. The +0.030 difference decomposes into −0.036
   from the gene universe and +0.066 from the responder→all-cell representation;
   the all-cell number is the conservative one. Responder-resolved scores are
   never compared against all-cell null-substrate scores.

2. **The matched-null is the weakest criterion.** RICTOR was evaluated against
   eight pre-specified criteria fixed before the raw-count result was viewed
   (centered-Pearson reversal > 0; Spearman reversal > 0; ranked-GSEA same
   direction; both guides positive; all 11 disease-donor LODO folds positive;
   responder-only support; positive in all three conditions; and above the
   matched-perturbation null at the frozen point estimate). Criterion 8 is the
   most marginal: of 200 matched controls, 7 exceed RICTOR (empirical
   p ≈ 0.040, Wilson 95% CI up to ~0.070). The correct summary is that **RICTOR
   satisfied seven strong convergence checks and nominally exceeded a
   matched-perturbation null, with borderline finite-pool uncertainty** — not
   "8/8 decisive criteria".

The supporting robustness numbers regenerated at Level 2 are the guide reversals
(+0.141 for RICTOR-1, +0.178 for RICTOR-2, both positive) and the 11/11 positive
disease-donor LODO folds (band +0.154..+0.167). The per-condition values
(Rest +0.153, Stim8hr +0.092, Stim48hr +0.042) require Level-3 inputs.

---

## 5. Provenance and the results manifest

`results/frozen/results_manifest.json` is the checksum index for the frozen
release. It is rewritten by `make manifest` (or `python -m perturbgate.cli
manifest`) and records:

- **`version`** — the release version (`1.0.0`).
- **`frozen`** — the **sha256** content hash of every frozen artifact under
  `results/frozen/` (every `*.tsv` and `*.json`).
- **`demo_inputs`** — the **sha256** of every compact demo input under
  `data/demo/` (the gzipped disease vector and the three KD meta vectors).

These hashes let any consumer, and the release audit, detect drift in a frozen
table or a demo input. The remaining provenance dimensions the task's four-part
record (**sha256, source, command, checksums**) refers to are captured across
three coordinated artifacts:

- **sha256** of artifacts and demo inputs → `results/frozen/results_manifest.json`.
- **Generating command** and **input checksums** per scientific claim →
  `results/frozen/claims.json`. Every claim carries its
  `generating_command` (e.g. `perturbgate demo && perturbgate verify`), its
  `code_version` (`1.0.0`), and the `input_checksums` it depends on — notably
  the disease-vector md5 `2b18d92684db1f70b637e1f098374c7e`.
- **Upstream source**, license and retrieval command per dataset →
  [`data/public_data_manifest.tsv`](../data/public_data_manifest.tsv), which
  maps each dataset to its accession, DOI, license, redistribution status and
  exact retrieval command.

Together these give a closed provenance chain: each public number resolves to a
frozen artifact (hashed in the manifest), each artifact to a generating command
and code version (in the claim ledger), and each input to a licensed public
source (in the data manifest). `verify` step 3 additionally checks that every
claim in `claims.json` resolves to an on-disk supporting artifact.

---

## 6. How `verify` guards against superseded values

The pipeline preserves negative and corrected results as first-class outputs
(see [`results/frozen/superseded_claims.json`](../results/frozen/superseded_claims.json)
and [Superseded results](SUPERSEDED_RESULTS.md)). To make sure a corrected value
can never quietly return to the public tables, `make verify` runs an explicit
superseded guard in addition to the golden-value checks:

1. **Golden guard (in the demo/verify golden check).** After recomputing the
   RICTOR reversal, the run asserts it is *not* within 0.05 of the superseded
   `+0.43`. That old figure came from an inflated covariate-adjusted /
   residency-removed 77-gene subset (SUP-01) and was replaced by the primary
   +0.161 and the conservative +0.131. If a recomputed RICTOR reversal ever
   matched +0.43, the run fails with an explicit "matches the SUPERSEDED +0.43"
   error.

2. **Frozen-table guard.** `verify` re-reads
   `results/frozen/primary_comparison.tsv` and fails if the RICTOR
   `primary_reversal` is within 0.05 of +0.43.

3. **Vocabulary guard.** `verify` loads `superseded_claims.json` and fails if any
   superseded entry is marked `may_appear_in_readme=true` (all five entries
   SUP-01..SUP-05 are marked `false`). This keeps the retired PAK2 claims — the
   activation-confounded JIA enrichment (SUP-02), the unestablished
   partial-inhibition axis (SUP-03), the "safer neighbour" search (SUP-04) and
   the PAK2–WASF2 axis (SUP-05) — out of public-facing text.

4. **Label guard.** The public decision labels are restricted to the controlled
   vocabulary — `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`,
   `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL`, and
   `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` — and `verify`
   checks schemas, the candidate-funnel denominators and the rejection-ledger
   vocabulary against these.

Finally, `scripts/public_readiness_audit.py` (run inside `make verify` and as
`make privacy-audit`) scans the whole repository for forbidden private or
superseded content before public approval.

---

## 7. Figures

`make figures` (or `python -m perturbgate.cli figures`) regenerates the full
figure set as both `.png` and `.svg`, each with a committed source-data TSV under
`figures/source_data/`:

- `figure_1_target_attrition` — the branching candidate-attrition map.
- `figure_2_directionality_and_null` — reversal directionality and the
  matched-perturbation null.
- `figure_3_gate_matrix` — the decision-gate matrix.
- `figure_4_pak2_rejection` — the PAK2 technical-pass / therapeutic-fail
  contrast.
- `supplementary_gate_ablation` — gate ablation.
- `supplementary_rictor_robustness` — RICTOR guide / condition / LODO
  robustness.

The attrition counts shown in Figure 1 are a branching decision map, not a
linear funnel: 924 perturbations were scored at screen level; 208 were
convergent and FDR < 0.10; 21 were biologically robust; 0 were advanceable from
the single-state screen (the 21 were safety/modality constrained →
`NO_ROBUST_CANDIDATE`). Separately, the deep candidate branch carried PAK2
(deep-validated, then rejected), RICTOR (bounded rescue, retained) and RIPK1
(comparator only). Not all 924 perturbations underwent every deep test; all
denominators trace to `results/frozen/candidate_funnel.tsv`,
`results/frozen/rejection_ledger.tsv` and
`results/frozen/all_perturbations_authoritative_reversal.tsv`.

---

## 8. Scope of the reproducibility guarantee

Reproducing these numbers reproduces the **analysis**, not a biological
validation. In particular: RICTOR is retained as a disease-reversing mechanism
*hypothesis* with a modality gap, **not** a validated drug target; systemic
RICTOR inhibition is not shown to be safe and no selective RICTOR modality
currently exists; the JIA disease vector is synovium-vs-blood, which is **not**
disease-vs-healthy; the old-vector sensitivity analysis is same-cohort and is
**not** independent biological replication; PAK2 is a reproducible cellular hit
but **not** an anti-inflammatory target; and the nominal matched-null
significance is not definitive. The pipeline's value is that every retained
claim carries an explicit, checkable record of how competing claims failed —
this is target *nomination* under evidence gating, not gene ranking.
