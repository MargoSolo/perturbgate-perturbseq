"""Code-generated, colour-blind-safe figures.

Every figure is produced from the frozen artifacts, writes a matching source-data
TSV to ``figures/source_data/``, and is saved as both PNG and SVG. The palette is
Okabe-Ito (colour-blind safe) and no conclusion is encoded by colour alone —
status cells always carry a text symbol as well.

Legends live in ``docs/FIGURE_LEGENDS.md``.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from .io import frozen_dir, repo_root

# --- Okabe-Ito colour-blind-safe palette ------------------------------------
OI = {
    "orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73", "yellow": "#F0E442",
    "blue": "#0072B2", "vermillion": "#D55E00", "purple": "#CC79A7",
    "black": "#000000", "grey": "#999999", "light": "#DDDDDD",
}
STATUS = {
    "PASS": ("✓", OI["green"]), "FAIL": ("✗", OI["vermillion"]),
    "BORDERLINE": ("~", OI["orange"]), "NOT_ESTABLISHED": ("?", OI["grey"]),
    "NOT_EVALUATED": ("–", OI["light"]), "TRANSLATIONAL_GAP": ("△", OI["blue"]),
}


def _style() -> None:
    plt.rcParams.update({
        "font.size": 11, "font.family": "DejaVu Sans", "axes.titlesize": 12,
        "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 120,
        "svg.fonttype": "none", "axes.titleweight": "bold",
        # Fixed salt makes SVG element ids deterministic across renders, so
        # `make demo` does not dirty the committed figures.
        "svg.hashsalt": "perturbgate",
    })


def _fig_dir() -> Path:
    d = repo_root() / "figures"
    (d / "source_data").mkdir(parents=True, exist_ok=True)
    return d


def _save(fig, stem: str) -> list[Path]:
    d = _fig_dir()
    out = []
    for ext in ("png", "svg"):
        p = d / f"{stem}.{ext}"
        # metadata Date=None suppresses the non-deterministic timestamp in SVG/PNG.
        meta = {"Date": None} if ext == "svg" else {"Software": None}
        fig.savefig(p, bbox_inches="tight", dpi=200 if ext == "png" else None, metadata=meta)
        if ext == "svg":  # force LF so the repo stays clean on Windows and Linux
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
        out.append(p)
    plt.close(fig)
    return out


def _source(df: pd.DataFrame, stem: str) -> None:
    # lineterminator + newline="" write LF (not platform CRLF) so source data is byte-stable.
    with open(_fig_dir() / "source_data" / f"{stem}.tsv", "w", encoding="utf-8", newline="") as fh:
        df.to_csv(fh, sep="\t", index=False, lineterminator="\n")


# =====================================================================
# Figure 1 — Target attrition through evidence gates
# =====================================================================
def figure_1_target_attrition() -> list[Path]:
    _style()
    fn = pd.read_csv(frozen_dir() / "candidate_funnel.tsv", sep="\t")
    _source(fn, "figure_1_target_attrition")
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_title("Target attrition through evidence gates\n"
                 "From 924 perturbations to a small set of evidence-gated mechanism hypotheses",
                 loc="left")

    def box(x, y, w, h, text, color, tcolor="black"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                    linewidth=1.2, edgecolor=OI["black"], facecolor=color, alpha=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.2, color=tcolor)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                                     color=OI["grey"], linewidth=1.4))

    # Screen-wide spine (left column)
    box(0.3, 8.3, 3.4, 1.3, "924 perturbations\nscreen-level reversal scoring", OI["sky"])
    box(0.3, 6.2, 3.4, 1.3, "208 convergent + FDR<0.10\n(716 not advanced)", OI["sky"])
    box(0.3, 4.1, 3.4, 1.3, "21 biologically robust\n(187 broad / donor-unstable)", OI["sky"])
    box(0.3, 2.0, 3.4, 1.3, "0 advanceable\n21 safety / modality constrained", OI["orange"])
    box(0.3, 0.3, 3.4, 1.1, "single-state screen:\nNO_ROBUST_CANDIDATE", OI["light"])
    for y in (8.3, 6.2, 4.1):
        arrow(2.0, y, 2.0, y - 0.8)
    arrow(2.0, 2.0, 2.0, 1.4)

    ax.text(6.0, 9.55, "Candidate-specific deep validation (branches)", fontsize=10.5,
            fontweight="bold", ha="left", color=OI["black"])
    # PAK2 branch
    box(4.5, 7.7, 3.3, 1.5, "PAK2 (lead)\ntechnical validation PASS\ntherapeutic direction FAIL", OI["vermillion"], "white")
    box(8.2, 7.7, 3.4, 1.5, "REJECTED\nreproducible cellular hit,\nnot therapeutically directional", OI["light"])
    arrow(7.8, 8.45, 8.2, 8.45)
    # RICTOR branch
    box(4.5, 5.4, 3.3, 1.5, "RICTOR (bounded rescue)\n7 strong criteria PASS\n+ borderline matched-null", OI["green"], "white")
    box(8.2, 5.4, 3.4, 1.5, "RETAINED mechanism node\nwith modality gap\n(+0.161; 11/11 LODO)", OI["light"])
    arrow(7.8, 6.15, 8.2, 6.15)
    # RIPK1 branch
    box(4.5, 3.1, 3.3, 1.4, "RIPK1 (comparator)\nweak / incoherent reversal", OI["grey"], "white")
    box(8.2, 3.1, 3.4, 1.4, "COMPARATOR ONLY\nnot directionally supported\nin this analysis", OI["light"])
    arrow(7.8, 3.8, 8.2, 3.8)

    ax.text(6.0, 1.7, "Ranking is not validation: a real perturbation effect is necessary but not "
            "sufficient for target nomination.", fontsize=9, style="italic", ha="left", color=OI["black"])
    ax.text(6.0, 1.05, "Denominators and reasons: results/frozen/candidate_funnel.tsv + rejection_ledger.tsv",
            fontsize=8, ha="left", color=OI["grey"])
    return _save(fig, "figure_1_target_attrition")


# =====================================================================
# Figure 2 — Directionality and matched-null calibration
# =====================================================================
def figure_2_directionality_and_null() -> list[Path]:
    _style()
    pc = pd.read_csv(frozen_dir() / "primary_comparison.tsv", sep="\t")
    guides = pd.read_csv(frozen_dir() / "rictor_guides.tsv", sep="\t")
    lodo = pd.read_csv(frozen_dir() / "rictor_lodo.tsv", sep="\t")
    cond = pd.read_csv(frozen_dir() / "rictor_conditions.tsv", sep="\t")
    nullv = pd.read_csv(frozen_dir() / "rictor_matched_null_values.tsv", sep="\t")
    le = pd.read_csv(frozen_dir() / "leading_edge.tsv", sep="\t")
    _source(pc[["target", "primary_reversal", "primary_pearson_p", "matched_substrate_reversal",
                "matched_percentile", "matched_empirical_p"]], "figure_2_directionality_and_null")

    fig = plt.figure(figsize=(12, 8.4))
    gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.28)

    # Panel A — primary responder-resolved reversal
    axA = fig.add_subplot(gs[0, 0])
    order = ["RICTOR", "PAK2", "RIPK1"]
    vals = [float(pc.loc[pc.target == t, "primary_reversal"].iloc[0]) for t in order]
    cols = [OI["green"], OI["vermillion"], OI["grey"]]
    axA.bar(order, vals, color=cols, edgecolor="black", linewidth=1)
    axA.axhline(0, color="black", linewidth=0.8)
    for i, (t, v) in enumerate(zip(order, vals, strict=False)):
        p = float(pc.loc[pc.target == t, "primary_pearson_p"].iloc[0])
        axA.text(i, v + 0.006, f"{v:+.3f}\np={p:.2g}", ha="center", va="bottom", fontsize=8.5)
    axA.set_title("A  Primary responder-resolved reversal")
    axA.set_ylabel("reversal = −centered Pearson(KD, disease)")
    axA.set_ylim(-0.03, 0.20)

    # Panel B — matched-null calibration
    axB = fig.add_subplot(gs[0, 1])
    obs = float(pc.loc[pc.target == "RICTOR", "matched_substrate_reversal"].iloc[0])
    axB.hist(nullv["matched_reversal"], bins=24, color=OI["sky"], edgecolor="white", alpha=0.9,
             label=f"matched null (n={len(nullv)})")
    n_exceed = int((nullv["matched_reversal"] >= obs).sum())
    axB.axvline(obs, color=OI["green"], linewidth=2.2, label=f"RICTOR +{obs:.3f}")
    axB.set_title("B  Matched-perturbation null (conservative substrate)")
    axB.set_xlabel("all-cell effect-vector reversal")
    axB.set_ylabel("matched perturbations")
    axB.legend(fontsize=8, loc="upper left")
    axB.text(0.98, 0.95,
             f"{n_exceed}/{len(nullv)} exceed RICTOR\npercentile 96.5 (global 97.9)\n"
             f"empirical p=0.040\nWilson 95% CI 0.017–0.070",
             transform=axB.transAxes, ha="right", va="top", fontsize=8,
             bbox=dict(boxstyle="round", facecolor="white", edgecolor=OI["grey"]))

    # Panel C — guide + LODO + condition robustness
    axC = fig.add_subplot(gs[1, 0])
    labels, values, colors = [], [], []
    for _, r in guides.iterrows():
        labels.append(r["guide"]); values.append(float(r["reversal_pearson"])); colors.append(OI["green"])
    for _, r in cond.iterrows():
        labels.append(f"cond:{r['condition']}"); values.append(float(r["reversal_pearson"])); colors.append(OI["blue"])
    folds = lodo[lodo["fold"] != "ALL"]["reversal_pearson"].astype(float)
    labels.append(f"LODO 11 folds\n[{folds.min():.3f}, {folds.max():.3f}]")
    values.append(float(folds.mean())); colors.append(OI["orange"])
    y = np.arange(len(labels))
    axC.barh(y, values, color=colors, edgecolor="black", linewidth=0.8)
    axC.axvline(0, color="black", linewidth=0.8)
    axC.set_yticks(y); axC.set_yticklabels(labels, fontsize=8.5)
    axC.invert_yaxis()
    axC.set_title("C  RICTOR guide / condition / donor robustness", loc="left")
    axC.set_xlabel("reversal")

    # Panel D — leading edge (descriptive)
    axD = fig.add_subplot(gs[1, 1])
    up = le[le["arm"] == "disease_up"].head(8)
    yr = np.arange(len(up))
    axD.barh(yr, up["kd_lfc"].astype(float), color=OI["green"], edgecolor="black", linewidth=0.6)
    axD.set_yticks(yr); axD.set_yticklabels(up["symbol"], fontsize=8)
    axD.invert_yaxis()
    axD.axvline(0, color="black", linewidth=0.8)
    axD.set_title("D  Leading edge: disease-UP genes RICTOR turns DOWN", loc="left")
    axD.set_xlabel("RICTOR KD log2FC (descriptive, not independently validated)")
    fig.suptitle("RICTOR disease-state reversal: effect size, denominator and uncertainty "
                 "(not a p-value alone)", fontsize=12.5, fontweight="bold", y=0.98)
    return _save(fig, "figure_2_directionality_and_null")


# =====================================================================
# Figure 3 — Gate matrix
# =====================================================================
def figure_3_gate_matrix() -> list[Path]:
    _style()
    gm = pd.read_csv(frozen_dir() / "gate_matrix.tsv", sep="\t")
    _source(gm, "figure_3_gate_matrix")
    cols = [c for c in gm.columns if c != "row_label"]
    col_labels = [c.replace("_", " ") for c in cols]
    rows = gm["row_label"].tolist()
    fig, ax = plt.subplots(figsize=(13, 4.6))
    ax.set_xlim(0, len(cols)); ax.set_ylim(0, len(rows))
    ax.set_xticks(np.arange(len(cols)) + 0.5)
    ax.set_xticklabels(col_labels, rotation=40, ha="right", fontsize=8.2)
    ax.set_yticks(np.arange(len(rows)) + 0.5)
    ax.set_yticklabels(rows[::-1], fontsize=9)
    for i, (_, r) in enumerate(gm.iterrows()):
        yy = len(rows) - 1 - i
        for j, c in enumerate(cols):
            val = str(r[c])
            sym, color = STATUS.get(val, ("", OI["light"]))
            ax.add_patch(plt.Rectangle((j, yy), 1, 1, facecolor=color, edgecolor="white", alpha=0.55))
            txt = sym if c != "final_public_decision" else val.replace("_", "\n")
            ax.text(j + 0.5, yy + 0.5, txt, ha="center", va="center",
                    fontsize=(11 if c != "final_public_decision" else 6.0),
                    color="black", fontweight="bold" if c != "final_public_decision" else "normal")
    ax.set_title("Gate matrix — biological evidence vs translational readiness "
                 "(symbols, not colour alone)", loc="left")
    handles = [plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=col, markersize=12,
                          label=f"{sym} {k}") for k, (sym, col) in STATUS.items()]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.005, 1.0), fontsize=8, frameon=False)
    ax.set_xticks(np.arange(len(cols) + 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    return _save(fig, "figure_3_gate_matrix")


# =====================================================================
# Figure 4 — PAK2 rejection case study
# =====================================================================
def figure_4_pak2_rejection() -> list[Path]:
    _style()
    src = pd.DataFrame([
        dict(side="technical", step="on-target knockdown", detail="both guides ~83–86% KD", verdict="PASS"),
        dict(side="technical", step="guide reproducibility", detail="concordance 0.85, 100% direction", verdict="PASS"),
        dict(side="technical", step="donor reproducibility", detail="112-gene programme donor + LODO robust", verdict="PASS"),
        dict(side="technical", step="real responder population", detail="Mixscape responder fraction 76.5%", verdict="PASS"),
        dict(side="technical", step="reproducible programme", detail="frozen 112-gene responder signature", verdict="PASS"),
        dict(side="therapeutic", step="inflammatory direction restored", detail="NF-κB Δ=−0.011, p=0.05, negligible", verdict="FAIL"),
        dict(side="therapeutic", step="disease-state reversal", detail="+0.010, p=0.297 (n.s.); 41st pctile", verdict="FAIL"),
        dict(side="therapeutic", step="external JIA enrichment", detail="UP & DOWN co-elevate: activation confound", verdict="FAIL"),
        dict(side="therapeutic", step="partial-inhibition sufficiency", detail="both guides strong: not established", verdict="NOT_ESTABLISHED"),
        dict(side="therapeutic", step="safer druggable escape", detail="0/10 pass veto stack", verdict="FAIL"),
    ])
    _source(src, "figure_4_pak2_rejection")
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 6.2))
    fig.suptitle("PAK2 — a real perturbation hit is not sufficient for target nomination",
                 fontsize=13, fontweight="bold", y=1.0)

    def panel(ax, side, title, color):
        rows = src[src.side == side].reset_index(drop=True)
        ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, len(rows) + 1.5)
        ax.text(0.2, len(rows) + 0.7, title, fontsize=11.5, fontweight="bold", color=color)
        for i, r in rows.iterrows():
            yy = len(rows) - 1 - i + 0.3
            sym, scol = STATUS.get(r["verdict"], ("", OI["grey"]))
            ax.add_patch(FancyBboxPatch((0.2, yy), 9.4, 0.82, boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor=scol, alpha=0.16, edgecolor=scol, linewidth=1.1))
            ax.text(0.5, yy + 0.41, sym, fontsize=13, va="center", ha="center", color=scol, fontweight="bold")
            ax.text(1.1, yy + 0.52, r["step"], fontsize=9.2, va="center", fontweight="bold")
            ax.text(1.1, yy + 0.22, r["detail"], fontsize=8.0, va="center", color="#333333")

    panel(axL, "technical", "Technical validation — PASSED", OI["green"])
    panel(axR, "therapeutic", "Therapeutic validation — FAILED", OI["vermillion"])
    fig.text(0.5, -0.02,
             "PAK2 passed technical validation but failed therapeutic validation → "
             "REPRODUCIBLE_CELLULAR_HIT_NOT_THERAPEUTICALLY_DIRECTIONAL",
             ha="center", fontsize=9.5, style="italic")
    return _save(fig, "figure_4_pak2_rejection")


# =====================================================================
# Supplementary — RICTOR robustness forest
# =====================================================================
def supplementary_rictor_robustness() -> list[Path]:
    _style()
    pc = pd.read_csv(frozen_dir() / "primary_comparison.tsv", sep="\t")
    lodo = pd.read_csv(frozen_dir() / "rictor_lodo.tsv", sep="\t")
    conf = pd.read_csv(frozen_dir() / "confound_decomposition.tsv", sep="\t")
    r = pc[pc.target == "RICTOR"].iloc[0]
    folds = lodo[lodo["fold"] != "ALL"]["reversal_pearson"].astype(float)
    conf_removed = conf[conf["removed"] == "cellcycle+activation+broaddown"]["reversal_pearson"].astype(float).iloc[0]
    rows = [
        ("primary raw-count vector", float(r["primary_reversal"]), None),
        ("adjusted-vector sensitivity", 0.147, None),
        ("RICTOR guide 1", float(r["guide_1_reversal"]), None),
        ("RICTOR guide 2", float(r["guide_2_reversal"]), None),
        ("disease-donor LODO (11)", float(folds.mean()), (folds.min(), folds.max())),
        ("responder-only mean", 0.054, None),
        ("condition: Rest", float(r["condition_rest"]), None),
        ("condition: Stim8hr", float(r["condition_stim8"]), None),
        ("condition: Stim48hr", float(r["condition_stim48"]), None),
        ("confound-removed (cc+act+broad)", float(conf_removed), None),
        ("matched-null substrate", float(r["matched_substrate_reversal"]), None),
    ]
    _source(pd.DataFrame(rows, columns=["track", "reversal", "range"]), "supplementary_rictor_robustness")
    fig, ax = plt.subplots(figsize=(9.5, 6.4))
    y = np.arange(len(rows))
    for i, (_lab, v, rng) in enumerate(rows):
        col = OI["green"] if v > 0 else OI["vermillion"]
        ax.plot([0, v], [i, i], color=OI["light"], linewidth=1)
        ax.scatter([v], [i], color=col, s=55, zorder=3)
        if rng is not None:
            ax.plot([rng[0], rng[1]], [i, i], color=OI["orange"], linewidth=3, alpha=0.6, zorder=2)
        ax.text(v + 0.004, i, f"{v:+.3f}", va="center", fontsize=8.5)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("reversal (−centered Pearson)")
    ax.set_title("Supplementary — RICTOR reversal across representations and controls\n"
                 "positive on every track; adjusted-vector is same-cohort sensitivity, not independent replication",
                 loc="left", fontsize=10.5)
    ax.set_xlim(-0.02, 0.22)
    return _save(fig, "supplementary_rictor_robustness")


# =====================================================================
# Supplementary — gate ablation
# =====================================================================
def supplementary_gate_ablation() -> list[Path]:
    _style()
    ab = pd.read_csv(frozen_dir() / "gate_ablation.tsv", sep="\t")
    _source(ab, "supplementary_gate_ablation")
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, len(ab) + 1)
    ax.set_title("Supplementary — process ablation: what would survive if one gate were removed\n"
                 "(frozen decisions only; no threshold changes; not a causal-importance claim)",
                 loc="left", fontsize=11)
    for i, row in ab.iterrows():
        yy = len(ab) - 1 - i
        ax.add_patch(FancyBboxPatch((0.2, yy + 0.1), 3.4, 0.78, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor=OI["orange"], alpha=0.2, edgecolor=OI["orange"]))
        ax.text(1.9, yy + 0.5, "– " + row["gate_removed"].replace("_", " "), ha="center", va="center", fontsize=8.4)
        ax.add_patch(FancyArrowPatch((3.65, yy + 0.5), (4.1, yy + 0.5), arrowstyle="-|>",
                                     mutation_scale=11, color=OI["grey"]))
        ax.text(4.25, yy + 0.62, row["what_would_survive"], ha="left", va="center", fontsize=8.2, fontweight="bold")
        ax.text(4.25, yy + 0.28, f"e.g. {row['example_entities']} — {row['why_misleading']}",
                ha="left", va="center", fontsize=7.2, color="#333333")
    return _save(fig, "supplementary_gate_ablation")


ALL_FIGURES = [
    figure_1_target_attrition,
    figure_2_directionality_and_null,
    figure_3_gate_matrix,
    figure_4_pak2_rejection,
    supplementary_rictor_robustness,
    supplementary_gate_ablation,
]


def make_all() -> list[Path]:
    out: list[Path] = []
    for fn in ALL_FIGURES:
        out.extend(fn())
    return out
