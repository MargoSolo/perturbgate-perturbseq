#!/usr/bin/env python3
"""Build the RICTOR translational-readiness tables (results/translational/).

These encode the completed Claude Science translational audit. Every literature
identifier (PMID / DOI) was verified against PubMed / PubChem / gnomAD / Open
Targets during the audit; retracted work is recorded ONLY as do-not-use evidence.
Reads nothing private; runs anywhere; writes LF, byte-stable TSVs.

Key verified corrections folded in:
  * JR-AB2-011 = PubChem CID 138319699 (CAS 2411853-34-2); CID 613034 is the
    *precursor* screening hit "CID613034", a different molecule.
  * The JR-AB2-011 founding paper (PLoS One 2017, PMID 28453552) is RETRACTED
    (retraction DOI 10.1371/journal.pone.0291490, PMID 37682814).
  * The RICTOR-ASO SLE paper (Rheumatology 2025, PMID 39656824) is RETRACTED
    (retraction DOI 10.1093/rheumatology/keaf391, PMID 40966663).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "results" / "translational"
OUT.mkdir(parents=True, exist_ok=True)


def write(rows: list[dict], name: str) -> None:
    df = pd.DataFrame(rows)
    with open(OUT / name, "w", encoding="utf-8", newline="") as fh:
        df.to_csv(fh, sep="\t", index=False, lineterminator="\n")
    print(f"  wrote results/translational/{name}  ({len(df)} rows)")


# --- Prior art / novelty boundary -------------------------------------------
prior_art = [
    dict(topic="mTORC2/RICTOR regulates Th1/Th2 differentiation", finding="established prior art (not novel)",
         novelty="ESTABLISHED", pmid="20620941", doi="10.1016/j.immuni.2010.06.002",
         retracted="False", retraction_doi="", evidence_use="context",
         note="Lee et al. Immunity 2010 — we do NOT claim novelty of mTORC2 T-cell biology"),
    dict(topic="RICTOR activity destabilizes Foxp3/Treg", finding="established opposing immune effect",
         novelty="ESTABLISHED", pmid="26437242", doi="10.1038/ni.3288",
         retracted="False", retraction_doi="", evidence_use="context",
         note="Charbonnier et al. Nat Immunol 2015 — motivates the cell-type-conflict safety concern"),
    dict(topic="JR-AB2-011 'specific blockade of Rictor-mTOR' (founding paper)", finding="RETRACTED",
         novelty="RETRACTED_PRIOR_ART", pmid="28453552", doi="10.1371/journal.pone.0176599",
         retracted="True", retraction_doi="10.1371/journal.pone.0291490", evidence_use="do_not_use",
         note="Benavides-Serrato et al. PLoS One 2017; retracted 2023 (figure-integrity); not cited as support"),
    dict(topic="RICTOR-ASO attenuates SLE immunopathology (human PBMCs)", finding="RETRACTED",
         novelty="RETRACTED_PRIOR_ART", pmid="39656824", doi="10.1093/rheumatology/keae662",
         retracted="True", retraction_doi="10.1093/rheumatology/keaf391", evidence_use="do_not_use",
         note="Ai et al. Rheumatology 2025; retracted 2025 (data miscalculation; human-efficacy figure); not cited as support"),
    dict(topic="JR-AB2-011 acts mTORC2-independently (off-target)", finding="effect persists in RICTOR-null cells",
         novelty="CAUTIONARY", pmid="39259491", doi="10.1007/s43440-024-00649-7",
         retracted="False", retraction_doi="", evidence_use="cautionary",
         note="Koranova et al. Pharmacol Rep 2024 — undermines JR-AB2-011 as a RICTOR target-engagement tool"),
    dict(topic="PerturbGate narrow claim (this work)",
         finding="RICTOR-specific KD in primary human CD4 T cells reverses a donor-paired inflamed-joint "
                 "activated-memory programme (tissue-retention + cytotoxic-effector genes) without detectable "
                 "Treg-identity collapse in this dataset",
         novelty="NARROW_COMPUTATIONAL_HYPOTHESIS", pmid="", doi="",
         retracted="False", retraction_doi="", evidence_use="this_work",
         note="computational mechanism hypothesis, NOT functional validation"),
]

# --- Modality landscape ------------------------------------------------------
modality = [
    dict(modality_class="small_molecule (mTORC2 disruptor)", example="JR-AB2-011", cid="138319699",
         status="NOT_VALIDATED", validated_target_engagement="no",
         retracted="True", pmid="28453552", doi="10.1371/journal.pone.0176599",
         retraction_doi="10.1371/journal.pone.0291490", evidence_use="do_not_use",
         note="founding paper retracted; off-target/RICTOR-independent (PMID 39259491); precursor hit = CID 613034"),
    dict(modality_class="antisense oligonucleotide (ASO)", example="anti-Rictor ASO (SLE)", cid="",
         status="NOT_VALIDATED", validated_target_engagement="no",
         retracted="True", pmid="39656824", doi="10.1093/rheumatology/keae662",
         retraction_doi="10.1093/rheumatology/keaf391", evidence_use="do_not_use",
         note="human SLE efficacy figure retracted; not a validated autoimmune modality"),
    dict(modality_class="antisense oligonucleotide (research tool, non-autoimmune)",
         example="Rictor-ASO (Pten neuropathology / inflammatory pain)", cid="",
         status="RESEARCH_TOOL_ONLY", validated_target_engagement="partial_knockdown",
         retracted="False", pmid="31636454", doi="10.1038/s41591-019-0608-y",
         retraction_doi="", evidence_use="cautionary",
         note="Chen Nat Med 2019 / Wong JCI 2022 (PMID 35579957) — knockdown tools, not clinical autoimmune modality"),
    dict(modality_class="ATP-competitive mTOR kinase inhibitor", example="PP242/Torin/AZD8055 (dual mTORC1/2)", cid="",
         status="NOT_SELECTIVE", validated_target_engagement="mTORC2_not_RICTOR_selective",
         retracted="False", pmid="", doi="", retraction_doi="", evidence_use="context",
         note="inhibit mTORC2 kinase activity but also mTORC1; not RICTOR-selective"),
    dict(modality_class="targeted degrader (PROTAC / molecular glue)", example="none known", cid="",
         status="NONE", validated_target_engagement="no",
         retracted="False", pmid="", doi="", retraction_doi="", evidence_use="none",
         note="no validated RICTOR degrader"),
    dict(modality_class="peptide / PPI disruptor", example="none validated", cid="",
         status="NONE", validated_target_engagement="no",
         retracted="False", pmid="", doi="", retraction_doi="", evidence_use="none",
         note="no validated RICTOR-selective peptide"),
    dict(modality_class="clinical-stage RICTOR-selective agent", example="none", cid="",
         status="NONE", validated_target_engagement="no",
         retracted="False", pmid="", doi="", retraction_doi="", evidence_use="none",
         note="no approved or trial-stage RICTOR-selective modality"),
]

# --- Safety landscape (mouse Rictor KO phenotypes) ---------------------------
safety = [
    dict(system="developmental", model="whole-body Rictor-null mouse", phenotype="embryonic lethal (~E11.5)",
         translational_direction="liability", pmid="16962829", doi="10.1016/j.devcel.2006.08.013",
         note="Shiota et al. Dev Cell 2006 — mTORC2 essential for fetal growth/viability"),
    dict(system="developmental", model="whole-body Rictor-null mouse", phenotype="early embryonic lethality",
         translational_direction="liability", pmid="17141160", doi="10.1016/j.devcel.2006.10.007",
         note="Guertin et al. Dev Cell 2006 — mTORC2 required for AKT-S473/PKCalpha"),
    dict(system="vascular/developmental", model="endothelial Rictor cKO", phenotype="lethality (~E12)",
         translational_direction="liability", pmid="26635098", doi="10.1038/srep17705",
         note="Aimi et al. Sci Rep 2015 — endothelial Rictor crucial for midgestation"),
    dict(system="metabolic", model="liver-specific Rictor cKO (LiRiKO)",
         phenotype="hyperglycemia, hyperinsulinemia, hypolipidemia", translational_direction="liability",
         pmid="22521878", doi="10.1016/j.cmet.2012.03.015",
         note="Hagiwara et al. Cell Metab 2012 — hepatic mTORC2 controls glycolysis/lipogenesis"),
    dict(system="immune (effector T cells)", model="T-cell Rictor cKO", phenotype="impaired Th1 and Th2 differentiation",
         translational_direction="cell_type_conflict", pmid="20620941", doi="10.1016/j.immuni.2010.06.002",
         note="Lee et al. Immunity 2010 — inhibiting RICTOR impairs effector Th (opposes disease benefit)"),
    dict(system="immune (Treg)", model="Treg-intrinsic Rictor/Notch axis",
         phenotype="RICTOR activity destabilizes Foxp3/Treg (opposing direction)",
         translational_direction="cell_type_conflict", pmid="26437242", doi="10.1038/ni.3288",
         note="Charbonnier et al. Nat Immunol 2015 — opposing effect across immune cell types"),
    dict(system="cardiac", model="cardiomyocyte Rictor cKO", phenotype="contractile dysfunction under pressure overload",
         translational_direction="liability", pmid="26598511", doi="10.1093/cvr/cvv252",
         note="Shende et al. Cardiovasc Res 2016 — mTORC2 preserves function under stress"),
]

# --- Human genetics ----------------------------------------------------------
genetics = [
    dict(source="gnomAD v2.1.1", metric="pLI", value="~1.0", interpretation="LoF-intolerant",
         efficacy_support="NA", pmid="", url="https://gnomad.broadinstitute.org/gene/ENSG00000164327?dataset=gnomad_r2_1",
         note="strong loss-of-function constraint"),
    dict(source="gnomAD v2.1.1", metric="LOEUF (oe_lof_upper)", value="0.155", interpretation="high constraint (<0.35)",
         efficacy_support="NA", pmid="", url="https://gnomad.broadinstitute.org/gene/ENSG00000164327?dataset=gnomad_r2_1",
         note="o/e LoF point estimate 0.089"),
    dict(source="gnomAD v4", metric="LOEUF (oe_lof_upper)", value="0.289", interpretation="high constraint (<0.35)",
         efficacy_support="NA", pmid="", url="https://gnomad.broadinstitute.org/gene/ENSG00000164327?dataset=gnomad_r4",
         note="pLI 1.0 in v4"),
    dict(source="Open Targets v4 — rheumatoid arthritis (MONDO_0008383)", metric="overall association / genetic",
         value="0.004 / none", interpretation="literature text-mining only; no genetic_association",
         efficacy_support="NO", pmid="", url="https://platform.opentargets.org/target/ENSG00000164327",
         note="no GWAS / colocalization linking RICTOR to RA"),
    dict(source="Open Targets v4 — systemic lupus erythematosus (MONDO_0007915)", metric="overall association / genetic",
         value="0.025 / none", interpretation="literature only; no genetic evidence",
         efficacy_support="NO", pmid="", url="https://platform.opentargets.org/target/ENSG00000164327",
         note="no genetic support"),
    dict(source="Open Targets v4 — juvenile idiopathic arthritis (MONDO_0011429)", metric="evidence count",
         value="0", interpretation="no evidence of any type", efficacy_support="NO", pmid="",
         url="https://platform.opentargets.org/target/ENSG00000164327", note="no JIA association"),
    dict(source="locus confounding (5p13.1)", metric="neighbour genes", value="OSMR, FYB1/ADAP",
         interpretation="cis-pQTL/eQTL at the RICTOR locus may misattribute to OSMR or FYB1",
         efficacy_support="CAUTION", pmid="",
         url="https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000164327",
         note="OSMR overlaps RICTOR 5' end; FYB1 (T-cell adaptor) immediately downstream; require colocalization"),
]

# --- External-dataset shortlist (future validation plan only) ---------------
external = [
    dict(dataset="AMP RA/SLE Phase 1", accession="AMP-RA Phase 1",
         description="RA/OA synovial scRNA-seq + CyTOF + bulk + flow (51 samples)",
         role_in_future_validation="preferred same-tissue RA-vs-OA disease-direction comparator",
         priority="1_preferred", control_comparator="yes (RA vs OA)", causal_validation="no_observational",
         caveat="cross-sectional; RA not JIA", pmid="31061532", doi="10.1038/s41590-019-0378-1", url=""),
    dict(dataset="GSE118209", accession="GSE118209",
         description="MASC expanded effector CD4+ T-cell subset in RA; bulk RNA-seq of sorted CD4 (blood+synovium)",
         role_in_future_validation="fastest orthogonal CD4 concordance test",
         priority="2_high", control_comparator="partial", causal_validation="no_observational",
         caveat="bulk sorted populations, not single-cell", pmid="", doi="",
         url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE118209"),
    dict(dataset="GSE243917", accession="GSE243917",
         description="single-nucleus multimodal (RNA+ATAC) synovium; 11 RA + 1 OA",
         role_in_future_validation="supporting orthogonal (multiome) only",
         priority="4_low", control_comparator="OA n=1", causal_validation="no_observational",
         caveat="OA arm underpowered (n=1)", pmid="", doi="",
         url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243917"),
    dict(dataset="GSE202375", accession="GSE202375",
         description="pooled scRNA-seq of T cells from human synovial tissue (RA/OA; 5 samples)",
         role_in_future_validation="supporting / partial only",
         priority="4_low", control_comparator="limited", causal_validation="no_observational",
         caveat="small, pooled samples", pmid="", doi="",
         url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202375"),
    dict(dataset="AMP RA Phase 2", accession="AMP-RA Phase 2",
         description="deep synovial single-cell atlas (>314k cells, 79 donors, CTAP subtypes)",
         role_in_future_validation="depth (large atlas) but no matched RA-vs-OA control comparator",
         priority="3_medium", control_comparator="no", causal_validation="no_observational",
         caveat="deep but no within-study OA/healthy control comparator", pmid="37938773",
         doi="10.1038/s41586-023-06708-y", url=""),
]

if __name__ == "__main__":
    write(prior_art, "RICTOR_PRIOR_ART_TABLE.tsv")
    write(modality, "RICTOR_MODALITY_TABLE.tsv")
    write(safety, "RICTOR_SAFETY_LANDSCAPE.tsv")
    write(genetics, "RICTOR_HUMAN_GENETICS.tsv")
    write(external, "EXTERNAL_DATASET_SHORTLIST.tsv")
    print("Translational tables written to results/translational/.")
