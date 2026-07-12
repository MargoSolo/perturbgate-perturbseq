# Demo video script

**Project:** TargetGate — Evidence-Gated Pipeline for T-cell Perturb-seq Mechanism Hypotheses
**Version:** 1.0.0 (frozen hackathon release, 2026-07-13)
**Event:** Built with Claude: Life Sciences (Anthropic x Gladstone Institutes), Research track
**Target length:** up to 3:00 (hard cap 3:00)
**Deliverable:** one screen-recorded walkthrough with voiceover and burned-in captions

---

## How to use this script

This is a shot-by-shot recording script. Each section gives:

- **Voiceover** — read verbatim; timings assume roughly 150 words per minute.
- **Screen** — what the viewer sees (figure, terminal, or document).
- **Commands** — exact commands to run live on screen during that section.
- **Caption** — burned-in on-screen text for silent viewing (short, one or two lines).

All numbers below are quoted from the frozen release under
[`results/frozen/`](../results/frozen/) and match [RESULTS.md](RESULTS.md),
[METHODS.md](METHODS.md), and [DECISION_TRAIL.md](DECISION_TRAIL.md). Do not paraphrase the
controlled labels. Nothing on screen may show a compute-cluster name, hostname, username, home
path, or job id — refer only to a "server" or "compute server".

**Central message to land:** a real perturbation effect is necessary but not sufficient for a
target nomination. TargetGate records not only which hypothesis survived, but why the competing
claims failed.

### Timing map

| Time | Section | Screen |
|------|---------|--------|
| 0:00–0:20 | The problem | Title card |
| 0:20–0:45 | Challenge and dataset | Dataset card |
| 0:45–1:10 | Figure 1 — attrition | `figures/figure_1_target_attrition.png` |
| 1:10–1:40 | PAK2 — "real but wrong" | `figures/figure_4_pak2_rejection.png` |
| 1:40–2:15 | RICTOR validation | `figures/figure_2_directionality_and_null.png` + terminal |
| 2:15–2:35 | Translation boundary | `docs/TRANSLATIONAL_REVIEW_STATUS.md` |
| 2:35–2:55 | Reproducibility | Terminal (`make demo`, `make verify`) |
| 2:55–3:00 | Closing line | Title card |

### Pre-recording checklist

- [ ] `make demo` has been run once so `results/demo/` and figures exist (see the [fallback](#fallback-if-live-server-output-is-unavailable) if the environment is offline).
- [ ] Terminal prompt is generic — no username, hostname, or home path visible. Set the prompt to `$` and `cd` into the repo before recording.
- [ ] Font size large enough to read at 1080p; light-on-dark or dark-on-light with high contrast.
- [ ] Open in advance: the four PNGs in [`figures/`](../figures/), [RESULTS.md](RESULTS.md), and [TRANSLATIONAL_REVIEW_STATUS.md](TRANSLATIONAL_REVIEW_STATUS.md).
- [ ] Mute notifications; hide any window that could reveal private paths or the server name.

---

## 0:00–0:20 — The problem

**Voiceover:**
> A Perturb-seq screen can knock down every gene in a T cell and tell you which ones change the
> transcriptome. But a hit is not a drug target. A perturbation can be real, reproducible, and
> completely non-toxic — and still push the cell in the wrong direction, or in no therapeutic
> direction at all. The hard part is not finding an effect. It is deciding which effect deserves
> to be nominated.

**Screen:** Title card — "TargetGate: an evidence-gated pipeline for T-cell Perturb-seq mechanism
hypotheses." Subtitle: "A Perturb-seq hit is not automatically a drug target."

**Commands:** none (static title card).

**Caption:**
`A Perturb-seq hit is not automatically a drug target.`
`Finding an effect is easy. Nominating a target is not.`

---

## 0:20–0:45 — The challenge and the dataset

**Voiceover:**
> The challenge was to find new drug targets in a human CD4 T-cell Perturb-seq dataset from the
> Marson and Pritchard labs — a genome-scale screen across resting and stimulated conditions.
> We asked a target-nomination question, not a gene-ranking one: does knocking a gene down move
> T cells against a real disease signature? For that signature we used an independent juvenile
> idiopathic arthritis synovial atlas — inflamed joint versus blood, in activated-memory CD4
> cells. Both datasets are fully open.

**Screen:** Dataset card listing the two inputs, each with its label and license:

- **Perturb-seq:** Human CD4+ T Cell Perturb-seq (Marson lab + Pritchard lab), bioRxiv DOI 10.64898/2025.12.23.696273, MIT license.
- **Disease vector:** JIA synovial single-cell atlas "Integrated global cells" (Knight et al., bioRxiv DOI 10.64898/2026.05.01.716870), CZ CELLxGENE, CC-BY-4.0.

**Commands (optional, if showing the manifest instead of a card):**
```
cat data/public_data_manifest.tsv
```

**Caption:**
`Perturb-seq: human CD4+ T cells (Marson + Pritchard labs).`
`Disease signature: independent JIA synovium-vs-blood atlas. Both open.`
`Question asked: target NOMINATION, not gene ranking.`

---

## 0:45–1:10 — Figure 1: the attrition

**Voiceover:**
> Here is what survives. We scored 924 perturbations against the disease vector. 208 were
> convergent and passed a false-discovery threshold; the other 716 did not advance. Of those,
> 21 were biologically robust across donors — but every one was constrained by safety,
> essentiality, or the lack of a credible drug modality. So the single-state screen produced no
> clean advanceable candidate. This is not a funnel where everything is pushed through one pipe.
> It is a branching decision map, and most branches end in a documented rejection.

**Screen:** [`figures/figure_1_target_attrition.png`](../figures/figure_1_target_attrition.png).
Slowly zoom from 924 down through 208, then 21, then the deep candidate branch.

**Commands (optional):**
```
column -t -s $'\t' results/frozen/candidate_funnel.tsv
```

**Caption:**
`924 scored -> 208 convergent + FDR<0.10 -> 21 robust -> 0 clean advanceable.`
`Branching decision map, not a linear funnel. Most branches end in a recorded rejection.`

> Note for the reader: do not say or imply that all 924 perturbations underwent every deep test.
> The deep validation applies to the named candidate branch (PAK2, RICTOR, RIPK1). Denominators
> trace to [`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv) and
> [`rejection_ledger.tsv`](../results/frozen/rejection_ledger.tsv).

---

## 1:10–1:40 — PAK2: real but wrong

**Voiceover:**
> PAK2 is the case that makes the point. It passed technical validation cleanly: on-target
> knockdown of about 83 to 86 percent for both guides, guide concordance of 0.85 with fully
> consistent direction, a 112-gene responder programme robust across donors and guides, and it
> was non-toxic. Every reason to like it. Then it failed the therapeutic test. Its disease
> reversal was +0.010, not significant at p equals 0.297, sitting at the 41st percentile of a
> matched-perturbation null. The external disease enrichment turned out to be an activation
> confound — up and down modules co-elevated. So PAK2 is a reproducible cellular hit that is not
> therapeutically directional. We rejected it as a nomination, and we kept the record of why.

**Screen:** [`figures/figure_4_pak2_rejection.png`](../figures/figure_4_pak2_rejection.png). Split
emphasis: technical panel (passes) on one side, therapeutic panel (fails) on the other.

**Commands (optional):**
```
grep -E "target|PAK2" results/frozen/primary_comparison.tsv | column -t -s $'\t'
```

**Caption:**
`PAK2 PASSED technical validation: ~83-86% KD, 0.85 guide concordance, 112-gene robust program, non-toxic.`
`PAK2 FAILED therapeutic validation: reversal +0.010, p=0.297, 41st-percentile null; enrichment activation-confounded.`
`Label: REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL.`

---

## 1:40–2:15 — RICTOR: bounded validation with honest uncertainty

**Voiceover:**
> RICTOR is what a retained hypothesis looks like. Against pre-specified criteria fixed before we
> saw the raw-count result, its responder-resolved reversal was +0.161 across nearly eleven
> thousand aligned genes — turning down disease-up genes like CXCR6, CCL4, and IFNG. Both guides
> were positive, +0.141 and +0.178. All eleven disease-donor leave-one-out folds stayed positive,
> in a tight band from +0.154 to +0.167. It reversed in all three conditions. Then the honest
> part: against a matched-perturbation null, RICTOR reached the 96.5th percentile, but 7 of 200
> matched controls still beat it — an empirical p around 0.040 with borderline finite-pool
> uncertainty. So RICTOR satisfied seven strong convergence checks and nominally exceeded a
> matched null. We report that boundary, we do not erase it.

**Screen:** [`figures/figure_2_directionality_and_null.png`](../figures/figure_2_directionality_and_null.png),
then cut to a terminal showing the RICTOR robustness tables.

**Commands (run live):**
```
column -t -s $'\t' results/frozen/rictor_guides.tsv
column -t -s $'\t' results/frozen/rictor_lodo.tsv
column -t -s $'\t' results/frozen/rictor_conditions.tsv
column -t -s $'\t' results/frozen/matched_null.tsv
```

**Caption:**
`RICTOR reversal +0.161 (centered-Pearson, p=1.8e-63, ~10,832 genes; Spearman +0.100).`
`Both guides positive (+0.141 / +0.178). 11/11 disease-donor LODO folds positive (+0.154..+0.167). Positive in all 3 conditions.`
`Matched null: 96.5th percentile, 7/200 controls exceed RICTOR, empirical p~0.040 (borderline).`
`Seven strong convergence checks + nominal exceedance of a matched null. Label: DISEASE_REVERSING_MECHANISM_NODE_WITH_MODALITY_GAP.`

> Note for the reader: never state "8/8 decisive criteria." Criterion 8 — clearing the matched
> null — is the weakest and most marginal. Preferred wording: "RICTOR satisfied seven strong
> convergence checks and nominally exceeded a matched-perturbation null, with borderline
> finite-pool uncertainty." Keep the responder-resolved score (+0.161) and the conservative
> all-cell null-substrate score (+0.131) in separate spaces; do not mix them on screen.

---

## 2:15–2:35 — The translation boundary

**Voiceover:**
> This is where we stop, on purpose. RICTOR is a disease-reversing mechanism node with a modality
> gap. It is not a validated drug target. Systemic RICTOR inhibition is not shown to be safe, no
> selective small-molecule modality exists, and synovium-versus-blood is not disease-versus-
> healthy. The point of TargetGate is to hand a downstream biologist a hypothesis with its
> boundary already drawn — the mechanism, the caveats, and the specific evidence that is still
> missing.

**Screen:** [`docs/TRANSLATIONAL_REVIEW_STATUS.md`](TRANSLATIONAL_REVIEW_STATUS.md), scrolled to
the "what we do not claim" boundary; briefly show [LIMITATIONS.md](LIMITATIONS.md).

**Commands (optional):**
```
sed -n '1,40p' docs/TRANSLATIONAL_REVIEW_STATUS.md
```

**Caption:**
`RICTOR is NOT a validated drug target. No selective modality exists (the modality gap).`
`Synovium-vs-blood is not disease-vs-healthy. The boundary is part of the deliverable.`

---

## 2:35–2:55 — Reproducibility

**Voiceover:**
> All of this is reproducible. `make demo` runs on a laptop in minutes from compact committed
> inputs — no server, no private data — and recomputes the RICTOR, PAK2, and RIPK1 reversals,
> regenerating the tables and figures against golden values. `make verify` is the composite gate:
> it rebuilds the demo outputs and figures, revalidates schemas, golden values, claims, and
> labels, runs the tests, and scans the whole repository for any forbidden private content.

**Screen:** terminal. Run the demo, let it finish, then run verify (or show its tail if long).

**Commands (run live):**
```
make demo
make verify
```

**Caption:**
`make demo — laptop, minutes, no server or private data; recomputes reversals + figures vs golden values.`
`make verify — checksums, schemas, golden values, claims, labels, tests, and a private-content audit.`

---

## 2:55–3:00 — Closing line

**Voiceover:**
> TargetGate does not just report which hypothesis survived. It records why the competing claims
> failed.

**Screen:** return to the title card; fade the closing line in over it.

**Commands:** none.

**Caption:**
`TargetGate does not just report which hypothesis survived. It records why the competing claims failed.`

---

## Fallback if live server output is unavailable

Nothing in this demo requires the compute server. Level 1 (`make demo`) and `make verify` run
entirely from committed inputs. If the recording environment cannot run commands live, or a
command errors on camera, use these substitutions and keep the voiceover unchanged:

- **Instead of running `make demo` / `make verify` live:** show the pre-generated outputs already
  in the repository — the four figures in [`figures/`](../figures/) and the frozen tables in
  [`results/frozen/`](../results/frozen/) — and narrate them as "here is what those commands
  produce." State on screen that the outputs are the frozen 1.0.0 release.
- **Instead of the RICTOR terminal tables:** display the same numbers from
  [RESULTS.md](RESULTS.md) or [`primary_comparison.tsv`](../results/frozen/primary_comparison.tsv)
  as a static screenshot.
- **Instead of Figure 1 zoom:** show [`candidate_funnel.tsv`](../results/frozen/candidate_funnel.tsv)
  as text.
- **If any command must be shown but cannot run:** show the command in the terminal, then cut to
  the committed artifact it would generate. Never fabricate console output — display the real
  frozen artifact instead.
- **Do not** show the Level 3 `make full` path on camera; it requires the compute server and
  large downloads, and nothing in this script depends on it.

Every figure and table referenced here already exists in the frozen release, so the entire demo
can be recorded with zero live computation if needed.

---

## Full caption sheet (silent viewing)

For a version cut with no audio, these captions in sequence carry the story:

1. A Perturb-seq hit is not automatically a drug target.
2. Perturb-seq (Marson + Pritchard labs) scored against an independent, open JIA disease signature. Target nomination, not gene ranking.
3. 924 scored -> 208 convergent + FDR<0.10 -> 21 robust -> 0 clean advanceable. A branching decision map, not a funnel.
4. PAK2 passed technical validation (~83-86% KD, 0.85 concordance, 112-gene robust program, non-toxic)...
5. ...but failed therapeutic validation (reversal +0.010, p=0.297, 41st-percentile null; enrichment activation-confounded). Rejected, with the record kept.
6. RICTOR reversal +0.161 (p=1.8e-63); both guides positive; 11/11 LODO folds positive (+0.154..+0.167); positive in all 3 conditions.
7. Matched null: 96.5th percentile, but 7/200 controls exceed RICTOR (empirical p~0.040). Seven strong checks + a nominal null exceedance — boundary reported.
8. RICTOR is a disease-reversing mechanism node with a modality gap — not a validated drug target.
9. Reproducible: make demo (laptop, minutes) and make verify (composite gate + private-content audit).
10. TargetGate does not just report which hypothesis survived. It records why the competing claims failed.

---

## Related documentation

- [RESULTS.md](RESULTS.md) — full result tables and the three controlled labels.
- [METHODS.md](METHODS.md) — disease vector, pseudobulk, reversal metric, matched-null design.
- [DECISION_TRAIL.md](DECISION_TRAIL.md) — the branching decision map behind Figure 1.
- [TRANSLATIONAL_REVIEW_STATUS.md](TRANSLATIONAL_REVIEW_STATUS.md) and [LIMITATIONS.md](LIMITATIONS.md) — the translation boundary.
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and [REPRODUCIBILITY_LEVELS.md](REPRODUCIBILITY_LEVELS.md) — `make demo` / `make verify` / `make full`.
- [SUPERSEDED_RESULTS.md](SUPERSEDED_RESULTS.md) — claims that must never be presented as current (e.g. the old RICTOR +0.43).
- [CLAUDE_USAGE.md](CLAUDE_USAGE.md) — how Claude Code and Claude Science were used.
