"""T4 + T5 — Ablation battery and verdict adjudication.

T4 runs every condition across many seeds, producing a per-seed metric vector
for BASE and each knockout. T5 forms, per pre-registered prediction, the paired
difference Δ = metric(BASE) - metric(KO) across seeds, bootstraps a 95% CI of
the mean Δ, and emits PASS / REFUTED / NULL:

    NULL     CI straddles 0                      -> no necessity evidence
    PASS     CI sign matches predicted_sign      -> necessity supported
    REFUTED  CI sign opposes predicted_sign      -> mechanism is anti-functional
                                                    as implemented

A REFUTED or NULL verdict is a valid, informative result, not a failure.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from oracle.benchmark import CONDITIONS, run_condition
from oracle.predictions import PRE_REGISTERED, Prediction

N_BOOTSTRAP = 5000
BOOTSTRAP_SEED = 12345


@dataclass(frozen=True)
class Verdict:
    mechanism: str
    knockout: str
    metric: str
    predicted_sign: int
    mean_base: float
    mean_ko: float
    mean_delta: float
    ci_low: float
    ci_high: float
    verdict: str


def run_battery(seeds: list[int]) -> dict[str, dict[str, np.ndarray]]:
    """Return {metric: {condition: array-over-seeds}} for every condition."""
    metrics = ("recall_at_1", "recall_at_1_high_novelty")
    out: dict[str, dict[str, np.ndarray]] = {m: {} for m in metrics}
    for name, spec in CONDITIONS.items():
        rows = [run_condition(s, spec) for s in seeds]
        for m in metrics:
            out[m][name] = np.array([r[m] for r in rows], dtype=float)
    return out


def _bootstrap_ci(delta: np.ndarray) -> tuple[float, float]:
    """95% percentile bootstrap CI of the mean of paired differences."""
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    n = delta.size
    means = np.empty(N_BOOTSTRAP, dtype=float)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, n, size=n)
        means[b] = delta[idx].mean()
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def _adjudicate_one(pred: Prediction, battery: dict[str, dict[str, np.ndarray]]) -> Verdict:
    base = battery[pred.metric]["BASE"]
    ko = battery[pred.metric][pred.knockout]
    delta = base - ko
    ci_low, ci_high = _bootstrap_ci(delta)

    if ci_low <= 0.0 <= ci_high:
        verdict = "NULL"
    else:
        observed_sign = 1 if ci_low > 0.0 else -1
        verdict = "PASS" if observed_sign == pred.predicted_sign else "REFUTED"

    return Verdict(
        mechanism=pred.mechanism,
        knockout=pred.knockout,
        metric=pred.metric,
        predicted_sign=pred.predicted_sign,
        mean_base=float(base.mean()),
        mean_ko=float(ko.mean()),
        mean_delta=float(delta.mean()),
        ci_low=ci_low,
        ci_high=ci_high,
        verdict=verdict,
    )


def adjudicate(battery: dict[str, dict[str, np.ndarray]]) -> list[Verdict]:
    return [_adjudicate_one(p, battery) for p in PRE_REGISTERED]
