"""Input / output helpers: locate the repo, load compact demo inputs and frozen
artifacts. All paths are repository-relative and configurable; nothing here reads
an absolute or server-specific location.
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


def repo_root() -> Path:
    """Repository root (the directory that contains ``results/frozen``).

    Honours ``TARGETGATE_ROOT`` for out-of-tree runs; otherwise walks up from this
    file until it finds the frozen-results marker.
    """
    env = os.environ.get("TARGETGATE_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "results" / "frozen").is_dir():
            return parent
    # Fall back to two levels up (src/targetgate/io.py -> repo).
    return here.parents[2]


def frozen_dir() -> Path:
    return repo_root() / "results" / "frozen"


def demo_dir() -> Path:
    return repo_root() / "data" / "demo"


def load_frozen(name: str) -> pd.DataFrame:
    """Load a frozen table by file name (with or without .tsv)."""
    if not name.endswith((".tsv", ".json")):
        name = name + ".tsv"
    path = frozen_dir() / name
    if not path.exists():
        raise FileNotFoundError(f"frozen artifact not found: {path}")
    return pd.read_csv(path, sep="\t")


def load_disease_vector() -> pd.Series:
    """Compact activated-memory disease direction (log2FC), indexed by gene id."""
    df = pd.read_csv(demo_dir() / "disease_vector_activated_memory.tsv.gz", sep="\t")
    return pd.Series(df["mean_logfc"].to_numpy(dtype=float), index=df["gene"].to_numpy())


def load_disease_consistency() -> pd.Series:
    df = pd.read_csv(demo_dir() / "disease_vector_activated_memory.tsv.gz", sep="\t")
    return pd.Series(df["donor_consistency"].to_numpy(dtype=float), index=df["gene"].to_numpy())


def load_kd_meta(target: str) -> pd.Series:
    """Compact responder-DE meta KD vector (log2FC) for a deep target."""
    path = demo_dir() / f"kd_meta_{target}.tsv.gz"
    if not path.exists():
        raise FileNotFoundError(f"KD meta not found for {target}: {path}")
    df = pd.read_csv(path, sep="\t")
    return pd.Series(df["lfc"].to_numpy(dtype=float), index=df["gene"].to_numpy())
