# Necessity-Gated Retrieval Oracle

A falsification instrument for the CA1 memory engine. It answers one disciplined
question and refuses to answer more:

> Are the biophysical mechanisms of `CA1MemoryModule` — theta phase-coded keys,
> novelty-gated replay selection, replay-driven Hebbian consolidation —
> *functionally necessary* for downstream associative recall, in the direction
> the literature predicts?

## Why this exists (the synthesis)

Two vectors in this repo are individually unable to validate the model:

- **Mechanistic core** (`core/`): literature-grounded, but by the repo's own
  honesty statement *not fit to or validated against electrophysiology*. It
  cannot prove itself by fidelity.
- **AI memory** (`ai_integration/memory_module.py`): has a measurable downstream
  task (retrieval), but raw retrieval performance says nothing about biological
  truth.

Colliding them yields a *third* claim neither could make alone: a mechanism
earns standing not by matching neurons and not by winning a RAG benchmark, but
by whether **knocking it out degrades retrieval in the literature-predicted
direction**. This is a falsifiable *implementation-necessity* claim — strictly
weaker than a digital twin, but real.

> **Scope guard.** A PASS means a mechanism is functionally necessary *as
> implemented*. It is **not** a biological measurement and **not** a digital-twin
> validation. REFUTED/NULL are valid, informative outcomes.

## Method (T1–T5)

| Stage | What | Where |
|-------|------|-------|
| T1 | Deterministic cued associative-recall benchmark (recall@1 under noise) | `oracle/benchmark.py` |
| T2 | Single-mechanism knockouts (data + RNG held identical across conditions) | `oracle/benchmark.py` |
| T3 | **Pre-registered, sha256-pinned** signed directional predictions | `oracle/predictions.py` |
| T4 | Ablation battery across seeds | `oracle/oracle.py` |
| T5 | Bootstrap-CI adjudication → PASS / REFUTED / NULL | `oracle/oracle.py` |

Pre-registration hash (printed atop every report; edits to the registry change
it, which is the audit signal):

```
20be317d26223261b1ffe8434fe229a82b0a7a120e7dd7091f0e82db55a3f269
```

Run it:

```bash
python -m oracle.run_oracle --seeds 24
```

## First honest run (24 seeds, baseline recall@1 ≈ 0.54)

| mechanism | knockout | Δ(base−ko) | 95% CI | verdict |
|-----------|----------|-----------:|--------|---------|
| replay_consolidation | KO_REPLAY | +0.001 | [−0.002, +0.005] | **NULL** |
| novelty_gated_selection | KO_NOVELTY | +0.002 | [+0.000, +0.006] | **NULL** |
| theta_phase_key | KO_PHASE | −0.167 | [−0.196, −0.137] | **REFUTED** |

### Read (no promotion)

- **Replay consolidation — NULL.** `replay()` applies a Hebbian update to
  `W_encoder` but the stored keys are frozen, so the encoder drifts away from
  the keys it must match: any consolidation benefit is cancelled. As
  implemented, consolidation is functionally inert for recall.
- **Novelty-gated selection — NULL.** Inherits the same inertia; selection
  policy cannot matter if replay itself does not move the metric.
- **Theta phase keys — REFUTED.** `retrieve()` encodes the query phase-blind
  (`include_phase=False`), so theta phase appears only in stored keys and acts
  as ~2 dims of pure mismatch noise. Phase coding **lowers** recall by ~17
  points — opposite to the pre-registered +1. This is a real implementation
  defect surfaced by the oracle, registered as a caveat *before* the run.

These are negative artefacts, not failures: the oracle did its job by refusing
to confirm mechanisms the implementation does not actually support.

## Closure run — same frozen registry (`20be317d…`), two implementation fixes

The first run's REFUTED/NULL verdicts were treated as falsification leads, not
endpoints. Two defects in `ai_integration/memory_module.py` were repaired and the
**same pre-registered predictions** were re-run (registry hash unchanged — no new
version opened):

1. **`retrieve()` was phase-blind** (`include_phase=False`): the query is now
   encoded phase-aware, and the benchmark probes each cue at the item's stored
   theta phase (the cue carries the event's own temporal context).
2. **`replay()` froze keys**: stored keys are now re-encoded from a retained
   `source_h` at their original phase after each Hebbian encoder update, so keys
   track the encoder instead of drifting out of alignment.

Re-run (24 seeds, baseline recall@1 ≈ 0.92):

| mechanism | knockout | Δ(base−ko) | 95% CI | verdict |
|-----------|----------|-----------:|--------|---------|
| replay_consolidation | KO_REPLAY | +0.000 | [+0.000, +0.000] | **NULL** |
| novelty_gated_selection | KO_NOVELTY | +0.000 | [+0.000, +0.000] | **NULL** |
| theta_phase_key | KO_PHASE | +0.219 | [+0.201, +0.239] | **PASS** |

- **theta_phase_key: REFUTED → PASS.** With phase-matched cues the mechanism is
  now functionally necessary (0.922 → 0.703 when removed), in the pre-registered
  +1 direction. This prediction is **closed cleanly**.
- **replay_consolidation: still NULL — and now a sharper negative.** Re-syncing
  keys was *necessary but not sufficient*. A Hebbian update to the **shared**
  encoder transforms stored keys and incoming queries symmetrically, so
  content-addressable recall is invariant to it (CI is exactly [0, 0] across all
  seeds: a structural no-op, not noise). To become functionally necessary,
  consolidation needs an **asymmetric** mechanism — per-key salience/magnitude or
  a value-side update — not a shared-encoder transform.
- **novelty_gated_selection: still NULL.** Inherits replay's inertness; selection
  policy cannot matter while replay itself is a no-op.

The registry stays frozen. `theta_phase_key` is closed as PASS; `replay` and
`novelty` remain **open negatives** — they are not promoted, and no new
prediction version is opened until they are closed honestly by an asymmetric
consolidation mechanism.
