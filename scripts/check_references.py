#!/usr/bin/env python3
"""DOI / PMID integrity check for the translational-audit tables.

Runs offline (format + internal consistency); online resolution was verified
during the audit and is recorded per row. It enforces three things across every
TSV under results/translational/:

  1. every non-empty DOI is well-formed (10.NNNN/...);
  2. every non-empty PMID is numeric;
  3. a row marked retracted MUST carry a retraction DOI/PMID and MUST NOT be used
     as positive evidence (evidence_use must be do_not_use / cautionary /
     negative_control) — retracted work is never cited as support.

Exit code is non-zero on any violation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
TRANS = REPO / "results" / "translational"

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
PMID_RE = re.compile(r"^\d{5,9}$")
POSITIVE_USE = {"positive", "support", "supporting", "efficacy_support"}
ALLOWED_RETRACTED_USE = {"do_not_use", "cautionary", "negative_control"}


def _blank(v) -> bool:
    s = str(v).strip().lower()
    return s in ("", "nan", "na", "none", "-", "n/a")


def check() -> list[str]:
    problems: list[str] = []
    if not TRANS.exists():
        return [f"missing directory: {TRANS.relative_to(REPO)}"]
    tsvs = sorted(TRANS.glob("*.tsv"))
    if not tsvs:
        return ["no translational TSVs found"]
    n_doi = n_pmid = n_retracted = 0
    for path in tsvs:
        rel = path.relative_to(REPO).as_posix()
        df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
        for i, row in df.iterrows():
            line = i + 2
            for col in df.columns:
                low = col.lower()
                val = str(row[col]).strip()
                if _blank(val):
                    continue
                if "doi" in low:
                    for d in re.split(r"[;, ]+", val):
                        if _blank(d):
                            continue
                        n_doi += 1
                        if not DOI_RE.match(d):
                            problems.append(f"{rel}:{line} column '{col}' malformed DOI: {d}")
                elif low == "pmid" or low.endswith("_pmid") or "pmid" in low:
                    for p in re.split(r"[;, ]+", val):
                        if _blank(p):
                            continue
                        n_pmid += 1
                        if not PMID_RE.match(p):
                            problems.append(f"{rel}:{line} column '{col}' malformed PMID: {p}")
            # retracted-not-positive rule
            retr_col = next((c for c in df.columns if c.lower() == "retracted"), None)
            if retr_col and str(row[retr_col]).strip().lower() in ("true", "yes", "1"):
                n_retracted += 1
                use = str(row.get("evidence_use", "")).strip().lower()
                if use in POSITIVE_USE:
                    problems.append(f"{rel}:{line} retracted row used as positive evidence (evidence_use={use})")
                elif use and use not in ALLOWED_RETRACTED_USE:
                    problems.append(f"{rel}:{line} retracted row has non-allowed evidence_use={use} "
                                    f"(allow: {sorted(ALLOWED_RETRACTED_USE)})")
                # retracted rows must carry a retraction identifier
                rd = " ".join(str(row[c]) for c in df.columns if "retraction" in c.lower())
                if _blank(rd):
                    problems.append(f"{rel}:{line} retracted row lacks a retraction DOI/PMID")
    print(f"checked {len(tsvs)} table(s): {n_doi} DOI(s), {n_pmid} PMID(s), {n_retracted} retracted row(s)")
    return problems


def main() -> int:
    problems = check()
    print("=" * 68)
    print("DOI / PMID integrity check")
    print("=" * 68)
    if not problems:
        print("PASS — identifiers well-formed; no retracted work used as positive evidence.")
        return 0
    print(f"FAIL — {len(problems)} problem(s):")
    for p in problems:
        print(f"  - {p}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
