# Hippocampal-CA1-LAM v2.0

**🧠 Literature-grounded mechanistic model of the CA1 hippocampal laminar circuit**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/neuron7xLab/Hippocampal-CA1-LAM/actions/workflows/python-tests.yml/badge.svg)](https://github.com/neuron7xLab/Hippocampal-CA1-LAM/actions/workflows/python-tests.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/neuron7xLab/Hippocampal-CA1-LAM/badge)](https://scorecard.dev/viewer/?uri=github.com/neuron7xLab/Hippocampal-CA1-LAM)

A reproducible, research-grade computational model of CA1: a two-compartment
conductance-based pyramidal neuron, a four-sublayer laminar structure, theta↔SWR
state switching, and calcium-based plasticity. Every structural and dynamical
parameter is taken from peer-reviewed sources (see [Bibliography](docs/BIBLIOGRAPHY.md)).

> **Scope and honesty.** This is a *mechanistic research model*, not a validated
> digital twin. Parameters are literature-sourced; the model has **not** been fit
> to or validated against the authors' own electrophysiology. Treat outputs as
> hypotheses about circuit dynamics, not measurements.

## Overview

- **Two-compartment pyramidal neuron** (soma–dendrite) with HCN gradient, NMDA,
  GABA conductances — parameters from Magee 1998, Jahr & Stevens 1990.
- **Four-sublayer laminar structure.** Layer *proportions* are derived from the
  58,065-cell smFISH atlas of Pachicano et al. (*Nat. Commun.* 2025). The atlas
  is the empirical source for the proportions — **not** the simulated network
  size. The simulated network size is configurable (`n_neurons`, default `100`).
- **Theta ↔ SWR state switching** with an explicit state machine, gated
  inhibition (OLM/PV) and replay detection.
- **Calcium-based plasticity** (Graupner & Brunel, *PNAS* 2012) with
  Tsodyks–Markram short-term plasticity.
- **AI-memory integration**: a HippoRAG-inspired retrieval module.
- **Deterministic**: `seed=42` reproduces an identical 6-test golden signal.

## Quick Start

```bash
bash quick_start.sh      # venv + deps + golden suite (expected: 6/6 PASSED)
```

### Manual installation

```bash
pip install -r requirements.txt

python test_golden_standalone.py     # expected: 6/6 PASSED
python examples/demo_basic_usage.py  # minimal CA1Network walkthrough
```

### Other entry points

```bash
python examples/demo_ca_plasticity.py   # calcium LTP/LTD demo
python examples/demo_theta_swr.py       # theta↔SWR switching demo
make test                               # full pytest suite
make lint                               # flake8 + format check
python scripts/benchmark.py             # performance profile
```

## Reproducing the CI gates locally

The same checks the CI runs, in order:

```bash
python -m pytest -q                          # unit + golden tests (204)
bandit -r core plasticity ai_integration data validation --severity-level medium
gitleaks detect --config .gitleaks.toml      # secret scan
python scripts/unicode_scan.py               # homoglyph / RTL scan
python scripts/validate_configs.py .         # JSON/YAML validity
python scripts/ci_policy_check.py            # workflow policy
pip-audit -r requirements.txt                # dependency CVEs
```

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Examples](docs/USAGE.md)
- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [CI/CD](.github/CI.md)
- [Bibliography](docs/BIBLIOGRAPHY.md)
- [Contributing](CONTRIBUTING.md)

## Scientific Foundation

All parameters from peer-reviewed sources — full DOIs in the
[Bibliography](docs/BIBLIOGRAPHY.md):

- **Laminar proportions** — Pachicano et al., *Nat. Commun.* 2025 (58,065-cell smFISH atlas)
- **Calcium plasticity** — θ_d = 1.0 μM, θ_p = 2.0 μM (Graupner & Brunel, *PNAS* 2012)
- **HCN gradient / NMDA** — Magee 1998; Jahr & Stevens 1990
- **Theta dynamics** — O'Keefe & Recce 1993

## Status

- ✅ Two-compartment neuron, laminar structure, theta/SWR switching, Ca²⁺ plasticity — implemented
- ✅ 204 unit tests + 6 deterministic golden tests (`seed=42`)
- ✅ Type hints, CI gates (tests, bandit, gitleaks, unicode, config, dependency audit)
- ⚠️ Not validated against in-house electrophysiology — see scope note above

## Citation

```bibtex
@software{hippocampal_ca1_lam_2025,
  title  = {Hippocampal-CA1-LAM: a literature-grounded mechanistic CA1 model},
  author = {neuron7xLab},
  year   = {2025},
  url    = {https://github.com/neuron7xLab/Hippocampal-CA1-LAM}
}
```

## License

MIT License — see [LICENSE](LICENSE).
