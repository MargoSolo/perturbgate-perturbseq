"""External same-disease concordance: GSE160097 (paired JIA synovial-fluid vs blood memory CD4).

Reuses ``perturbgate.reversal.reversal`` and the committed compact KD vectors
(``data/demo/kd_meta_*.tsv.gz``) to reproduce the external directional-concordance
result of the frozen RICTOR/PAK2/RIPK1 signatures against an EXTERNAL public JIA
disease direction, with no detected donor overlap with the internal cohort
(see ``results/external_validation/gse160097/cohort_independence_audit.tsv``).

This is external same-disease, paired-compartment transcriptional concordance -
NOT causal replication, an external RICTOR perturbation, therapeutic validation,
or evidence that RICTOR is a validated drug target.

Two routes (contract in ``results/external_validation/gse160097/analysis_contract.json``):

  * OFFLINE (default) -- recompute the reversal, paired leave-one-donor-pair-out,
    paired bootstrap and the supplementary figure from committed, legally
    redistributable DERIVED aggregates (per-gene disease vector + per-donor-pair
    log2FC) and the committed KD vectors. No raw data, no network.
  * DOWNLOAD (``--download``) -- fetch the official public GSE160097 10x
    ``filtered_gene_bc_matrices`` H5 files from GEO (URLs + sha256 documented in
    ``docs/EXTERNAL_CONCORDANCE_GSE160097.md``) and rebuild the raw-count paired
    pseudobulk disease vector before rescoring. Raw H5 files are NOT redistributed
    here (GEO redistribution terms are not explicitly stated); only the official
    download route and derived summaries are provided.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from ..io import load_kd_meta, repo_root
from ..provenance import write_json
from ..reversal import reversal

TARGETS = ["RICTOR", "PAK2", "RIPK1"]
SEED = 0
N_BOOT = 1000
TOL = 1.5e-3

#: golden external values (frozen; validated by tests/test_external_gse160097.py)
GOLDEN = {
    "RICTOR_reversal": 0.1649,
    "RICTOR_reversal_spearman": 0.1025,
    "RICTOR_n_aligned": 14806,
    "PAK2_reversal": 0.0015,
    "RIPK1_reversal": -0.0068,
    "n_donor_pairs": 6,
    "internal_reference": 0.161,
}


def ext_dir() -> Path:
    return repo_root() / "results" / "external_validation" / "gse160097"


def load_disease_vector() -> pd.Series:
    df = pd.read_csv(ext_dir() / "gse160097_sf_vs_pb_cd4mem_disease_vector.tsv", sep="\t")
    return pd.Series(df["effect_SF_minus_PB"].to_numpy(dtype=float), index=df["gene_id"].to_numpy())


def load_paired_logfc() -> pd.DataFrame:
    """Per-donor-pair SF-minus-PB log2FC (genes x 6 donor pairs); a derived aggregate."""
    df = pd.read_csv(ext_dir() / "donor_paired_logfc_tcon.tsv.gz", sep="\t")
    return df.set_index("gene_id")


def _score(kd: pd.Series, disease: pd.Series) -> float | None:
    r = reversal(kd, disease)
    return None if r is None else r.reversal_score


def run(download: bool = False, write: bool = True) -> dict:
    if download:  # pragma: no cover - network path, documented full-data route
        disease, logfc = _download_and_rebuild()
    else:
        disease = load_disease_vector()
        logfc = load_paired_logfc()
    kds = {t: load_kd_meta(t) for t in TARGETS}
    donors = list(logfc.columns)

    # primary
    prim = {}
    for t in TARGETS:
        r = reversal(kds[t], disease)
        prim[t] = dict(reversal=r.reversal_score, reversal_spearman=r.reversal_spearman,
                       pearson_p=r.pearson_p, n_aligned=r.n)

    # paired leave-one-donor-pair-out
    lodo = {}
    for d in donors:
        eff = logfc[[c for c in donors if c != d]].mean(axis=1)
        lodo[d] = _score(kds["RICTOR"], eff)
    lodo_vals = np.array(list(lodo.values()))

    # paired donor bootstrap (resample donor pairs with replacement)
    rng = np.random.default_rng(SEED)
    boot = []
    for _ in range(N_BOOT):
        samp = list(rng.choice(donors, size=len(donors), replace=True))
        eff = logfc[samp].mean(axis=1)
        if np.std(eff.to_numpy()) < 1e-9:
            continue
        boot.append(_score(kds["RICTOR"], eff))
    boot = np.array([b for b in boot if b is not None and np.isfinite(b)])

    result = dict(
        primary=prim,
        lodo=lodo,
        lodo_all_positive=bool(np.all(lodo_vals > 0)),
        bootstrap=dict(median=float(np.median(boot)), p2_5=float(np.percentile(boot, 2.5)),
                       p97_5=float(np.percentile(boot, 97.5)), frac_positive=float((boot > 0).mean()),
                       n_draws=int(len(boot))),
        n_donor_pairs=len(donors),
        internal_reference=GOLDEN["internal_reference"],
    )
    if write:
        out = ext_dir() / "recomputed"
        out.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([dict(candidate=t, **prim[t]) for t in TARGETS]).to_csv(
            out / "candidate_external_concordance.tsv", sep="\t", index=False)
        pd.DataFrame([dict(dropped=d, reversal=v) for d, v in lodo.items()]).to_csv(
            out / "paired_lodo.tsv", sep="\t", index=False)
        write_json(result, out / "recomputed_summary.json")
        _make_figure(prim, lodo, boot)
    return result


def validate(result: dict) -> list[str]:
    problems = []

    def close(a, b, tol=TOL):
        return abs(float(a) - float(b)) <= tol

    checks = [
        ("RICTOR reversal", result["primary"]["RICTOR"]["reversal"], GOLDEN["RICTOR_reversal"]),
        ("RICTOR spearman", result["primary"]["RICTOR"]["reversal_spearman"], GOLDEN["RICTOR_reversal_spearman"]),
        ("PAK2 reversal", result["primary"]["PAK2"]["reversal"], GOLDEN["PAK2_reversal"]),
        ("RIPK1 reversal", result["primary"]["RIPK1"]["reversal"], GOLDEN["RIPK1_reversal"]),
    ]
    for name, got, exp in checks:
        if not close(got, exp):
            problems.append(f"{name} = {float(got):.6g} != golden {float(exp):.6g}")
    if result["primary"]["RICTOR"]["n_aligned"] != GOLDEN["RICTOR_n_aligned"]:
        problems.append(f"RICTOR n_aligned {result['primary']['RICTOR']['n_aligned']} != {GOLDEN['RICTOR_n_aligned']}")
    if not result["lodo_all_positive"]:
        problems.append("paired LODO not 6/6 positive")
    if result["bootstrap"]["frac_positive"] < 0.999:
        problems.append(f"paired bootstrap frac_positive {result['bootstrap']['frac_positive']} < 1.0")
    if result["bootstrap"]["p2_5"] <= 0:
        problems.append("paired bootstrap 2.5th percentile not > 0")
    return problems


def _write_tsv_lf(df: pd.DataFrame, path: Path) -> None:
    """Write a TSV byte-identically across Linux/macOS/Windows: explicit LF, no index."""
    text = df.to_csv(sep="\t", index=False, lineterminator="\n")
    path.write_bytes(text.encode("utf-8"))  # bytes -> no OS newline translation


def _make_figure(prim: dict, lodo: dict, boot: np.ndarray) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from .. import figures as _figs
    _figs._style()  # deterministic rcParams (svg.hashsalt) shared with the main figures

    order = ["RICTOR", "PAK2", "RIPK1"]
    vals = [prim[t]["reversal"] for t in order]
    lodo_donors = list(lodo.keys())            # stable donor order (patients 1,2,4,5,6,7)
    lodo_vals = np.array([lodo[d] for d in lodo_donors])
    b_med = float(np.median(boot)); b_lo = float(np.percentile(boot, 2.5)); b_hi = float(np.percentile(boot, 97.5))
    frac_pos = float((boot > 0).mean())

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    xs = np.arange(3)
    colors = ["#1BA7FF", "#9aa0a6", "#c4c8cc"]
    ax.bar(xs, vals, color=colors, width=0.52, edgecolor="black", lw=0.6, zorder=2)
    ax.axhline(0, color="black", lw=0.8)
    ax.axhline(GOLDEN["internal_reference"], color="#DA2828", ls="--", lw=1.3, zorder=1,
               label=f"internal reversal (+{GOLDEN['internal_reference']:.3f})")

    # RICTOR: paired-bootstrap 95% CI (left offset) + six individual LODO points (right offset) — no overlap
    x_ci, x_lodo = -0.20, 0.20
    ax.errorbar([x_ci], [b_med], yerr=[[b_med - b_lo], [b_hi - b_med]], fmt="o", ms=4,
                color="#08306B", ecolor="#08306B", capsize=4, lw=1.4, zorder=4,
                label="bootstrap median + 95% CI")
    # deterministic tiny horizontal spread so the six points do not stack
    xj = x_lodo + np.linspace(-0.06, 0.06, len(lodo_vals))
    ax.scatter(xj, lodo_vals, s=26, color="#1BA7FF", edgecolor="black", lw=0.5, zorder=5,
               label="6 leave-one-pair-out")
    # value labels: RICTOR lifted clear above the CI/points; comparators next to their bars
    ax.text(xs[0], b_hi + 0.016, f"{vals[0]:+.3f}", ha="center", va="bottom", fontsize=9, zorder=6)
    ax.text(xs[1], vals[1] + 0.010, f"{vals[1]:+.3f}", ha="center", va="bottom", fontsize=9, zorder=6)
    ax.text(xs[2], vals[2] - 0.014, f"{vals[2]:+.3f}", ha="center", va="top", fontsize=9, zorder=6)

    ax.set_xticks(xs); ax.set_xticklabels(order)
    ax.set_ylabel("reversal score (-centered Pearson)")
    ax.set_ylim(min(-0.03, min(vals) - 0.03), max(lodo_vals.max(), b_hi, GOLDEN["internal_reference"]) + 0.055)
    ax.set_title("External paired JIA compartment concordance (GSE160097)\n"
                 "synovial-fluid - blood memory CD4; + = knockdown opposes the joint programme", fontsize=9.5)
    ax.text(0.5, -0.185,
            f"n=6 donor pairs; leave-one-pair-out 6/6 positive; paired bootstrap median {b_med:+.3f}, "
            f"95% CI [{b_lo:+.3f}, {b_hi:+.3f}], {frac_pos*100:.0f}% of bootstrap draws positive. "
            "Observational concordance; not causal/therapeutic validation.",
            transform=ax.transAxes, ha="center", va="top", fontsize=7, color="#444")
    ax.legend(fontsize=7.5, loc="center right", framealpha=0.95)
    plt.tight_layout()
    figdir = repo_root() / "figures"
    sdir = figdir / "source_data"; sdir.mkdir(parents=True, exist_ok=True)
    paths = _figs._save(fig, "supplementary_external_jia_concordance")  # deterministic PNG+SVG
    plt.close(fig)

    # Source data: tidy key/value, ALL values rounded to fixed precision + explicit LF, so the
    # file is byte-identical on Linux/macOS/Windows (guards the CI byte-stability check).
    def r6(x):
        return round(float(x), 6)
    rows = [("external_reversal_RICTOR", r6(prim["RICTOR"]["reversal"])),
            ("external_reversal_PAK2", r6(prim["PAK2"]["reversal"])),
            ("external_reversal_RIPK1", r6(prim["RIPK1"]["reversal"])),
            ("internal_reference", r6(GOLDEN["internal_reference"]))]
    rows += [(f"lodo_RICTOR_drop_{d.replace(' ', '_')}", r6(lodo[d])) for d in lodo_donors]
    rows += [("bootstrap_RICTOR_median", r6(b_med)), ("bootstrap_RICTOR_ci_low", r6(b_lo)),
             ("bootstrap_RICTOR_ci_high", r6(b_hi)), ("bootstrap_RICTOR_frac_positive", r6(frac_pos))]
    _write_tsv_lf(pd.DataFrame(rows, columns=["metric", "value"]),
                  sdir / "supplementary_external_jia_concordance.tsv")
    return paths


#: official public GEO 10x filtered-matrix H5 for the 6 paired Tcon donors (raw UMI).
#: raw files are NOT redistributed; sha256 + full table in docs/EXTERNAL_CONCORDANCE_GSE160097.md.
_GEO_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM4859nnn"
_TCON_H5 = [
    ("JIA patient 1", "SF", "GSM4859835", "GSM4859835_PM1_CD4_SF_p1_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 2", "SF", "GSM4859836", "GSM4859836_PM1_CD4_SF_p2_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 4", "SF", "GSM4859838", "GSM4859838_PM1_CD4_SF_p4_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 5", "SF", "GSM4859839", "GSM4859839_PM1_CD4_SF_p5_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 6", "SF", "GSM4859840", "GSM4859840_PM1_CD4_SF_p6_filtered_feature_bc_matrix.h5"),
    ("JIA patient 7", "SF", "GSM4859841", "GSM4859841_PM1_CD4_SF_p7_filtered_feature_bc_matrix.h5"),
    ("JIA patient 1", "PB", "GSM4859842", "GSM4859842_PM4_CD4_blood_p1_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 2", "PB", "GSM4859843", "GSM4859843_PM4_CD4_blood_p2_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 4", "PB", "GSM4859844", "GSM4859844_PM4_CD4_blood_p4_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 5", "PB", "GSM4859845", "GSM4859845_PM4_CD4_blood_p5_filtered_gene_bc_matrices_h5.h5"),
    ("JIA patient 6", "PB", "GSM4859846", "GSM4859846_PM4_CD4_blood_p6_filtered_feature_bc_matrix.h5"),
    ("JIA patient 7", "PB", "GSM4859847", "GSM4859847_PM4_CD4_blood_p7_filtered_feature_bc_matrix.h5"),
]
_MIN_GENES = 200


def _download_and_rebuild():  # pragma: no cover - network / full-data route
    """Official-route rebuild from public GSE160097 raw 10x H5 (documented, not redistributed).

    Downloads the 6-pair Tcon filtered matrices from GEO, rebuilds the raw-count paired
    SF-minus-PB disease vector + per-donor-pair log2FC identically to the committed
    derived aggregates, and returns (disease_series, logfc_dataframe). Requires h5py.
    See docs/EXTERNAL_CONCORDANCE_GSE160097.md for the per-file sha256 to verify downloads.
    """
    import urllib.request

    import h5py
    from scipy import sparse

    cache = ext_dir() / "downloads" / "h5"
    cache.mkdir(parents=True, exist_ok=True)

    def load(gsm, fname):
        p = cache / f"{gsm}.h5"
        if not p.exists() or p.stat().st_size < 1000:
            urllib.request.urlretrieve(f"{_GEO_BASE}/{gsm}/suppl/{fname}", p)
        with h5py.File(p, "r") as f:
            keys = list(f.keys())
            if "matrix" in keys:  # CellRanger v3
                m = f["matrix"]; ens = [x.decode().split(".")[0] for x in m["features"]["id"][:]]
                M = sparse.csc_matrix((m["data"][:], m["indices"][:], m["indptr"][:]), shape=tuple(m["shape"][:]))
            else:  # v2
                g = f[keys[0]]; ens = [x.decode().split(".")[0] for x in g["genes"][:]]
                M = sparse.csc_matrix((g["data"][:], g["indices"][:], g["indptr"][:]), shape=tuple(g["shape"][:]))
        genes_per_cell = np.asarray((M > 0).sum(axis=0)).ravel()
        umi = np.asarray(M[:, genes_per_cell >= _MIN_GENES].sum(axis=1)).ravel()
        return pd.Series(umi, index=ens).groupby(level=0).sum()

    pb = {f"{pt}||{comp}": load(gsm, fn) for pt, comp, gsm, fn in _TCON_H5}
    allg = sorted(set().union(*[set(s.index) for s in pb.values()]))
    PB = pd.DataFrame({k: s.reindex(allg).fillna(0.0) for k, s in pb.items()})
    donors = ["JIA patient 1", "JIA patient 2", "JIA patient 4", "JIA patient 5", "JIA patient 6", "JIA patient 7"]

    def log2cpm(v):
        tot = v.sum()
        return np.log2(v / tot * 1e6 + 1) if tot > 0 else v * 0.0

    logfc = pd.DataFrame({p: log2cpm(PB[f"{p}||SF"].to_numpy()) - log2cpm(PB[f"{p}||PB"].to_numpy())
                          for p in donors}, index=allg)
    sf = PB[[f"{p}||SF" for p in donors]].sum(axis=1); pbt = PB[[f"{p}||PB" for p in donors]].sum(axis=1)
    logfc = logfc[(sf > 0) | (pbt > 0)]
    disease = logfc.mean(axis=1)
    return disease, logfc


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="perturbgate.external.gse160097",
                                 description="GSE160097 external same-disease concordance")
    ap.add_argument("--download", action="store_true",
                    help="rebuild from official public GEO raw H5 (documented route) instead of committed derived aggregates")
    args = ap.parse_args(argv)
    print("PerturbGate - external same-disease concordance (GSE160097)")
    result = run(download=args.download)
    r = result["primary"]
    print(f"  RICTOR external reversal = {r['RICTOR']['reversal']:+.4f} "
          f"(internal reference +{GOLDEN['internal_reference']:.3f}); n_aligned={r['RICTOR']['n_aligned']}")
    print(f"  PAK2 = {r['PAK2']['reversal']:+.4f} | RIPK1 = {r['RIPK1']['reversal']:+.4f}")
    print(f"  paired LODO {sum(v>0 for v in result['lodo'].values())}/{len(result['lodo'])} positive; "
          f"range [{min(result['lodo'].values()):+.4f}, {max(result['lodo'].values()):+.4f}]")
    b = result["bootstrap"]
    print(f"  paired bootstrap median {b['median']:+.4f}, 95% CI [{b['p2_5']:+.4f}, {b['p97_5']:+.4f}], "
          f"frac_positive {b['frac_positive']:.3f}")
    problems = validate(result)
    if problems:
        for p in problems:
            print(f"  [FAIL] {p}")
        return 1
    print("  [ok] external golden values reproduced; figure + recomputed tables written")
    print("  evidence class: SAME_DISEASE_PAIRED_COMPARTMENT_CONCORDANCE_SUPPORTED "
          "(observational; not causal/therapeutic/target validation)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
