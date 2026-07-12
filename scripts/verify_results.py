#!/usr/bin/env python3
"""Verify frozen results: schemas, golden values, claim resolution, funnel
consistency, and the superseded-value guard. Equivalent to `perturbgate verify`.
For the full release gate (which also runs the demo, figures, tests and the
privacy audit) use `make verify`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from perturbgate.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(["verify"]))
