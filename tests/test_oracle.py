"""Tests for the Necessity-Gated Retrieval Oracle.

These tests verify the *instrument* (determinism, knockout isolation, verdict
logic, pre-registration integrity). They deliberately do NOT assert which
mechanism passes or fails: hardcoding a scientific verdict would defeat the
falsification purpose. Scientific verdicts come from running the battery.
"""

from __future__ import annotations

import numpy as np

from oracle.benchmark import CONDITIONS, run_condition
from oracle.oracle import _bootstrap_ci, adjudicate, run_battery
from oracle.predictions import PRE_REGISTERED, registry_hash


def test_registry_hash_is_stable_and_pinned() -> None:
    # The hash must be deterministic and match the value pinned at registration.
    assert registry_hash() == registry_hash()
    assert registry_hash() == "20be317d26223261b1ffe8434fe229a82b0a7a120e7dd7091f0e82db55a3f269"


def test_predictions_are_well_formed() -> None:
    for p in PRE_REGISTERED:
        assert p.predicted_sign in (-1, 1)
        assert p.knockout in CONDITIONS
        assert p.metric in ("recall_at_1", "recall_at_1_high_novelty")


def test_run_condition_is_deterministic() -> None:
    a = run_condition(7, CONDITIONS["BASE"])
    b = run_condition(7, CONDITIONS["BASE"])
    assert a == b


def test_metrics_are_valid_probabilities() -> None:
    r = run_condition(0, CONDITIONS["BASE"])
    for v in r.values():
        assert 0.0 <= v <= 1.0


def test_knockout_isolates_a_single_mechanism() -> None:
    # KO_PHASE must change the measured recall vs BASE for the same seed,
    # otherwise the knockout switch is wired to nothing.
    base = run_condition(3, CONDITIONS["BASE"])["recall_at_1"]
    ko_phase = run_condition(3, CONDITIONS["KO_PHASE"])["recall_at_1"]
    assert base != ko_phase


def test_bootstrap_ci_is_ordered_and_brackets_mean() -> None:
    delta = np.array([0.1, 0.2, 0.15, 0.05, 0.12, 0.18, 0.09, 0.11])
    low, high = _bootstrap_ci(delta)
    assert low <= high
    assert low <= delta.mean() <= high


def test_adjudicate_emits_valid_verdicts() -> None:
    battery = run_battery(list(range(6)))
    verdicts = adjudicate(battery)
    assert len(verdicts) == len(PRE_REGISTERED)
    for v in verdicts:
        assert v.verdict in ("PASS", "REFUTED", "NULL")
        assert v.ci_low <= v.ci_high
        # NULL iff the CI brackets zero.
        brackets_zero = v.ci_low <= 0.0 <= v.ci_high
        assert (v.verdict == "NULL") == brackets_zero
