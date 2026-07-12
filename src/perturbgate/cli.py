"""PerturbGate command-line interface.

Subcommands
    demo        recompute the headline reversal from compact frozen inputs,
                regenerate figures, and validate against the golden values
    reproduce   recompute guide / condition / LODO summaries from the Level-2
                pseudobulk inputs and compare to the frozen tables
    figures     (re)generate all figures + source data
    verify      schemas + golden values + claims + funnel + superseded guard
    manifest    write results/frozen/results_manifest.json (checksums + provenance)
    contract    print the analysis contract
"""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from . import GOLDEN, __version__, attrition, calibration, claim_ledger, figures
from .io import demo_dir, frozen_dir, load_disease_consistency, load_disease_vector, load_kd_meta, repo_root
from .provenance import checksum_tree, write_json
from .reversal import gsea_reversal, reversal
from .schemas import SCHEMAS, SchemaError

TARGETS = ["RICTOR", "PAK2", "RIPK1"]
TOL = 1e-3  # golden-value tolerance (documented in docs/REPRODUCIBILITY.md)


def _ok(msg): print(f"  [ok] {msg}")
def _fail(msg): print(f"  [FAIL] {msg}")


# ---------------------------------------------------------------- demo
def cmd_demo(_args) -> int:
    print(f"PerturbGate {__version__} - demo (Level 1: artifact reproduction)")
    out = repo_root() / "results" / "demo"
    out.mkdir(parents=True, exist_ok=True)
    disease = load_disease_vector()
    cons = load_disease_consistency()
    rows = []
    for t in TARGETS:
        kd = load_kd_meta(t)
        r = reversal(kd, disease)
        g = gsea_reversal(kd, disease, cons=cons)
        rows.append(dict(target=t, n_aligned=r.n, reversal_pearson=r.reversal_score,
                         pearson_p=r.pearson_p, reversal_spearman=r.reversal_spearman,
                         gsea_reversal=g["gsea_reversal"], n_reversed=r.n_reversed,
                         n_reinforced=r.n_reinforced))
    df = pd.DataFrame(rows)
    df.to_csv(out / "reversal_recomputed.tsv", sep="\t", index=False)
    print(df.to_string(index=False))

    # Matched-null empirical p recomputed from the frozen matched values.
    nullv = pd.read_csv(frozen_dir() / "rictor_matched_null_values.tsv", sep="\t")
    obs = float(GOLDEN["RICTOR_matched_substrate_reversal"])
    nres = calibration.empirical_p(obs, nullv["matched_reversal"].to_numpy())
    write_json(nres.as_dict(), out / "matched_null_recomputed.json")
    print(f"\n  matched-null: observed +{obs:.4f}; {nres.n_exceed}/{nres.n_null} exceed; "
          f"empirical p={nres.empirical_p:.4f}; Wilson95=({nres.wilson_low:.4f},{nres.wilson_high:.4f})")

    # Validate headline values against golden.
    problems = _check_golden(df, nres)
    print("\n  Regenerating figures ...")
    figures.make_all()
    _ok("figures written to figures/")
    summary = dict(version=__version__, targets=rows, matched_null=nres.as_dict(),
                   golden_ok=not problems, problems=problems)
    write_json(summary, out / "demo_summary.json")
    if problems:
        for p in problems:
            _fail(p)
        return 1
    _ok("all headline values within tolerance of frozen golden values")
    return 0


def _check_golden(df: pd.DataFrame, nres) -> list[str]:
    problems = []

    def close(a, b, tol=TOL):
        return abs(float(a) - float(b)) <= tol

    def getr(t):
        return df.loc[df.target == t].iloc[0]

    checks = [
        ("RICTOR reversal", getr("RICTOR")["reversal_pearson"], GOLDEN["RICTOR_reversal_pearson"]),
        ("RICTOR spearman", getr("RICTOR")["reversal_spearman"], GOLDEN["RICTOR_reversal_spearman"]),
        ("RICTOR n_aligned", getr("RICTOR")["n_aligned"], GOLDEN["RICTOR_n_aligned"]),
        ("PAK2 reversal", getr("PAK2")["reversal_pearson"], GOLDEN["PAK2_reversal_pearson"]),
        ("RIPK1 reversal", getr("RIPK1")["reversal_pearson"], GOLDEN["RIPK1_reversal_pearson"]),
        ("matched empirical_p", nres.empirical_p, GOLDEN["RICTOR_matched_empirical_p"]),
        ("matched exceedances", nres.n_exceed, GOLDEN["RICTOR_matched_exceedances"]),
    ]
    for name, got, exp in checks:
        if close(got, exp):
            _ok(f"{name} = {float(got):.6g} (golden {float(exp):.6g})")
        else:
            problems.append(f"{name} = {float(got):.6g} != golden {float(exp):.6g}")
    # Guard: RICTOR reversal must never be the superseded +0.43.
    if close(getr("RICTOR")["reversal_pearson"], GOLDEN["SUPERSEDED_RICTOR_reversal"], tol=0.05):
        problems.append("RICTOR reversal matches the SUPERSEDED +0.43 value")
    return problems


# ---------------------------------------------------------------- reproduce
def cmd_reproduce(_args) -> int:
    print(f"PerturbGate {__version__} - reproduce (Level 2: analytical reproduction)")
    repro_in = repo_root() / "data" / "reproduce"
    if not (repro_in / "pseudobulk_counts.parquet").exists():
        _fail("Level-2 inputs missing (data/reproduce/pseudobulk_counts.parquet). "
              "Run `make reproduce-data` or see docs/REPRODUCIBILITY_LEVELS.md.")
        return 2
    out = repo_root() / "results" / "reproduced"
    out.mkdir(parents=True, exist_ok=True)
    from .reproduce import recompute_guides_conditions_lodo
    rep = recompute_guides_conditions_lodo(repro_in, load_disease_vector())
    for name, df in rep.items():
        df.to_csv(out / f"{name}.tsv", sep="\t", index=False)
        _ok(f"reproduced {name} ({len(df)} rows)")
    # Compare guide reversal to frozen with tolerance.
    frozen_g = pd.read_csv(frozen_dir() / "rictor_guides.tsv", sep="\t").set_index("guide")["reversal_pearson"]
    rep_g = rep["rictor_guides"].set_index("guide")["reversal_pearson"]
    problems = []
    for guide, v in rep_g.items():
        if guide in frozen_g.index and abs(v - frozen_g[guide]) > 5e-3:
            problems.append(f"guide {guide}: reproduced {v:.4f} vs frozen {frozen_g[guide]:.4f}")
    if problems:
        for p in problems:
            _fail(p)
        return 1
    _ok("reproduced guide reversals within tolerance of frozen values")
    return 0


# ---------------------------------------------------------------- figures
def cmd_figures(_args) -> int:
    paths = figures.make_all()
    for p in paths:
        _ok(str(p.relative_to(repo_root())))
    return 0


# ---------------------------------------------------------------- verify
def cmd_verify(_args) -> int:
    print(f"PerturbGate {__version__} - verify")
    problems: list[str] = []

    # 1. Schemas
    for name, schema in SCHEMAS.items():
        try:
            schema.validate(pd.read_csv(frozen_dir() / f"{name}.tsv", sep="\t"))
            _ok(f"schema {name}")
        except (SchemaError, FileNotFoundError) as e:
            problems.append(str(e))
            _fail(str(e))

    # 2. Golden values (recompute from compact inputs)
    disease = load_disease_vector()
    df = pd.DataFrame([
        dict(target=t, **{k: v for k, v in reversal(load_kd_meta(t), disease).as_dict().items()})
        for t in TARGETS
    ]).rename(columns={"reversal_score": "reversal_pearson"})
    nullv = pd.read_csv(frozen_dir() / "rictor_matched_null_values.tsv", sep="\t")
    nres = calibration.empirical_p(GOLDEN["RICTOR_matched_substrate_reversal"], nullv["matched_reversal"].to_numpy())
    gp = _check_golden(df.assign(n_aligned=df["n"]), nres)
    problems += gp

    # 3. Claims resolve to artifacts
    cp = claim_ledger.resolve_claims(claim_ledger.load_claims())
    if cp:
        problems += cp
        for p in cp:
            _fail(p)
    else:
        _ok("all claims resolve to on-disk artifacts")

    # 4. Funnel + ledger consistency
    fn = pd.read_csv(frozen_dir() / "candidate_funnel.tsv", sep="\t")
    fp = attrition.check_funnel(fn)
    led = pd.read_csv(frozen_dir() / "rejection_ledger.tsv", sep="\t")
    lp = attrition.check_ledger_depths(led)
    if fp or lp:
        problems += fp + lp
        for p in fp + lp:
            _fail(p)
    else:
        _ok("candidate funnel denominators + ledger vocabulary consistent")

    # 5. Superseded guard
    sp = _superseded_guard()
    problems += sp

    if problems:
        print(f"\nVERIFY FAILED with {len(problems)} problem(s).")
        return 1
    print("\nVERIFY PASSED - schemas, golden values, claims, funnel and superseded guard all clean.")
    return 0


def _superseded_guard() -> list[str]:
    """No frozen table may present RICTOR at the superseded +0.43, and no public
    label outside the controlled vocabulary may appear."""
    problems = []
    pc = pd.read_csv(frozen_dir() / "primary_comparison.tsv", sep="\t")
    rictor = pc[pc.target == "RICTOR"].iloc[0]
    if abs(float(rictor["primary_reversal"]) - 0.43) < 0.05:
        problems.append("primary_comparison RICTOR reversal matches superseded +0.43")
        _fail(problems[-1])
    sup = json.load(open(frozen_dir() / "superseded_claims.json", encoding="utf-8"))
    if any(s.get("may_appear_in_readme", True) for s in sup):
        problems.append("a superseded claim is marked may_appear_in_readme=true")
        _fail(problems[-1])
    if not problems:
        _ok("superseded-value guard (no +0.43, no superseded claim promoted)")
    return problems


# ---------------------------------------------------------------- manifest
def cmd_manifest(_args) -> int:
    root = repo_root()
    checks = checksum_tree(root / "results" / "frozen")
    checks.pop("results_manifest.json", None)  # never checksum the manifest into itself
    demo_checks = checksum_tree(demo_dir())
    manifest = dict(
        version=__version__,
        frozen=checks,
        demo_inputs=demo_checks,
        note="sha256 of every frozen artifact and demo input; see docs/REPRODUCIBILITY.md",
    )
    write_json(manifest, frozen_dir() / "results_manifest.json")
    _ok(f"wrote results/frozen/results_manifest.json ({len(checks)} frozen + {len(demo_checks)} demo entries)")
    return 0


# ---------------------------------------------------------------- contract
def cmd_contract(_args) -> int:
    print((frozen_dir() / "analysis_contract.json").read_text(encoding="utf-8"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="perturbgate", description="Evidence-gated Perturb-seq mechanism pipeline")
    p.add_argument("--version", action="version", version=f"perturbgate {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    for name, fn in [("demo", cmd_demo), ("reproduce", cmd_reproduce), ("figures", cmd_figures),
                     ("verify", cmd_verify), ("manifest", cmd_manifest), ("contract", cmd_contract)]:
        sp = sub.add_parser(name)
        sp.set_defaults(func=fn)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
