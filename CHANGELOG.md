# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/) and the project uses
[semantic versioning](https://semver.org/).

## [1.0.0] — 2026-07-13 — Frozen hackathon release

First public, open-data release, built for *Built with Claude: Life Sciences*
(Research track).

### Added
- Reusable `targetgate` Python package: disease-state reversal scoring,
  matched-perturbation null calibration with finite-pool uncertainty, guide /
  donor / condition / LODO robustness, the pre-specified 8-criterion decision
  gate, candidate attrition, claim ledger and code-generated figures.
- Frozen public artifacts (`results/frozen/`): primary comparison,
  all-perturbation authoritative reversal (924 perturbations), candidate funnel,
  rejection ledger, gate matrix, gate ablation, matched-null values, confound
  decomposition, safety summary, claims, superseded claims, analysis contract,
  results manifest.
- Three honest reproducibility levels: `make demo` (Level 1, laptop, minutes),
  `make reproduce` (Level 2, public derived matrices), `make full` (Level 3,
  open-data reconstruction, server-scale).
- Four main figures + two supplementary figures, each with source data, PNG+SVG.
- Documentation set (methods, results, decision trail, failure modes, superseded
  results, open-data statement, data availability/licenses, claims and evidence,
  reproducibility, technical note, manuscript roadmap, Claude usage).
- Tests, continuous integration, and an automated public-readiness / privacy
  audit.

### Scientific conclusions (frozen)
- **PAK2**: `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` — a real,
  reproducible CD4 T-cell perturbation hit that does not reverse the disease
  state (+0.010, p=0.297); apparent external JIA enrichment is
  activation-confounded; partial inhibition not established; **rejected**.
- **RICTOR**: `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` — reverses the
  corrected activated-memory JIA synovium-vs-blood direction at +0.161; both
  guides positive; 11/11 disease-donor LODO positive; positive in all three
  conditions; confound-resistant. Matched-null significance is nominal but
  finite-pool uncertainty extends to ~0.07. Retained as a mechanism hypothesis,
  **not** a validated drug target.
- **RIPK1**: `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS`.

### Superseded (never presented as current findings)
- The old RICTOR reversal of ~+0.43 (see `docs/SUPERSEDED_RESULTS.md`).
- Unsigned PAK2 JIA enrichment as disease support.
- PAK2 partial-inhibition support; a "safer PAK2 neighbour"; PAK2–WASF2 as a
  therapeutic axis.
