"""Necessity-Gated Retrieval Oracle for Hippocampal-CA1-LAM.

A falsification instrument. It does **not** claim the model is a digital twin.
It asks one disciplined question: are the biophysical mechanisms of the CA1
memory module (theta phase-coded keys, novelty-gated replay selection,
replay-driven Hebbian consolidation) *functionally necessary* for downstream
associative recall, in the direction the literature predicts?

Pre-registered predictions live in `oracle.predictions` and are sha256-pinned
*before* the ablation battery runs, so PASS/REFUTED/NULL verdicts cannot be
post-hoc fitted. A REFUTED verdict is a valid, informative outcome: it is
evidence that a mechanism, as implemented, is not functionally necessary.

Scope guard (inherited from the repo's own honesty statement): outputs are
hypotheses about *implementation necessity*, not measurements of biology and
not a validation of the model as a digital twin.
"""

from oracle.benchmark import CONDITIONS, ConditionSpec, run_condition
from oracle.predictions import PRE_REGISTERED, registry_hash

__all__ = [
    "CONDITIONS",
    "ConditionSpec",
    "run_condition",
    "PRE_REGISTERED",
    "registry_hash",
]
