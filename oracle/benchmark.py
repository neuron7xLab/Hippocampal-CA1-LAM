"""T1 + T2 — Deterministic associative-recall benchmark and knockout conditions.

T1 task: *cued associative recall under noise*. Store N (key, value) episodes in
the CA1 memory module while the theta phase advances between events; then probe
with a noisy cue of each stored hidden state and ask the module to retrieve the
single best slot. The metric is recall@1 (fraction of cues whose top-1 retrieved
slot is the correct one). A high-novelty subset metric supports the novelty test.

T2 knockouts: each condition differs from BASE by exactly one mechanism, so any
metric difference is attributable to that mechanism (the episode data and the
module's RNG stream are held identical across conditions for a fixed seed).

The benchmark targets `CA1MemoryModule` deliberately: the public
`CA1Network.simulate()` is a synthetic RNG scaffold with no biophysics, so an
oracle over it would be vacuous by construction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ai_integration.memory_module import CA1MemoryModule
from data.biophysical_parameters import AIIntegrationParams

# --- Instrument calibration (difficulty knobs; chosen for non-degeneracy, i.e.
#     baseline recall strictly between floor and ceiling so knockouts can move
#     it).  These are design choices, independent of the signed predictions. ---
D_MODEL = 64
KEY_DIM = 64  # no compression: isolate mechanism effects from projection loss
VALUE_DIM = 64
MEMORY_SIZE = 128
N_ITEMS = 40
CUE_NOISE = 0.25  # std of additive cue noise (pre-normalisation)
N_REPLAY = 20
PHASE_STEP_S = 0.0125  # seconds advanced per stored event (~1/10 theta period)


@dataclass(frozen=True)
class ConditionSpec:
    """One ablation condition: BASE, or BASE minus a single mechanism."""

    name: str
    use_phase_key: bool
    do_replay: bool
    replay_mode: str  # "novelty" | "random" | "recent"


CONDITIONS: dict[str, ConditionSpec] = {
    "BASE": ConditionSpec("BASE", use_phase_key=True, do_replay=True, replay_mode="novelty"),
    "KO_PHASE": ConditionSpec(
        "KO_PHASE", use_phase_key=False, do_replay=True, replay_mode="novelty"
    ),
    "KO_REPLAY": ConditionSpec(
        "KO_REPLAY", use_phase_key=True, do_replay=False, replay_mode="novelty"
    ),
    "KO_NOVELTY": ConditionSpec(
        "KO_NOVELTY", use_phase_key=True, do_replay=True, replay_mode="random"
    ),
}


def _make_params(use_phase_key: bool) -> AIIntegrationParams:
    return AIIntegrationParams(
        d_model=D_MODEL,
        memory_size=MEMORY_SIZE,
        key_dim=KEY_DIM,
        value_dim=VALUE_DIM,
        use_phase_key=use_phase_key,
        top_k=1,
        temperature=0.1,
    )


def _build_episodes(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (H, V, novelty): identical for a fixed seed across all conditions."""
    h = rng.standard_normal((N_ITEMS, D_MODEL))
    h /= np.linalg.norm(h, axis=1, keepdims=True) + 1e-8
    v = rng.standard_normal((N_ITEMS, VALUE_DIM))
    novelty = rng.uniform(0.2, 1.0, size=N_ITEMS)
    return h, v, novelty


def run_condition(seed: int, spec: ConditionSpec) -> dict[str, float]:
    """Run one condition. Returns recall@1 and high-novelty recall@1.

    Determinism: episode data uses ``default_rng(seed)``; the module's internal
    RNG uses ``default_rng(seed + 10_000)``; cue noise uses ``default_rng(seed +
    20_000)``. All three are independent of the knockout, so the only varying
    factor across conditions is the mechanism itself.
    """
    data_rng = np.random.default_rng(seed)
    module_rng = np.random.default_rng(seed + 10_000)
    cue_rng = np.random.default_rng(seed + 20_000)

    h, v, novelty = _build_episodes(data_rng)
    params = _make_params(spec.use_phase_key)
    mem = CA1MemoryModule(params, rng=module_rng)

    # Store episodes, advancing theta phase between events (phase diversity).
    slot_of_item: list[int] = []
    phase_of_item: list[float] = []
    for i in range(N_ITEMS):
        mem.update_theta(dt=PHASE_STEP_S)
        phase_of_item.append(mem.theta_phase)
        slot = mem.store(h[i], v[i], novelty=float(novelty[i]))
        slot_of_item.append(slot)

    # Offline consolidation (the mechanism under test for replay/novelty).
    if spec.do_replay:
        mem.set_learning_mode("offline")
        mem.replay(n_episodes=N_REPLAY, selection_mode=spec.replay_mode)

    # Probe with noisy cues; recall@1 = top-1 slot matches the stored slot.
    correct = np.zeros(N_ITEMS, dtype=bool)
    for i in range(N_ITEMS):
        noise = cue_rng.standard_normal(D_MODEL)
        cue = h[i] + CUE_NOISE * noise
        cue /= np.linalg.norm(cue) + 1e-8
        # The cue carries the event's own temporal context: probe at the theta
        # phase the item was stored at (no-op when use_phase_key is False).
        mem.theta_phase = phase_of_item[i]
        _, indices = mem.retrieve(cue, top_k=1)
        correct[i] = bool(indices) and indices[0] == slot_of_item[i]

    recall = float(correct.mean())
    # High-novelty subset: top 50% by novelty.
    hi = novelty >= np.median(novelty)
    recall_hi = float(correct[hi].mean()) if hi.any() else float("nan")
    return {"recall_at_1": recall, "recall_at_1_high_novelty": recall_hi}
