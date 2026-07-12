# PerturbGate

**Evidence-Gated Pipeline for T-cell Perturb-seq Mechanism Hypotheses**

> From 920 perturbations to auditable, evidence-gated mechanism hypotheses.

<!-- Badges become live once the repository is pushed and CI runs. -->
![CI](https://img.shields.io/badge/CI-GitHub_Actions-informational)
![python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![license](https://img.shields.io/badge/code_license-MIT-green)
![data](https://img.shields.io/badge/data-open%20(MIT%20%2B%20CC--BY--4.0)-brightgreen)
![release](https://img.shields.io/badge/release-v1.0--hackathon-orange)

---

PerturbGate is an open-data, reproducible pipeline for turning **T-cell Perturb-seq
hits into evidence-gated mechanism hypotheses**. Built for the challenge to find
new drug targets in a primary human CD4 T-cell Perturb-seq dataset from the
**Marson and Pritchard laboratories**, it combines responder-aware perturbation
effects, guide and donor robustness, donor-paired disease-state reversal,
matched-perturbation calibration, confound testing, and translational safety and
modality gates.

**The goal is not to declare the highest-ranked perturbation a drug target. The
goal is to determine which claims survive explicit attempts to falsify them.**

> **PAK2 passed technical validation but failed therapeutic validation.**
> PerturbGate preserves that distinction: it treats a real perturbation effect as
> *necessary but not sufficient* for target nomination.

---

## Why this project exists

Perturb-seq is powerful for identifying real cellular effects — but a real
cellular effect is not automatically therapeutically useful. PerturbGate separates
four things that are usually collapsed into one ranking:

1. **technical perturbation validity** (is the knockdown real and on-target?)
2. **biological reproducibility** (guides, donors, responders, conditions)
3. **disease directionality** (does it *reverse* a disease state, or mimic it?)
4. **translational readiness** (safety, essentiality, human genetics, modality)

PerturbGate did not succeed because it found a positive hit. It succeeded because
**every retained claim survived an explicit record of how competing claims
failed.**

## What we built

- a reusable **Python package + CLI** (`perturbgate`): disease-reversal scoring,
  matched-perturbation null calibration with finite-pool uncertainty, guide /
  donor / condition / LODO robustness, a pre-specified 8-criterion decision gate,
  candidate attrition, a claim ledger, and code-generated figures;
- **frozen public artifacts** (`results/frozen/`) — 924-perturbation authoritative
  reversal table, candidate funnel, rejection ledger, gate matrix, gate ablation,
  matched-null values, claim registry, superseded-claim registry, analysis
  contract, results manifest;
- **open-data manifests + provenance** with verified accessions and licenses;
- **four main figures + two supplementary**, each with source data (PNG + SVG);
- **three honest reproducibility levels** — `make demo`, `make reproduce`,
  `make full` — plus tests, CI, and an automated privacy / public-readiness audit.

## What we investigated

- which perturbations produce reproducible CD4 T-cell effects;
- whether those effects **reverse** a disease-associated activated-memory state
  (JIA synovium-vs-blood), rather than merely correlating with it;
- whether the surviving signal holds under guide, donor, condition, matched-null
  and confound checks;
- whether the surviving biology has an unresolved safety or modality gap.

## What we found

| Target | Public label | Reversal | Robustness | Decision |
|---|---|---|---|---|
| **RICTOR** | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` | **+0.161** (p=1.8e-63) | both guides +; **11/11** disease-donor LODO +; all 3 conditions +; matched percentile 96.5 | **Retained** mechanism hypothesis — *not* a validated target |
| **PAK2** | `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` | +0.010 (p=0.297, n.s.) | technically real & reproducible, but external JIA enrichment activation-confounded | **Rejected** |
| **RIPK1** | `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` | +0.038 (incoherent) | comparator only | Not supported by this test |

RICTOR's matched-null evidence is **nominal but statistically marginal**: only 200
matched controls exist, 7 of which exceed RICTOR (empirical p ≈ 0.040; finite-pool
95% CI extends to ≈ 0.07). We therefore retain RICTOR as a **mechanism node**, and
name the borderline explicitly rather than reporting "8/8 decisive criteria".

## Target attrition

![Target attrition through evidence gates](figures/figure_1_target_attrition.png)

### How candidates were eliminated

PerturbGate does not treat ranking as validation. Candidates pass through evidence
gates for measurable perturbation effects, guide and donor reproducibility,
responder support, disease directionality, matched-perturbation calibration,
confound resistance, and translational safety and modality. Candidates are
**retained, downgraded, not advanced, or rejected with an explicit reason**. The
full decision trail is the [rejection ledger](results/frozen/rejection_ledger.tsv)
and [candidate funnel](results/frozen/candidate_funnel.tsv); see
[DECISION_TRAIL.md](docs/DECISION_TRAIL.md).

## Why the negative results matter

PAK2 was **not** discarded because its perturbation failed. It was discarded
because the perturbation was real but **not therapeutically directional**. PAK2
passed technical validation but failed therapeutic validation — and PerturbGate
preserves that distinction. Negative results, detected confounds, and superseded
interpretations are first-class, auditable outputs
([SUPERSEDED_RESULTS.md](docs/SUPERSEDED_RESULTS.md),
[FAILURE_MODES.md](docs/FAILURE_MODES.md)).

## Main directional validation

![RICTOR directionality and matched-null calibration](figures/figure_2_directionality_and_null.png)

We report two RICTOR reversal numbers and never mix them silently:

- **+0.161** — the *primary responder-resolved* full-transcriptome reversal;
- **+0.131** — the *conservative all-cell null-substrate projection*, used only to
  calibrate against the matched-perturbation null in the same space.

The difference is a documented representation effect
([Methods](docs/METHODS.md), [Analysis contract](docs/ANALYSIS_CONTRACT.md)).

## Gate matrix

![Gate matrix](figures/figure_3_gate_matrix.png)

The matrix separates **biological evidence** from **translational readiness**: a
row can PASS every biological gate and still carry a `TRANSLATIONAL_GAP` in
modality (RICTOR), or PASS technical gates and FAIL directionality (PAK2).

## PAK2 case study

![PAK2 rejection case study](figures/figure_4_pak2_rejection.png)

PAK2 is the strongest demonstration that the pipeline can distinguish **technical
validity** from **therapeutic relevance**: strong on-target knockdown, guide and
donor reproducibility, a real responder population and a reproducible programme —
followed by no disease-state restoration, an activation-confounded external
enrichment, unestablished partial inhibition, and no safer druggable escape.

## What the pipeline caught

The audit layer detected analytical failure modes that could otherwise have
produced an overclaimed target nomination — unsigned enrichment mistaken for
reversal, biological residency removed as a nuisance, a gene-ID namespace
mismatch, broad transcriptional effects mimicking reversal, repeated Monte-Carlo
draws mistaken for independent controls, and same-cohort sensitivity mistaken for
independent replication. See [FAILURE_MODES.md](docs/FAILURE_MODES.md).

## What we do **not** claim

> - that RICTOR is a **validated drug target**;
> - that systemic RICTOR inhibition is **safe**;
> - that a **selective RICTOR modality** currently exists;
> - that synovium-vs-blood is equivalent to disease-vs-healthy tissue;
> - that the adjusted-vector sensitivity analysis is **independent biological replication**;
> - that PAK2 is an **anti-inflammatory target**;
> - that **all 924 perturbations** underwent deep candidate validation;
> - that the **nominal matched-null significance** is definitive.

## Reproduction

```bash
git clone <PUBLIC_URL>
cd perturbgate-perturbseq

make setup     # install the package (+ dev tools)
make demo      # Level 1: recompute the headline reversal from compact inputs (< 2 min)
make verify    # schemas + golden values + claims + funnel + superseded guard + audit
```

For analytical reproduction and full server-scale reproduction:

```bash
make reproduce # Level 2: recompute robustness from public derived matrices (< 5 min)
make full      # Level 3: reconstruct from open raw data (server-scale; see below)
```

No `make`? Every target is a plain command, e.g. `python -m perturbgate.cli demo`
(see [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)).

## Reproducibility levels (honest)

| Level | Command | Needs | Time | What it proves |
|---|---|---|---|---|
| **1 Demo** | `make demo` | laptop, committed compact inputs | < 2 min | recomputes RICTOR **+0.161** (and PAK2/RIPK1) from per-gene vectors; regenerates tables + figures; validates golden values |
| **2 Analytical** | `make reproduce` | committed pseudobulk matrices | < 5 min | recomputes guide + disease-donor LODO robustness; compares to frozen |
| **3 Full open-data** | `make full` | open raw data, high-memory server | hours | rebuilds the disease vector + genome-scale effect vectors and reruns everything |

Level 1 is **artifact reproducibility**, not end-to-end raw-data reproduction —
see [REPRODUCIBILITY_LEVELS.md](docs/REPRODUCIBILITY_LEVELS.md).

## Open data

Both datasets are open. Derived per-gene aggregate vectors are redistributed here
with attribution; no single-cell or controlled-access data is required for the
demo, reproduction, CI, or the central figures.

- [Public data manifest](data/public_data_manifest.tsv)
- [Open-data statement](docs/OPEN_DATA_STATEMENT.md) ·
  [Data availability](docs/DATA_AVAILABILITY.md) ·
  [Data licenses](docs/DATA_LICENSES.md)
- Primary Perturb-seq: Zhu, Dann, … Pritchard & Marson, bioRxiv 2025
  (DOI [10.64898/2025.12.23.696273](https://doi.org/10.64898/2025.12.23.696273), MIT).
- JIA synovial atlas: Knight et al., bioRxiv 2026
  (DOI [10.64898/2026.05.01.716870](https://doi.org/10.64898/2026.05.01.716870), CC-BY-4.0).

## Claude usage

Claude Code implemented, debugged, tested, packaged and audited the pipeline;
Claude Science red-teamed the hypotheses, surfaced confounds, and scouted the
translational literature. **Claude mattered most when the initial hypothesis
failed** — designing stricter falsification tests and preventing an attractive
cellular hit from becoming an unsupported target claim. AI output is never
presented as evidence. See [CLAUDE_USAGE.md](docs/CLAUDE_USAGE.md).

## Limitations

The matched-null margin is thin (finite pool of 200); synovium-vs-blood is a
disease *surrogate*, not disease-vs-healthy tissue; the adjusted-vector analysis
is same-cohort sensitivity, not independent replication; RICTOR's modality,
safety and human-genetic direction are unresolved. Full list in
[LIMITATIONS.md](docs/LIMITATIONS.md).

## Ongoing study and manuscript plan

This repository is the **frozen hackathon release** of an ongoing study. We plan
to extend it with independent same-tissue disease validation, partial-inhibition
/ titration analyses, deeper translational safety and modality assessment, and,
where feasible, experimental validation — intended to form the basis of a full
scientific manuscript. Future analyses will be versioned separately and will
**not** silently alter the frozen hackathon conclusions
([MANUSCRIPT_ROADMAP.md](docs/MANUSCRIPT_ROADMAP.md)).

## Citation and acknowledgements

Please cite this repository ([CITATION.cff](CITATION.cff)) and the two upstream
datasets ([NOTICE](NOTICE)). We thank the **Marson and Pritchard laboratories**
and the CZI Virtual Cells Platform for the Perturb-seq data; the **Knight et al.**
and **Bolton/Mahony et al.** teams and CZ CELLxGENE for the JIA synovial atlas;
the maintainers of NumPy, pandas, SciPy, Matplotlib and PyArrow; and the
organizers of *Built with Claude: Life Sciences* (Anthropic × Gladstone
Institutes).

---

*Documentation index:* [Methods](docs/METHODS.md) ·
[Results](docs/RESULTS.md) · [Decision trail](docs/DECISION_TRAIL.md) ·
[Failure modes](docs/FAILURE_MODES.md) · [Claims & evidence](docs/CLAIMS_AND_EVIDENCE.md) ·
[Superseded results](docs/SUPERSEDED_RESULTS.md) · [Analysis contract](docs/ANALYSIS_CONTRACT.md) ·
[Technical note](docs/TECHNICAL_NOTE.md) · [Reproducibility](docs/REPRODUCIBILITY.md) ·
[Translational context](docs/TRANSLATIONAL_CONTEXT.md) · [Hackathon submission](docs/HACKATHON_SUBMISSION.md) ·
[Explorer](reports/perturbgate_explorer.html)
