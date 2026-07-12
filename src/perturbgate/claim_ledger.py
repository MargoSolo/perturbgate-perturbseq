"""Claim ledger: resolve every public claim to a supporting artifact.

A public claim is not allowed to exist without (a) a controlled claim type,
(b) an evidence status, and (c) at least one supporting artifact that is present
on disk. ``resolve_claims`` returns the unresolved claims so the release audit can
fail loudly rather than let an unsupported statement ship.
"""
from __future__ import annotations

import json
from pathlib import Path

from .io import repo_root

REQUIRED_FIELDS = (
    "claim_id",
    "exact_public_wording",
    "entity",
    "claim_type",
    "evidence_status",
    "evidence_depth",
    "supporting_artifacts",
)


def load_claims(path: str | Path | None = None) -> list[dict]:
    path = Path(path) if path else repo_root() / "results" / "frozen" / "claims.json"
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def resolve_claims(claims: list[dict], root: str | Path | None = None) -> list[str]:
    """Return a list of problems; empty means every claim resolves to an artifact."""
    root = Path(root) if root else repo_root()
    problems: list[str] = []
    for c in claims:
        cid = c.get("claim_id", "<no id>")
        for f in REQUIRED_FIELDS:
            if f not in c or c[f] in (None, "", []):
                problems.append(f"claim {cid}: missing required field '{f}'")
        for art in c.get("supporting_artifacts", []):
            if not (root / art).exists():
                problems.append(f"claim {cid}: supporting artifact missing on disk: {art}")
    return problems
