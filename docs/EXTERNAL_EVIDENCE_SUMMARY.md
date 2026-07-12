# External evidence summary

PerturbGate keeps three axes explicitly separate. The external GSE160097 result adds evidence on the **external-evidence** axis only; it does **not** change the biological classification or the translational stop.

| Axis | Status |
|---|---|
| **Biological classification** | `DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP` |
| **External evidence** | `SAME_DISEASE_PAIRED_COMPARTMENT_CONCORDANCE_SUPPORTED` |
| **Translational readiness** | `NOT_ADVANCEABLE_WITH_CURRENT_EVIDENCE_AND_MODALITIES` |

## What the external evidence is

The frozen RICTOR-knockdown signature showed **external same-disease, paired-compartment transcriptional concordance** with an external public JIA synovial-fluid-versus-blood memory-CD4 direction (GSE160097): external reversal **+0.165** vs the internal **+0.161**; **6/6** positive leave-one-donor-pair-out; paired-bootstrap 95% interval **+0.113 … +0.191** excluding zero; PAK2 and RIPK1 near zero; the signal driven by an inflammatory effector programme rather than a generic egress module. Details: [EXTERNAL_CONCORDANCE_GSE160097.md](EXTERNAL_CONCORDANCE_GSE160097.md).

**Cohort-independence:** `NO_OVERLAP_DETECTED_BUT_NOT_FULLY_VERIFIABLE` — reported as *"an external public JIA cohort with no detected donor overlap"*, never "independent" (both cohorts share the Charité/DRFZ Berlin ecosystem and are de-identified).

## What it is not

Not replicated therapeutic efficacy, therapeutic/causal replication, clinical validation, a validated drug target, an independent RICTOR *perturbation* experiment, or proof that RICTOR inhibition treats JIA. The disease vector is observational (a compartment contrast, not disease-vs-healthy), rests on six donor pairs, and involved no RICTOR perturbation.

## Why the translational stop is unchanged

Stronger biological + external evidence does **not** move the translational axis: no validated RICTOR-selective modality exists, human genetics provides no efficacy support and indicates loss-of-function constraint, and systemic safety is constrained by essentiality and opposing cell-type effects. See [TRANSLATIONAL_AUDIT_UPDATE.md](TRANSLATIONAL_AUDIT_UPDATE.md).
