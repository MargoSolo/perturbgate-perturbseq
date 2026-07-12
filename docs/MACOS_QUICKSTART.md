# macOS quickstart

**Status: verified on macOS CI** (`macos-latest`, Apple Silicon / arm64, Python
3.11). We do not claim macOS support by inspection alone — this status reflects a
green macOS CI run in which install, unit tests, `demo`, `reproduce`, `verify`,
the privacy audit, and a text-artifact byte-stability check all passed. See
[the CI workflow](../.github/workflows/ci.yml) and the repository's Actions tab.

This repository was developed on Linux/Windows. Everything below is standard,
cross-platform Python — no shell scripts, no PowerShell, no Windows-only paths.

---

## Prerequisites

- **macOS 12+** (Intel or Apple Silicon).
- **Python 3.11** (3.10–3.12 all supported). Recommended install:
  [python.org](https://www.python.org/downloads/macos/) or
  `brew install python@3.11`.
- **git**. `make` is optional (ships with the Xcode Command Line Tools:
  `xcode-select --install`); every `make` target has a plain-Python equivalent
  (see the [README](../README.md#5-reproducibility)).

## Apple Silicon (M1/M2/M3) notes

- All runtime dependencies — NumPy, pandas, SciPy, Matplotlib, PyArrow — publish
  native **arm64 macOS wheels** at the pinned versions, so `pip install` uses
  prebuilt binaries (no compiler needed) on Apple Silicon and Intel alike.
- There are **no** x86-only, Windows-only, or Rosetta-dependent packages.
- Use a native arm64 Python (the default from python.org / Homebrew on Apple
  Silicon). You do **not** need Rosetta. If you accidentally run an x86 Python
  under Rosetta, pip will still resolve universal2/x86_64 wheels, but native
  arm64 is preferred.

## Environment setup

```bash
git clone https://github.com/MargoSolo/perturbgate-perturbseq.git
cd perturbgate-perturbseq

python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"     # == make setup
```

## Demo (Level 1 — laptop, < 2 min)

Recomputes RICTOR's **+0.161** disease reversal from compact committed inputs and
validates the golden values; regenerates the figures.

```bash
make demo
# or, without make:
python -m perturbgate.cli demo
```

## Analytical reproduction (Level 2 — laptop, < 5 min)

```bash
make reproduce
# or:
python -m perturbgate.cli reproduce
```

## Verify (schemas, golden values, claims, funnel, superseded guard, audit)

```bash
make verify
# or, the individual steps:
python -m perturbgate.cli verify
python -m pytest
python scripts/public_readiness_audit.py
```

## Open PerturbGate Explorer

The Explorer is a single self-contained HTML file with no backend. The simplest
way to open it:

```bash
open reports/perturbgate_explorer.html      # opens in your default browser
```

Some browsers restrict `file://` pages; if search/filtering does not work, serve
it over a local HTTP server instead (recommended):

```bash
cd reports
python -m http.server 8000
# then open http://localhost:8000/perturbgate_explorer.html
# press Ctrl-C to stop the server
```

## `make full` is server-scale — not for a laptop

**Do not run `make full` on a normal laptop.** Level 3 downloads the open raw data
and rebuilds the disease vector and the genome-scale effect vectors; it needs a
high-memory compute server (≈ 128 GB RAM) and takes hours. Levels 1 and 2 (`make
demo`, `make reproduce`) are the laptop-scale reproducibility guarantees and cover
the headline result. See
[REPRODUCIBILITY_LEVELS.md](REPRODUCIBILITY_LEVELS.md).

---

## Portability audit (findings)

Performed before release; the definitive proof is the macOS CI job, not this
inspection.

| Check | Finding |
|---|---|
| Windows-only / x86-only / non-arm64 dependencies | none — NumPy, pandas, SciPy, Matplotlib, PyArrow all ship arm64 macOS wheels |
| lockfile | none; `pyproject.toml` uses version ranges that resolve to arm64 wheels |
| shell scripts (`.sh`/`.ps1`/`.bat`) | none in the repository — all logic is Python + a POSIX Makefile |
| hardcoded path separators / drive letters | none — `pathlib` is used throughout; the one `\r\n`→`\n` normalizer is portable |
| PowerShell/cmd-specific commands | none in committed code |
| GNU-only `sed`/`grep`/`readlink` assumptions | none — the Makefile uses only portable `find`/`rm` |
| line endings | all text committed as LF (`.gitattributes`; generators write LF explicitly) |
| Makefile on macOS | works with the system GNU make; every target also has a plain-Python equivalent |

The macOS CI job is green, so this status is **"verified on macOS CI"** rather
than "expected to work, pending platform test".
