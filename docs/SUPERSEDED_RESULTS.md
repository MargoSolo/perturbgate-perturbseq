# Superseded results

A central design principle of TargetGate is that **superseded interpretations are
kept, labelled, and corrected — not deleted.** This document is the human-readable
companion to [`results/frozen/superseded_claims.json`](../results/frozen/superseded_claims.json).
None of the old claims below may appear as a current finding anywhere in the public
outputs; the automated privacy audit (`scripts/public_readiness_audit.py`) enforces
this for the most important one (the old +0.43 RICTOR reversal).

For each entry: what the old interpretation was, why it was superseded, the
authoritative replacement, and the artifact that supports the correction.

---

## SUP-01 — RICTOR reversal ≈ +0.43

- **Old claim:** RICTOR knockdown reverses the disease direction at ≈ +0.43.
- **Source:** an old covariate-adjusted / residency-removed 77-gene subset with a
  responder-only knockdown representation.
- **Why superseded:** the value was inflated by the frozen-subset gene universe and
  the knockdown representation. The honest full-transcriptome centered-Pearson
  reversal is far smaller.
- **Authoritative replacement:** primary responder-resolved full-transcriptome
  reversal **+0.161**; conservative all-cell null-substrate projection **+0.131**.
- **Replacement artifacts:** `results/frozen/primary_comparison.tsv`,
  `results/frozen/matched_null.tsv`.
- **May appear in README:** never.

## SUP-02 — PAK2 programme enriched in JIA joint tissue (positive disease validation)

- **Old claim:** the PAK2 responder programme is enriched in JIA synovium, i.e.
  positive external disease validation.
- **Source:** a raw synovial enrichment in which all modules appeared up in synovium.
- **Why superseded:** after covariate adjustment (activation / proliferation / IFN /
  stress) and a matched-random-signature null, the FROZEN-UP and FROZEN-DOWN modules
  **co-elevate** (diverge = False) — a generic activation-confounded signal, not a
  disease-directional one.
- **Authoritative replacement:** PAK2 is **not disease-directionally supported**
  (disease_relevant = False).
- **Replacement artifacts:** `results/frozen/primary_comparison.tsv` (PAK2 reversal
  +0.010, p=0.297), rejection ledger.
- **May appear in README:** never.

## SUP-03 — Partial PAK2 inhibition supported

- **Old claim:** partial / bounded PAK2 inhibition is sufficient (a therapeutic-window
  claim).
- **Source:** a two-guide analysis interpreted as a titration.
- **Why superseded:** both PAK2 guides produce **similarly strong** knockdown
  (≈ 83–86%). There is no strong-vs-weak contrast, so partial-inhibition sufficiency
  cannot be assessed.
- **Authoritative replacement:** partial-inhibition sufficiency **NOT_ESTABLISHED**;
  the finding is `GUIDE_CONCORDANT_STRONG_KD_EFFECT`, with no dose-response and no
  therapeutic-window claim.
- **Replacement artifact:** `results/frozen/rejection_ledger.tsv`.
- **May appear in README:** never.

## SUP-04 — A safer PAK2 neighbour reproduces the programme

- **Old claim:** a safer, druggable neighbour of PAK2 reproduces its programme (an
  "escape target").
- **Source:** a global-cosine neighbour search (e.g. PTEN) rewarding broad similarity.
- **Why superseded:** a gene-ID namespace mismatch and incomplete essentiality /
  safety vetoes. The corrected search (ENSG→symbol fix, PAK2 self-exclusion, expanded
  vetoes, external essentiality/oncogenicity/tractability) finds **none**.
- **Authoritative replacement:** **no safer, druggable, immune-directional escape
  target** was identified in the screened universe.
- **Replacement artifact:** `results/frozen/rejection_ledger.tsv`.
- **May appear in README:** never.

## SUP-05 — PAK2–WASF2 is a supported therapeutic axis

- **Old claim:** PAK2–WASF2 is a high-confidence direct therapeutic interface.
- **Source:** structural / topology exploration (AlphaFold2 / AlphaFold3 modelling).
- **Why superseded:** structural and directional evidence did not establish a
  high-confidence direct therapeutic interface (the modelled interface was not a
  confident, stable interface in either method).
- **Authoritative replacement:** PAK2–WASF2 is **not** a validated therapeutic axis;
  the structural work is **not** the target-discovery result of this project.
- **Replacement artifact:** this document.
- **May appear in README:** never.

---

## How the correction is enforced

- The frozen [`superseded_claims.json`](../results/frozen/superseded_claims.json)
  marks every entry `may_appear_in_readme: false` and is validated by
  `tests/test_superseded_input_block.py`.
- `targetgate verify` guards that no frozen table carries the +0.43 RICTOR reversal
  and that no superseded claim is promoted.
- The privacy / public-readiness audit flags a +0.43 reversal appearing near RICTOR
  outside an explicitly-superseded context.

See also [FAILURE_MODES.md](FAILURE_MODES.md) for the analytical failure modes these
corrections address.
