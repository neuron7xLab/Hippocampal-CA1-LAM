"""T3 — Pre-registered, sha256-pinned directional predictions.

Frozen BEFORE the ablation battery is run (T4). Each prediction names a
biophysical mechanism, the knockout that removes it, and a *signed* directional
hypothesis grounded in the cited literature. The sign is the falsifiable
commitment: if the measured effect lands with the opposite sign at significance,
the mechanism is REFUTED, not quietly re-interpreted.

`registry_hash()` returns a stable digest of this registry. The oracle runner
prints it at the top of every report so a reviewer can confirm the predictions
were not edited after seeing results.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Prediction:
    """A single pre-registered, signed directional hypothesis."""

    mechanism: str
    knockout: str
    metric: str
    #: +1  -> removing the mechanism should DECREASE the metric (Δ = base - ko > 0)
    #: -1  -> removing the mechanism should INCREASE the metric (Δ < 0)
    predicted_sign: int
    literature: str
    rationale: str


# ---------------------------------------------------------------------------
# THE FROZEN REGISTRY.  Do not edit after a battery has been run against it;
# open a new versioned entry instead.  Edits change registry_hash() and the
# mismatch is the audit signal.
# ---------------------------------------------------------------------------
PRE_REGISTERED: tuple[Prediction, ...] = (
    Prediction(
        mechanism="replay_consolidation",
        knockout="KO_REPLAY",
        metric="recall_at_1",
        predicted_sign=+1,
        literature="Graupner & Brunel 2012 (PNAS); SWR replay consolidation.",
        rationale=(
            "Offline replay applies Hebbian strengthening to the encoder for "
            "replayed entries. If consolidation is functionally necessary, "
            "removing it should not increase cued recall: Δ = base - KO >= 0, "
            "predicted strictly > 0."
        ),
    ),
    Prediction(
        mechanism="novelty_gated_selection",
        knockout="KO_NOVELTY",
        metric="recall_at_1_high_novelty",
        predicted_sign=+1,
        literature="Novelty-gated replay prioritisation (SWR literature).",
        rationale=(
            "Novelty-weighted replay selection preferentially re-strengthens "
            "high-novelty memories vs uniform-random selection. For the "
            "high-novelty subset, novelty-mode recall should be >= random-mode."
        ),
    ),
    Prediction(
        mechanism="theta_phase_key",
        knockout="KO_PHASE",
        metric="recall_at_1",
        predicted_sign=+1,
        literature="Theta phase-coded keys (Magee 1998 HCN gradient context).",
        rationale=(
            "Phase-coded keys are claimed to add temporal context capacity. "
            "Naive literature prediction is +1. MECHANISTIC CAVEAT registered "
            "in advance: the current retrieve() encodes queries phase-blind "
            "(include_phase=False), so phase appears only in stored keys. A "
            "NULL or REFUTED verdict here would be a real finding about the "
            "implementation, not a benchmark artdefact."
        ),
    ),
)


def registry_hash() -> str:
    """Stable sha256 over the canonical JSON of the frozen registry."""
    canonical = json.dumps(
        [
            {
                "mechanism": p.mechanism,
                "knockout": p.knockout,
                "metric": p.metric,
                "predicted_sign": p.predicted_sign,
            }
            for p in PRE_REGISTERED
        ],
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
