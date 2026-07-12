#!/usr/bin/env python3
"""Level 1 entry point: recompute the headline reversal from compact frozen
inputs, regenerate figures, and validate against golden values. Equivalent to
`make demo` / `perturbgate demo`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from perturbgate.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(["demo"]))
