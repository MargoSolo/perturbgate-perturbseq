"""External-validation analyses (kept separate from the frozen internal pipeline).

Each submodule scores the frozen PerturbGate knockdown signatures against an
external public disease direction, reusing the same ``perturbgate.reversal``
function and sign convention. External results never alter the frozen internal
results under ``results/frozen/``.
"""
