"""IO helpers locate the repo and load compact inputs as gene-indexed series."""
import pandas as pd

from targetgate.io import demo_dir, frozen_dir, load_disease_vector, load_kd_meta, repo_root


def test_repo_root_has_frozen_dir():
    assert (repo_root() / "results" / "frozen").is_dir()
    assert frozen_dir().is_dir()


def test_disease_vector_is_gene_indexed_series():
    dv = load_disease_vector()
    assert isinstance(dv, pd.Series)
    assert len(dv) > 10000
    assert dv.index.astype(str).str.startswith("ENSG").mean() > 0.9


def test_kd_meta_loads_for_all_targets():
    for t in ("RICTOR", "PAK2", "RIPK1"):
        kd = load_kd_meta(t)
        assert isinstance(kd, pd.Series)
        assert len(kd) > 10000


def test_demo_inputs_present():
    assert (demo_dir() / "disease_vector_activated_memory.tsv.gz").exists()
    for t in ("RICTOR", "PAK2", "RIPK1"):
        assert (demo_dir() / f"kd_meta_{t}.tsv.gz").exists()
