"""Candidate attrition: reconcile the funnel and the rejection ledger against the
authoritative all-perturbation table.

The scientific point of TargetGate is that *ranking is not validation*. The funnel
records how many perturbations entered each gate, how many advanced, and how many
were not advanced / rejected / left unresolved — with a source artifact for every
count. This module checks the funnel's denominators are internally consistent and
that the ledger's vocabulary is honest (not-advanced != rejected-after-validation).
"""
from __future__ import annotations

import pandas as pd

from .schemas import EVIDENCE_DEPTHS


def check_funnel(funnel: pd.DataFrame) -> list[str]:
    """Return a list of human-readable problems; empty list means consistent."""
    problems: list[str] = []
    for _, r in funnel.iterrows():
        entering = int(r["n_entering"])
        parts = int(r["n_advanced"]) + int(r["n_not_advanced"]) + int(r["n_rejected"]) + int(r["n_unresolved"])
        if parts != entering:
            problems.append(
                f"stage {r['stage_id']} ({r['stage_name']}): advanced+not_advanced+rejected+"
                f"unresolved = {parts} != n_entering = {entering}"
            )
        if not str(r.get("source_artifact", "")).strip():
            problems.append(f"stage {r['stage_id']}: missing source_artifact")
    return problems


def check_ledger_depths(ledger: pd.DataFrame) -> list[str]:
    problems: list[str] = []
    bad = set(ledger["evidence_depth"].dropna().unique()) - EVIDENCE_DEPTHS
    if bad:
        problems.append(f"rejection_ledger has evidence_depth outside vocabulary: {sorted(bad)}")
    # A "REJECTED_AFTER_DEEP_VALIDATION" row must actually be DEEP.
    mism = ledger[
        (ledger["final_evidence_class"] == "REJECTED_AFTER_DEEP_VALIDATION")
        & (ledger["evidence_depth"] != "DEEP")
    ]
    if len(mism):
        problems.append(
            f"{len(mism)} row(s) labelled REJECTED_AFTER_DEEP_VALIDATION but not evidence_depth=DEEP"
        )
    return problems


def screen_counts(all_perturbations: pd.DataFrame) -> dict:
    """Recompute the screen-level denominators from the authoritative table so the
    funnel can be checked against them."""
    df = all_perturbations
    return {
        "n_total": int(len(df)),
        "n_convergent_fdr": int((df["screen_level_status"] == "CONVERGENT_FDR<0.10").sum()),
        "n_shortlist_vetted": int((df["evidence_depth"] == "SHORTLIST_VETTED").sum()),
        "n_deep": int((df["evidence_depth"] == "DEEP").sum()),
        "n_retained": int((df["final_evidence_class"] == "RETAINED_MECHANISM_HYPOTHESIS").sum()),
        "n_rejected_deep": int((df["final_evidence_class"] == "REJECTED_AFTER_DEEP_VALIDATION").sum()),
    }
