"""Provenance: content hashing and results-manifest construction.

Every frozen artifact carries a sha256 so downstream consumers (and the release
audit) can detect drift. The manifest maps each public artifact to its checksum,
schema, generating command and the claim ids it supports.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def md5_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def checksum_tree(root: str | Path, patterns=("*.tsv", "*.json", "*.tsv.gz", "*.parquet")) -> dict[str, str]:
    """sha256 of every matching file under ``root`` (repo-relative keys, sorted)."""
    root = Path(root)
    out: dict[str, str] = {}
    for pat in patterns:
        for p in sorted(root.rglob(pat)):
            out[str(p.relative_to(root)).replace("\\", "/")] = sha256_file(p)
    return dict(sorted(out.items()))


def write_json(obj, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" writes LF on every platform so regenerated JSON is byte-stable.
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
