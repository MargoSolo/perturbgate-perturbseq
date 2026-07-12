"""The superseded registry must be complete, never README-promotable, and the
public outputs must never carry the superseded +0.43 RICTOR reversal."""
import json

import pandas as pd

from perturbgate.io import frozen_dir


def test_all_superseded_claims_blocked_from_readme():
    sup = json.load(open(frozen_dir() / "superseded_claims.json", encoding="utf-8"))
    assert len(sup) >= 5
    for s in sup:
        assert s["may_appear_in_readme"] is False


def test_superseded_registry_covers_the_key_five():
    sup = json.load(open(frozen_dir() / "superseded_claims.json", encoding="utf-8"))
    joined = " ".join(s["old_wording"].lower() for s in sup)
    assert "0.43" in joined                 # old RICTOR reversal
    assert "enrich" in joined               # PAK2 JIA enrichment
    assert "partial" in joined              # PAK2 partial inhibition
    assert "neighbour" in joined or "neighbor" in joined  # safer PAK2 neighbour
    assert "wasf2" in joined                # PAK2-WASF2 axis


def test_no_frozen_table_carries_the_superseded_reversal():
    pc = pd.read_csv(frozen_dir() / "primary_comparison.tsv", sep="\t")
    rictor = float(pc.loc[pc.target == "RICTOR", "primary_reversal"].iloc[0])
    assert abs(rictor - 0.43) > 0.2  # must be the +0.161 primary, never +0.43


def test_claims_reference_superseded_ids():
    claims = json.load(open(frozen_dir() / "claims.json", encoding="utf-8"))
    rictor = next(c for c in claims if c["entity"] == "RICTOR")
    assert "SUP-01" in rictor["superseded_claims"]
