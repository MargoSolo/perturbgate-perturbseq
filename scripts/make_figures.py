#!/usr/bin/env python3
"""Regenerate all figures (PNG + SVG) and their source data from frozen artifacts.
Equivalent to `make figures` / `targetgate figures`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from targetgate.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(["figures"]))
