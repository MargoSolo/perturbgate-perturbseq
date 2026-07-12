# Translational context

This document places the PerturbGate result in its biological, pharmacological,
and safety context. Its scope is deliberately narrow. It is written for the one
retained hypothesis — **RICTOR** — with a short companion card explaining why the
external literature is consistent with the **PAK2** rejection.

> **Read this first.** RICTOR carries the controlled label
> `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP`. That label is a
> **mechanism hypothesis**, not a target nomination. RICTOR is **not** a validated
> drug target, is **not** an advanceable target, and there is **no** demonstrated
> selective modality against it. Everything below is context for a mechanism node
> that survived falsification, not a case for developing a drug. The primary
> statistical caveats live in [Limitations](LIMITATIONS.md); the reproducibility
> tiers in [Reproducibility levels](REPRODUCIBILITY_LEVELS.md); the headline claims
> and the "What we do not claim" box in the [README](../README.md).

All biological claims resolve to primary literature or an official database (cited
at the end). Model-generated review text is **not** used as evidence. All internal
effect sizes are quoted with their denominators and uncertainty, never a p-value
alone, and trace to `results/frozen/`.

---

## 1. What RICTOR is: mTORC2 biology

RICTOR (rapamycin-insensitive companion of mTOR) is a large, non-catalytic
**scaffold** subunit that defines mechanistic target-of-rapamycin complex 2
(mTORC2). It was identified as an mTOR-binding partner that assembles a
rapamycin-insensitive, raptor-independent complex controlling the actin
cytoskeleton (Sarbassov et al., *Curr Biol* 2004; Jacinto et al., *Nat Cell Biol*
2004). The defining catalytic output of the RICTOR–mTOR complex is
phosphorylation of AKT/PKB at Ser473, which primes AKT signalling (Sarbassov et
al., *Science* 2005). Genetic ablation studies established that mTORC2 (via
raptor/rictor/mLST8 dissection) is required for AKT–FOXO and PKCα signalling but
not for S6K1 (Guertin et al., *Dev Cell* 2006).

RICTOR is therefore not an enzyme with a druggable active site of its own; it is
the **structural core** of a signalling complex. This distinction is central to
the modality discussion in Section 3.

In T cells specifically, mTORC2/RICTOR shapes effector versus regulatory
differentiation. mTOR integrates activation signals through the differential use
of mTORC1 and mTORC2 (Delgoffe et al., *Immunity* 2009; Delgoffe et al., *Nat
Immunol* 2011), and rictor-dependent mTORC2 signalling regulates T-helper subset
differentiation (Lee et al., *Immunity* 2010). That published role — mTORC2 as a
node biasing T cells toward inflammatory effector programmes — is the biological
backdrop against which the PerturbGate directional signal should be read.

## 2. Directional coherence (why this is a mechanism node, not noise)

On the frozen JIA disease vector, RICTOR knockdown **reverses** the disease
direction with a small but highly reproducible effect: primary
responder-resolved centered-Pearson reversal **+0.161** (r² ≈ 2.6 %, 10 832
aligned genes), Spearman **+0.100**. The effect is positive on both guides
(RICTOR-1 **+0.141**, RICTOR-2 **+0.178**), across all 11 disease-donor
leave-one-donor-out folds (band **+0.154 … +0.167**), and in all three
conditions (Rest **+0.153**, Stim8hr **+0.092**, Stim48hr **+0.042**). Against a
matched-perturbation null in the conservative all-cell substrate (**+0.131**),
RICTOR sits at matched-null percentile **96.5** (global percentile 97.9), with
**7 of 200** matched controls exceeding it (empirical p ≈ **0.040**; Wilson 95 %
CI up to ≈ **0.070**).

Using the pre-specified rescue framework, RICTOR **satisfied seven strong
convergence checks and nominally exceeded a matched-perturbation null, with
borderline finite-pool uncertainty** (the matched-null check is the weakest of the
eight; see [Limitations](LIMITATIONS.md)). This is deliberately **not** described
as "8/8 decisive."

What makes the direction biologically legible is the leading edge: RICTOR
knockdown turns **down** disease-UP effector genes — CXCL13, CXCR6, CCL4, IFNG,
GZMB, PDCD1, RGS1 — with **0** disease-UP genes reinforced
(`results/frozen/leading_edge.tsv`). Suppression of an IFNG/GZMB/CXCR6 effector
programme is directionally consistent with the published role of mTORC2 in
effector-T-cell differentiation cited above. The reversal is confound-resistant:
removing cell-cycle, activation, stress, apoptosis, or T-identity gene sets leaves
it essentially unchanged (`results/frozen/confound_decomposition.tsv`). It drops
to **+0.093** only when the 780 strongly-knockdown-down genes are removed — but
those genes *include* the pathogenic disease-UP effectors (CXCR6, CCL4, IFNG), so
that ablation removes real signal, not a confound. See
`figures/figure_2_directionality_and_null.svg` and
`figures/supplementary_rictor_robustness.svg`.

Coherence with known biology raises prior plausibility. It does **not** establish
efficacy, safety, or druggability. Those are the subjects of the next three
sections, and each is unresolved.

## 3. The modality gap

RICTOR's label ends in `_WITH_MODALITY_GAP` for a concrete reason: **there is no
selective small-molecule modality against RICTOR/mTORC2.** RICTOR is a scaffold,
not a catalytic pocket, and the reversal signal leans on RICTOR's selective
downregulation arm — a genetic knockdown, not a pharmacological inhibition that a
clinician could deliver.

The available mTOR pharmacology does not close this gap:

- **Rapalogs (sirolimus and analogues)** acutely inhibit mTORC1 and are, by
  definition, rapamycin-*insensitive* with respect to the core mTORC2 reaction.
  Prolonged rapamycin exposure can secondarily disrupt mTORC2 assembly in some
  cell types (Sarbassov et al., *Mol Cell* 2006), but this is an indirect,
  cell-type-dependent effect, not selective RICTOR inhibition.
- **ATP-competitive mTOR kinase inhibitors** (e.g. Torin-class compounds; Thoreen
  et al., *J Biol Chem* 2009) block the mTOR catalytic site and therefore inhibit
  mTORC1 **and** mTORC2 together. They are dual-complex inhibitors, not
  RICTOR-selective, and mTORC1 co-inhibition carries its own liabilities.

No agent in clinical or validated preclinical use selectively removes RICTOR/mTORC2
function while sparing mTORC1.

> **Explicit exclusion.** The literature contains reports of putatively
> mTORC2-selective tool compounds. We do **not** rely on any such report as
> evidence of a validated modality, and in particular we do **not** treat the
> retracted selective-mTORC2-inhibitor study as evidence that a selective modality
> exists. Retracted work is excluded from the evidence base by construction. The
> modality assessment above rests only on the well-characterized,
> non-RICTOR-selective pharmacology.

Bottom line for Section 3: even if the disease-reversal direction were fully
validated, a therapeutic route to act on it selectively does **not** currently
exist.

## 4. Safety considerations

Systemic RICTOR/mTORC2 inhibition is **not** shown to be safe, and the biology
argues for caution rather than reassurance:

- **Constitutive essentiality (mouse).** Whole-body rictor ablation is embryonic
  lethal in mice, with mTORC2 required for fetal growth and viability (Shiota et
  al., *Dev Cell* 2006; Guertin et al., *Dev Cell* 2006). RICTOR is a core
  developmental scaffold, not a dispensable modifier.
- **Human constraint.** Loss-of-function constraint for RICTOR should be read
  directly from gnomAD; RICTOR is a large, essential scaffold and its constraint
  metrics belong in any serious tractability assessment (Karczewski et al.,
  *Nature* 2020). We do not assert a specific constraint value here.
- **Internal safety readouts (bounded, and imperfect).** In the Perturb-seq data,
  RICTOR knockdown carries a **mild, donor-inconsistent early-toxicity flag**:
  apoptosis Δ **+0.030** with only **≤ 33 %** of strata consistent
  (`results/frozen/safety_summary.tsv`). This is weak and not donor-robust, so it
  is neither a clean safety signal nor a clean all-clear. T-cell and Treg identity
  scores were preserved in this readout, but a preserved identity score in one
  cohort is not a safety demonstration.

Together these mean systemic-inhibition safety is **unestablished**. A mechanism
node that is also a developmentally essential scaffold is exactly the kind of node
that requires a selectivity/tissue-restriction strategy that does not yet exist
(Section 3).

## 5. Disease surrogate: synovium-vs-blood is not disease-vs-healthy

The disease direction used throughout PerturbGate is a **compartment contrast, not
a disease-state contrast.** It is a JIA **synovium (tissue + fluid) versus
peripheral blood** signature in activated-memory CD4 T cells — raw-count,
donor-paired pseudobulk across 11 paired donors — derived from the JIA synovial
single-cell atlas (Knight et al., bioRxiv 2026, DOI
10.64898/2026.05.01.716870; companion Bolton, Mahony et al., *Sci Transl Med*
2025, DOI 10.1126/scitranslmed.adt6050).

This has direct interpretive consequences:

- It contrasts an **inflamed site against the circulation within patients**, not
  diseased tissue against healthy tissue, and not adult rheumatoid arthritis.
- Tissue-residency and compartment programmes are **partially confounded with
  disease** by construction (residency was not regressed out). "Turning down the
  synovial signature" is not identical to "reversing disease."
- A perturbation that shifts synovial-compartment biology may or may not be
  disease-modifying in vivo. The surrogate cannot distinguish these.

This is a bounded proxy for disease biology, and it is labelled as such wherever
the disease vector is used.

## 6. Human genetics and independent replication are unresolved

Two of the strongest possible external supports for a target are (a) human
genetic evidence that perturbing the gene in the disease-beneficial direction is
tolerated and protective, and (b) replication of the transcriptional signal in an
independent cohort. **Neither is resolved for RICTOR in this work.**

- **Human genetics — not evaluated here.** Whether human genetics support RICTOR
  inhibition in the disease-beneficial direction is an open question. The
  appropriate sources to interrogate are official databases — gnomAD for
  loss-of-function constraint (Karczewski et al., *Nature* 2020), OMIM and ClinGen
  for Mendelian gene–disease relationships, the NHGRI-EBI GWAS Catalog for
  association evidence, and the Open Targets Platform for aggregated
  target–disease genetics (Ochoa et al., *Nucleic Acids Res* 2023). We make no
  claim that RICTOR carries directional human-genetic support for JIA; that
  assessment has not been done here.
- **Replication — same cohort only.** Every disease-donor statistic derives from a
  **single** JIA atlas. Leave-one-donor-out is within-cohort robustness. The
  agreement between the primary raw-count vector and the older covariate-adjusted
  vector is a **same-cohort sensitivity analysis, not independent biological
  replication** — both are computed on the same donors. Cross-cohort replication
  remains to be done.

Until both are addressed, RICTOR stays a mechanism node.

## 7. PAK2 external-support card (why the rejection is consistent with the literature)

PAK2 was a **real, reproducible cellular hit** — controlled label
`REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL` — that **failed**
therapeutic-directionality validation (disease reversal **+0.010**, not
significant; matched-null 41st percentile; external JIA enrichment
activation-confounded, so `disease_relevant=False`). It was rejected as a target
nomination despite passing technical validation. The external literature is
consistent with that rejection:

- PAK2 is a **broadly required kinase**, not an immune-selective node. It is
  required for normal thymocyte development, TCR signalling, and actin
  remodelling (Phee et al., *eLife* 2014). A gene whose loss reshapes core T-cell
  development is a poor fit for a clean, disease-directional anti-inflammatory
  mechanism.
- PAK2 registers as **broadly essential** across cell lines in the Cancer
  Dependency Map (DepMap; Tsherniak et al., *Cell* 2017). Broad essentiality is
  consistent with our finding that the PAK2 knockdown signature is a genuine but
  **generic activation-linked programme** rather than a selective disease-reversing
  one.

None of this makes PAK2 uninteresting biologically; it makes PAK2 unsuitable as a
**therapeutic-direction** nomination on this evidence. See
`figures/figure_4_pak2_rejection.svg` and the superseded PAK2 claims recorded in
`results/frozen/superseded_claims.json` (the earlier "JIA joint enrichment,"
"partial-inhibition supported," "safer neighbour," and "PAK2–WASF2 axis" readings
are all superseded and must not be presented as current).

## Bottom line

RICTOR is a **disease-reversing mechanism node with a modality gap**: a
directionally coherent, confound-resistant, small-but-robust reversal of a JIA
synovial effector programme, supported by seven strong convergence checks and a
nominal matched-null pass with borderline finite-pool uncertainty. It is held back
from any target claim by four unresolved translational facts — no selective
modality, unestablished systemic-inhibition safety, a synovium-vs-blood surrogate
that is not disease-vs-healthy, and no human-genetic or independent-cohort
support. RICTOR is retained as a hypothesis to test, **not** as a target to
advance.

---

## References

### Primary literature

- Sarbassov DD, Ali SM, Kim D-H, et al. Rictor, a novel binding partner of mTOR,
  defines a rapamycin-insensitive and raptor-independent pathway that regulates the
  cytoskeleton. *Curr Biol.* 2004;14(14):1296–1302. DOI 10.1016/j.cub.2004.06.054
- Jacinto E, Loewith R, Schmidt A, et al. Mammalian TOR complex 2 controls the
  actin cytoskeleton and is rapamycin insensitive. *Nat Cell Biol.*
  2004;6(11):1122–1128. DOI 10.1038/ncb1183
- Sarbassov DD, Guertin DA, Ali SM, Sabatini DM. Phosphorylation and regulation of
  Akt/PKB by the rictor–mTOR complex. *Science.* 2005;307(5712):1098–1101. DOI
  10.1126/science.1106148
- Sarbassov DD, Ali SM, Sengupta S, et al. Prolonged rapamycin treatment inhibits
  mTORC2 assembly and Akt/PKB. *Mol Cell.* 2006;22(2):159–168. DOI
  10.1016/j.molcel.2006.03.029
- Guertin DA, Stevens DM, Thoreen CC, et al. Ablation in mice of the mTOR
  components raptor, rictor, or mLST8 reveals that mTORC2 is required for signaling
  to Akt-FOXO and PKCα, but not S6K1. *Dev Cell.* 2006;11(6):859–871. DOI
  10.1016/j.devcel.2006.10.007
- Shiota C, Woo J-T, Lindner J, et al. Multiallelic disruption of the rictor gene
  in mice reveals that mTOR complex 2 is essential for fetal growth and viability.
  *Dev Cell.* 2006;11(4):583–589. DOI 10.1016/j.devcel.2006.08.013
- Thoreen CC, Kang SA, Chang JW, et al. An ATP-competitive mammalian target of
  rapamycin inhibitor reveals rapamycin-resistant functions of mTORC1. *J Biol
  Chem.* 2009;284(12):8023–8032. DOI 10.1074/jbc.M900301200
- Delgoffe GM, Kole TP, Zheng Y, et al. The mTOR kinase differentially regulates
  effector and regulatory T cell lineage commitment. *Immunity.*
  2009;30(6):832–844. DOI 10.1016/j.immuni.2009.04.014
- Lee K, Gudapati P, Dragovic S, et al. Mammalian target of rapamycin protein
  complex 2 regulates differentiation of Th1 and Th2 cell subsets via distinct
  signaling pathways. *Immunity.* 2010;32(6):743–753. DOI
  10.1016/j.immuni.2010.06.002
- Delgoffe GM, Pollizzi KN, Waickman AT, et al. The kinase mTOR regulates the
  differentiation of helper T cells through the selective activation of signaling
  by mTORC1 and mTORC2. *Nat Immunol.* 2011;12(4):295–303. DOI 10.1038/ni.2005
- Phee H, Au-Yeung BB, Pryshchep O, et al. Pak2 is required for actin cytoskeleton
  remodeling, TCR signaling, and normal thymocyte development and maturation.
  *eLife.* 2014;3:e02270. DOI 10.7554/eLife.02270
- Tsherniak A, Vazquez F, Montgomery PG, et al. Defining a Cancer Dependency Map.
  *Cell.* 2017;170(3):564–576. DOI 10.1016/j.cell.2017.06.010
- Karczewski KJ, Francioli LC, Tiao G, et al. The mutational constraint spectrum
  quantified from variation in 141,456 humans (gnomAD). *Nature.*
  2020;581(7809):434–443. DOI 10.1038/s41586-020-2308-7
- Ochoa D, Hercules A, Carmona M, et al. The next-generation Open Targets Platform:
  reimagined, redesigned, rebuilt. *Nucleic Acids Res.* 2023;51(D1):D1353–D1359.
  DOI 10.1093/nar/gkac1046

### Disease and perturbation datasets (primary)

- Knight AM, et al. JIA synovial single-cell atlas — "Integrated global cells."
  *bioRxiv* 2026. DOI 10.64898/2026.05.01.716870 (CC-BY-4.0).
- Bolton C, Mahony CB, et al. Companion JIA synovial study. *Sci Transl Med* 2025.
  DOI 10.1126/scitranslmed.adt6050
- Marson & Pritchard laboratories. Primary human CD4+ T-cell Perturb-seq. *bioRxiv*
  2025. DOI 10.64898/2025.12.23.696273 (MIT).

### Official databases (to be interrogated directly)

- gnomAD — loss-of-function constraint. https://gnomad.broadinstitute.org
- OMIM — Mendelian gene–disease relationships. https://omim.org
- ClinGen — clinical gene–disease validity. https://clinicalgenome.org
- NHGRI-EBI GWAS Catalog — genetic associations. https://www.ebi.ac.uk/gwas
- Open Targets Platform — aggregated target–disease evidence.
  https://platform.opentargets.org
- DepMap — cancer cell-line dependency / essentiality. https://depmap.org

---

*Related documentation:* [Limitations](LIMITATIONS.md) ·
[Reproducibility levels](REPRODUCIBILITY_LEVELS.md) ·
[Failure modes](FAILURE_MODES.md) · [README](../README.md).
Superseded claims are recorded in `results/frozen/superseded_claims.json`. The
superseded RICTOR reversal of ≈ +0.43 is a retired covariate-adjusted 77-gene-subset
number and must never be presented as a current result; the current values are the
primary +0.161 and the conservative null-substrate +0.131.
