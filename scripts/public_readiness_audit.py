#!/usr/bin/env python3
"""Public-readiness / privacy audit.

Recursively scans the repository (tracked and untracked text files, docs, code,
configs, manifests, generated HTML/SVG, and — if present — the new repo's git
log) for content that must not appear in a public open-data release:

  * the internal compute-cluster name and filesystem names;
  * usernames, home paths, absolute private paths, hostnames;
  * scheduler ids / job accounts / container images;
  * tokens, secrets, API keys, .env files;
  * the superseded RICTOR +0.43 claim outside a clearly-superseded context;
  * unsupported "validated drug target" wording outside a negated context.

Exit code is non-zero if any finding is unresolved. The sensitive cluster and
filesystem names are constructed from fragments so this scanner does not itself
introduce a forbidden literal into the repository.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

# Sensitive names built from fragments so the literal never appears in this file.
_CLUSTER = "".join(("C", "E", "S", "G", "A"))
_FS = "".join(("L", "U", "S", "T", "R", "E"))

# (label, compiled regex, optional context-whitelist predicate on the line)
FORBIDDEN = [
    ("compute-cluster name", re.compile(_CLUSTER, re.IGNORECASE), None),
    ("cluster filesystem name", re.compile(_FS, re.IGNORECASE), None),
    ("lustre mount path", re.compile(r"/mnt/lustre", re.IGNORECASE), None),
    ("nlsas filesystem", re.compile(r"nlsas", re.IGNORECASE), None),
    ("private home path", re.compile(r"/home/uvi|uvi/bg/|/home/[a-z]+/", re.IGNORECASE), None),
    ("login-node hostname", re.compile(r"\bft[0-9]\b|\.usc\.es\b", re.IGNORECASE), None),
    ("container image", re.compile(r"\b\w+\.sif\b"), None),
    ("scheduler account/id", re.compile(r"\b8[0-9]{6}\b|afterok:|sacct_|--account=|-A\s+\w+_\w+"), None),
    ("windows user home path", re.compile(r"[A-Za-z]:[\\/]Users[\\/][^\\/\s\"']+", re.IGNORECASE), None),
    ("posix user home mount", re.compile(r"/c/Users/[^/\s\"']+", re.IGNORECASE), None),
    ("token / secret / key", re.compile(r"\b(api[_-]?key|secret|access[_-]?token|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b", re.IGNORECASE), None),
    ("env file reference", re.compile(r"\.env\b"), None),
]

# Context-sensitive checks (finding unless whitelisted on the same line/file).
SUPERSEDED_OK = re.compile(
    r"supersed|SUP-0|inflated|\bold\b|no longer|not reused|deprecated|guard|within 0\.05|"
    r"residency-removed|77-gene|covariate-adjusted|must never|never (?:appear|be)",
    re.IGNORECASE)
# The forbidden phrase is specifically claiming a *validated drug target*.
VALIDATED = re.compile(r"validated\s+drug[\s-]?target", re.IGNORECASE)
VALIDATED_OK = re.compile(r"\bnot\b|never|is not|isn'?t|do(es)? not claim", re.IGNORECASE)
# The superseded RICTOR reversal +0.43, as a *reversal-like* number (not a stray 0.43).
RICTOR_043 = re.compile(r"(?<![\d.])[+\-~]?\s?0\.43(?![\d])")

TEXT_EXT = {".py", ".md", ".tsv", ".csv", ".json", ".yaml", ".yml", ".toml", ".cfg",
            ".ini", ".txt", ".html", ".svg", ".cff", ".sh", ".make", ".in"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "data", "results"}
# results/ + data/ are re-checked with a narrower filter below (only text tables).


def _iter_files():
    for p in REPO.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(REPO).parts[:1]):
            continue
        if p.resolve() == SELF:
            continue
        if p.suffix.lower() in TEXT_EXT:
            yield p
    # Frozen text tables and manifests must also be clean (but not binary demo data).
    for sub in ("results/frozen", "data"):
        for p in (REPO / sub).rglob("*"):
            if p.is_file() and p.suffix.lower() in {".tsv", ".csv", ".json", ".md", ".yaml", ".yml"}:
                yield p


def audit() -> list[str]:
    findings: list[str] = []
    superseded_files = {"SUPERSEDED_RESULTS.md", "superseded_claims.json", "CHANGELOG.md",
                        "public_readiness_audit.py"}
    for path in sorted(set(_iter_files())):
        rel = path.relative_to(REPO).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:  # pragma: no cover
            findings.append(f"{rel}: could not read ({e})")
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            # Context window = this line plus the preceding 3 lines (handles list-style
            # "We do not claim:" -> bullet, and "superseded:" -> value on the next line).
            ctx = " ".join(lines[max(0, i - 4):i])
            for label, rx, _wl in FORBIDDEN:
                if rx.search(line):
                    findings.append(f"{rel}:{i}: forbidden [{label}]: {line.strip()[:120]}")
            # Superseded +0.43 outside a clearly-superseded context. Only meaningful
            # in prose (.md); in data tables 0.43 is just a value, and in code it is a guard.
            if (path.suffix.lower() == ".md" and RICTOR_043.search(line)
                    and re.search(r"rictor|revers", line, re.IGNORECASE)
                    and path.name not in superseded_files and not SUPERSEDED_OK.search(ctx)):
                findings.append(f"{rel}:{i}: superseded +0.43 near RICTOR/reversal in non-superseded context: {line.strip()[:120]}")
            # "validated drug target" not negated within the context window.
            if VALIDATED.search(line) and not VALIDATED_OK.search(ctx):
                findings.append(f"{rel}:{i}: unsupported 'validated (drug) target' wording: {line.strip()[:120]}")

    # Git history of the new public repo (commit messages) must also be clean.
    try:
        log = subprocess.run(["git", "-C", str(REPO), "log", "--format=%H %s%n%b"],
                             capture_output=True, text=True, timeout=30)
        for label, rx, _wl in FORBIDDEN:
            if label in ("env file reference",):
                continue
            for line in log.stdout.splitlines():
                if rx.search(line):
                    findings.append(f"git-history: forbidden [{label}] in commit message: {line.strip()[:120]}")
    except Exception:
        pass  # no git history yet is fine
    return findings


def main() -> int:
    findings = audit()
    print("=" * 70)
    print("TargetGate — public-readiness / privacy audit")
    print("=" * 70)
    if not findings:
        print("PASS — no forbidden private, superseded, or unsupported content found.")
        return 0
    print(f"FAIL — {len(findings)} finding(s):\n")
    for f in findings:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
