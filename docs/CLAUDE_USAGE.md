# Claude usage

This document records **how Claude was used** in building PerturbGate — an
evidence-gated pipeline for T-cell Perturb-seq mechanism hypotheses, built for
*Built with Claude: Life Sciences* (Anthropic × Gladstone Institutes), Research
track. It is written for reviewers who want to understand the division of labour
between the human investigators and the AI assistance, and — more importantly —
the epistemic boundary around that assistance.

The single most important point in this file is stated first, because it governs
everything below:

> **AI output is not scientific evidence.** No claim in this repository is
> supported by "Claude said so." Every public biological claim resolves to a
> committed **data artifact**, a **primary paper**, or an **official database**.
> Claude was an instrument for implementation and adversarial reasoning, not a
> source of evidence, and no private conversation transcript is exposed anywhere
> in the public outputs.

---

## Central message: Claude mattered most when the hypothesis failed

PerturbGate's contribution is not that it found a positive hit. It is that every
retained claim survives an explicit, auditable record of how competing claims
failed. Framed correctly, this is **target nomination, not gene ranking**: a real
perturbation effect is *necessary but not sufficient* for target nomination.

Claude's marginal value tracked that framing. On the parts of the project where
things were going well — a reproducible cellular signature, a large centered-
Pearson reversal — Claude was a competent but ordinary coding assistant. Its
contribution became decisive precisely at the points where the **initial
hypothesis failed**, where the temptation to keep an attractive result was
strongest, and where an honest pipeline has to design a harder test against its
own preferred answer. Three concrete instances:

1. **PAK2 was an attractive cellular hit that had to be rejected.** PAK2 passed
   technical validation — on-target knockdown of ~83–86% on both guides, guide
   concordance 0.85, a donor/guide/LODO-robust 112-gene responder programme,
   Mixscape responder fraction 76.5%, non-toxic. The attractive next step was to
   call it a target. Adversarial review instead surfaced that its apparent
   external JIA enrichment was **activation-confounded** (the FROZEN-UP and
   FROZEN-DOWN modules co-elevate, `diverge=False`), that its disease reversal was
   `+0.010` (p=0.297, not significant; 41st matched-null percentile), and that
   partial-inhibition sufficiency was **not established** (both guides similarly
   strong, no strong-vs-weak titration axis). PAK2 is retained as
   `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` and **rejected as a
   target nomination**. Four earlier PAK2 interpretations (JIA enrichment as
   disease support; partial-inhibition support; a "safer neighbour"; a PAK2–WASF2
   therapeutic axis) were registered as superseded rather than deleted.

2. **An inflated RICTOR number had to be corrected down.** An early RICTOR
   reversal of roughly +0.43 came from a residency-removed 77-gene subset with a
   responder-only knockdown representation. Recognising that this was inflated by
   the frozen-subset gene universe and the knockdown representation — not a real
   effect size — led to the honest full-transcriptome primary value of **+0.161**
   and the conservative all-cell null-substrate projection of **+0.131**. The old
   value is preserved only in explicitly-superseded context (`SUP-01`) and is
   blocked from the public outputs by an automated audit.

3. **The surviving claim was forced through a harder, pre-specified test.**
   Rather than accept RICTOR on the strength of a single correlation, the analysis
   fixed **eight criteria before viewing the corrected raw-count result** and then
   evaluated RICTOR against a matched-perturbation null. RICTOR **satisfied seven
   strong convergence checks and nominally exceeded a matched-perturbation null,
   with borderline finite-pool uncertainty** — it is retained as
   `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`, a mechanism hypothesis,
   **not a validated drug target**.

In each case the useful contribution was not producing an answer — it was helping
design a stricter falsification test, preserve the negative result, and stop an
attractive cellular hit from becoming an unsupported drug-target claim.

---

## Two modes of assistance

Assistance came through two distinct surfaces, kept separate on purpose.

### Claude Code — building and auditing the pipeline

Claude Code was used for engineering the reproducible machinery. Concretely:

- **Pipeline implementation**: the reversal scoring
  (`−centered_Pearson(KD_log2FC, disease_log2FC)`), pseudobulk assembly, guide/
  donor/LODO robustness, matched-perturbation null construction (features:
  magnitude, breadth, donor-sign-consistency, guide-concordance, on-target-KD;
  z-scored Euclidean, k=200), and confound decomposition.
- **Debugging**: e.g. tracing a gene-ID namespace mismatch (ENSG↔symbol) that had
  earlier produced a spurious "safer PAK2 neighbour" result.
- **Server execution**: orchestrating server-scale reconstruction jobs on the
  high-memory batch server (open JIA h5ad + Perturb-seq rebuild). No
  compute-cluster name, hostname, username, home path, or job identifier is
  recorded in the public outputs.
- **Tests and provenance**: golden-value tests, tolerance checks, the frozen
  claims/evidence ledger, superseded-claim blocking, and input checksums (disease
  vector md5 `2b18d92684db1f70b637e1f098374c7e`).
- **Packaging and reproducibility audit**: the three-level reproducibility ladder
  (laptop `make demo`; committed-input `make reproduce`; server-scale
  `make full`), the public-readiness/privacy audit, and figure regeneration.

### Claude Science — red-teaming and external grounding

Claude Science was used as an adversarial reasoning and literature/database
scouting surface, never as an evidence source. Concretely:

- **Hypothesis red-teaming**: actively arguing against the preferred answer
  (PAK2-as-target; the inflated RICTOR effect) to expose where each claim could
  be wrong.
- **Prior-art review**: contextualising RIPK1 as a benchmark comparator (real
  IBD/autoinflammatory genetics and clinical-stage kinase inhibitors exist; full
  loss-of-function causes immunodeficiency, so kinase inhibition — not knockdown —
  is the relevant modality).
- **Confound identification**: flagging the activation confound behind the PAK2
  JIA enrichment, and motivating the confound decomposition
  (cell-cycle/activation/stress/apoptosis/T-identity removal) that leaves RICTOR's
  reversal essentially unchanged.
- **Safety and modality assessment**: the essentiality/tractability gate that left
  the single-state screen with **no advanceable candidate**, and the RICTOR
  "modality gap" (mTORC2 core scaffold, no selective small-molecule modality).
- **External-dataset scouting**: identifying the open JIA synovial atlas and the
  Perturb-seq resource used to build the disease vector and effect vectors.
- **Contradiction and retraction checks**: cross-checking that surviving claims do
  not conflict with established literature, and that superseded interpretations
  are corrected rather than quietly promoted.

Every output from either surface was treated as a hypothesis to be verified
against artifacts and primary sources — not as a finding.

### RICTOR translational audit (final release)

In the completed RICTOR translational-readiness audit, **Claude Science identified
and verified two RICTOR-relevant retraction chains, distinguished vendor-labelled
compounds from validated target engagement, detected neighbour-gene pQTL
misattribution, and preserved a human-genetics efficacy null rather than converting
it into support.** Concretely:

- it flagged that the JR-AB2-011 founding paper (retraction DOI
  `10.1371/journal.pone.0291490`) and the only RICTOR-ASO human-autoimmune-disease
  paper (retraction DOI `10.1093/rheumatology/keaf391`) are **both retracted**, and
  recorded them only as do-not-use entries;
- it corrected the compound identity (JR-AB2-011 = PubChem CID 138319699, not the
  precursor CID 613034) and surfaced independent work showing JR-AB2-011 acts
  RICTOR-independently;
- it flagged that the RICTOR locus (5p13.1) is confounded by OSMR and FYB1, so any
  "RICTOR" pQTL/eQTL needs colocalization before use;
- it kept the Open Targets efficacy null as a null.

Every one of these resolves to PubMed / PubChem / gnomAD / Open Targets, checked by
`scripts/check_references.py`. See
[../results/translational/](../results/translational/) and
[TRANSLATIONAL_AUDIT_UPDATE.md](TRANSLATIONAL_AUDIT_UPDATE.md).

---

## How AI assistance maps to evidence

To make the epistemic boundary concrete, the claims Claude helped stress-test all
resolve to committed artifacts, not to the assistant:

| Claim | Public label | Resolves to |
| --- | --- | --- |
| RICTOR reverses the corrected activated-memory JIA direction at +0.161 (seven convergence checks; nominal matched-null; borderline finite-pool) | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` | [`results/frozen/primary_comparison.tsv`](../results/frozen/primary_comparison.tsv), [`rictor_guides.tsv`](../results/frozen/rictor_guides.tsv), [`rictor_lodo.tsv`](../results/frozen/rictor_lodo.tsv), [`rictor_conditions.tsv`](../results/frozen/rictor_conditions.tsv), [`matched_null.tsv`](../results/frozen/matched_null.tsv) |
| PAK2 is a real cellular hit but not therapeutically directional (+0.010, p=0.297; activation-confounded) | `REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` | [`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv), [`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv) |
| RIPK1 is a comparator not directionally supported here (+0.038; 42nd matched-null percentile) | `COMPARATOR_NOT_DIRECTIONALLY_SUPPORTED_IN_THIS_ANALYSIS` | [`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv), [`matched_null.tsv`](../results/frozen/matched_null.tsv) |
| Attrition: 924 scored → 208 convergent (FDR<0.10) → 21 robust → 0 advanceable from the single-state screen | process claim | [`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv), [`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv), [`all_perturbations_authoritative_reversal.tsv`](../results/frozen/all_perturbations_authoritative_reversal.tsv) |
| Superseded interpretations (old +0.43 RICTOR; PAK2 enrichment/partial-inhibition/neighbour/WASF2) | corrected, not deleted | [`superseded_claims.json`](../results/frozen/superseded_claims.json), [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md) |

External evidence resolves to **primary literature and official databases**: the
Marson/Pritchard CD4 T-cell Perturb-seq resource (bioRxiv DOI
`10.64898/2025.12.23.696273`; GEO `GSE314342` / SRA `SRP643211`) and the JIA
synovial single-cell atlas (bioRxiv DOI `10.64898/2026.05.01.716870`; companion
*Sci Transl Med* DOI `10.1126/scitranslmed.adt6050`; CZ CELLxGENE collection
`10eb236d-d42d-45b8-8363-c2dcf865f388`).

---

## What Claude was *not* used to do

To avoid overstating the role of AI:

- Claude was **not** an evidence source. Where a biological statement appears in
  the public repository, its support is an artifact, a paper, or a database — not
  an assistant transcript.
- No **private conversation transcript** is published. This document describes the
  *nature* of the assistance, not its verbatim content.
- Claude did **not** decide the controlled labels or the effect sizes. Those are
  computed by committed code from committed inputs and frozen; the reproducibility
  ladder lets a third party recompute them independently.
- Claude assistance does **not** upgrade the strength of any claim. In particular
  it does not make RICTOR a validated drug target, does not establish a selective
  RICTOR modality, and does not turn synovium-vs-blood into disease-vs-healthy or
  into independent replication. The same-cohort adjusted-vector sensitivity is not
  independent biological replication, and the nominal matched-null significance is
  not definitive. See [LIMITATIONS.md](LIMITATIONS.md).

---

## Related documentation

- Results in full: [RESULTS.md](RESULTS.md)
- The decision process, stage by stage: [DECISION_TRAIL.md](DECISION_TRAIL.md)
- Analytical failure modes the pipeline guards against:
  [FAILURE_MODES.md](FAILURE_MODES.md)
- Corrected/superseded interpretations: [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md)
- Scope and non-claims: [LIMITATIONS.md](LIMITATIONS.md)
- Reproducing the numbers: [REPRODUCIBILITY.md](REPRODUCIBILITY.md) ·
  [REPRODUCIBILITY_LEVELS.md](REPRODUCIBILITY_LEVELS.md)
- Hackathon submission summary: [HACKATHON_SUBMISSION.md](HACKATHON_SUBMISSION.md)
