#!/usr/bin/env python3
"""Level 2 entry point: recompute RICTOR robustness from public derived matrices
and compare to the frozen tables. Equivalent to `make reproduce`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from targetgate.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(["reproduce"]))
