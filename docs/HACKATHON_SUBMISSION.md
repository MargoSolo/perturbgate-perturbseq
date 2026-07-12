# Hackathon submission — PerturbGate

*Built with Claude: Life Sciences (Anthropic × Gladstone Institutes) — Research track.*
*Challenge: find new drug targets in a primary human CD4 T-cell Perturb-seq dataset
from the Marson and Pritchard laboratories.*

---

## Primary written summary (submission text, ~195 words)

PerturbGate is an open-data, reproducible analysis for converting genome-scale
human CD4 Perturb-seq hits into evidence-gated mechanism hypotheses. Our first
lead, PAK2, produced a real cellular phenotype but failed therapeutic-direction
testing and was rejected. RICTOR survived responder, guide, donor, condition,
confound, and matched-null checks as a disease-reversing mechanism hypothesis.

We then tested the frozen RICTOR signature in GSE160097, an external paired JIA
synovial-fluid-versus-blood memory-CD4 cohort. The external reversal score was
+0.165, closely matching the internal +0.161 estimate. All six
leave-one-donor-pair-out analyses remained positive, and paired-bootstrap
uncertainty excluded zero. PAK2 and RIPK1 remained near zero. The signal was
driven by an inflammatory effector programme rather than a generic
egress-associated module.

RICTOR nevertheless remains a mechanism node, not a validated drug target:
selective pharmacology, human-genetic efficacy support, systemic safety, and
experimental validation remain unresolved. PerturbGate makes both candidate
retention and rejection explicit, reproducible, and auditable.

*(External concordance is reported as an external public JIA cohort with no
detected donor overlap — not an independent cohort, causal/perturbation
replication, or therapeutic validation. See
[EXTERNAL_CONCORDANCE_GSE160097.md](EXTERNAL_CONCORDANCE_GSE160097.md).)*

---

## One-sentence version

PerturbGate turns a 924-perturbation human CD4 T-cell Perturb-seq screen into
auditable, evidence-gated mechanism hypotheses — rejecting a real-but-not-directional
hit (PAK2) and retaining a modest disease-reversing mechanism node with an explicit
modality gap (RICTOR), never a validated drug target.

## 50-word version

PerturbGate converts T-cell Perturb-seq hits into evidence-gated mechanism
hypotheses. PAK2 passed technical but failed therapeutic validation (rejected).
RICTOR survived a pre-specified 8-criterion rescue as a modest disease-reversing
mechanism node with a modality gap — not a validated target. The contribution is an
auditable decision process that preserves negative and superseded results.

## 100-word version

PerturbGate is an open-data, reproducible pipeline that turns primary human CD4
T-cell Perturb-seq hits into evidence-gated mechanism hypotheses. It combines
responder-aware effects, guide/donor robustness, donor-paired disease-state reversal,
matched-perturbation calibration, confound testing, and translational gates. PAK2 —
a real, reproducible cellular hit — did not reverse the disease state and its
external enrichment was activation-confounded, so it was rejected. RICTOR reversed
the corrected activated-memory JIA direction at +0.161 with both guides, 11/11
disease-donor folds, all conditions and confound removal, but a marginal matched
null; it is retained only as a mechanism node with a modality gap. Every claim
resolves to an artifact.

## Non-technical version

Modern gene screens can knock out thousands of genes in immune cells and measure
what changes. It is tempting to call the biggest change a "drug target" — but a real
change is not the same as a useful one. PerturbGate is software that puts each
candidate through a series of honest checks: is the effect real and repeatable? Does
it actually push the cell *away* from a disease state, or just look busy? Is it safe,
and can a drug even reach it? One popular candidate, PAK2, passed the "is it real"
checks but failed the "does it help the disease" checks, so we ruled it out. Another,
RICTOR, passed more checks but still has an unsolved problem: there is no good drug
for it yet. So we call it a promising lead to study further — not a finished target.
The point of the project is that it shows its work: every conclusion, including the
ones we rejected, is written down and can be reproduced.

## Technical reviewer version

PerturbGate scores disease-state reversal as `−centered_Pearson(KD_log2FC,
disease_log2FC)` of a responder-DE donor random-effects meta knockdown vector against
a donor-paired raw-count pseudobulk JIA synovium-vs-blood activated-memory CD4
direction (11 paired donors, 12,071 genes, residency not regressed;
md5 `2b18d92684db1f70b637e1f098374c7e`). RICTOR: +0.161 (p=1.8e-63, 10,832 aligned
genes); guides +0.141/+0.178; 11/11 disease-donor LODO ∈ [+0.154, +0.167]; Rest
+0.153, Stim8hr +0.092, Stim48hr +0.042; responder-only 93% strata positive,
100% donors. A matched-perturbation null (features: magnitude, breadth,
donor-sign-consistency, guide-concordance, on-target-KD; z-scored Euclidean, k=200)
on the conservative all-cell effect-vector substrate places RICTOR at +0.131,
percentile 96.5 (global 97.9), with 7/200 exceeding (empirical p=0.0398; Wilson 95%
CI 0.017–0.070; seed-stable p ∈ [0.032, 0.042]). Confound decomposition
(cell-cycle/activation/stress/apoptosis/T-identity removal) leaves the reversal
essentially unchanged. Criterion 8 (matched null) is the weakest of the eight
pre-specified criteria and is reported as borderline, not decisive. PAK2 is
orthogonal (+0.010, p=0.297; 41st matched percentile), technically valid but
therapeutically non-directional; RIPK1 is a comparator (+0.038, incoherent GSEA;
42nd percentile). Superseded interpretations (old +0.43 reversal; PAK2 JIA
enrichment; PAK2 partial-inhibition; PAK2 neighbour; PAK2–WASF2 axis) are registered
and blocked from the public outputs. Levels 1–2 reproduce on a laptop; Level 3
reconstructs from open data on a high-memory server.

---

## Links

- Repository README: [../README.md](../README.md)
- Methods: [METHODS.md](METHODS.md) · Results: [RESULTS.md](RESULTS.md)
- Decision trail: [DECISION_TRAIL.md](DECISION_TRAIL.md)
- Claims & evidence: [CLAIMS_AND_EVIDENCE.md](CLAIMS_AND_EVIDENCE.md)
- Superseded results: [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md)
- Reproducibility: [REPRODUCIBILITY.md](REPRODUCIBILITY.md) ·
  [REPRODUCIBILITY_LEVELS.md](REPRODUCIBILITY_LEVELS.md)
- Claude usage: [CLAUDE_USAGE.md](CLAUDE_USAGE.md)
- Demo video script: [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
