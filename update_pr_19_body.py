#!/usr/bin/env python3
"""
Script to update PR #19 body with required Phase and Verification metadata.

This script uses the GitHub API to update the PR body to satisfy the
phase-validation.yml workflow requirements.

Usage:
    export GITHUB_TOKEN="your_token_here"
    python3 update_pr_19_body.py
"""

import os
import sys

import requests

# Configuration
OWNER = "neuron7x"
REPO = "Hippocampal-CA1-LAM"
PR_NUMBER = 19

# New PR body with required metadata
NEW_PR_BODY = """Phase: 1.0

The CA1/LAM effort requires explicit core boundaries, invariants, and a deterministic harness. This PR adds a concise MODE A audit doc that captures the public interfaces, guards, and roadmap for deterministic enforcement.

- Audit & boundaries: New `docs/mode_a_audit.md` describes the memory core surface (contracts, invariants, metrics, config) and the deterministic `CA1Network.simulate(duration_ms, dt=None)` API.
- Determinism harness: Provides the minimal seeded command (`PYTHONPATH=. pytest -q tests/test_core_contracts.py tests/test_config.py`), notes on guard enforcement, and the exact `REPORT_KEYS` set from metrics.
- Failure map & roadmap: Enumerates determinism risks (seed drift, guard bypass, state growth, API drift, config skew) and a 5-item roadmap for CI gating, seed propagation, bounded traces, metrics validation, and config linting.
- Clean-up: Removed stray egg-info artifacts introduced by editable install.

Verification:
- PYTHONPATH=. pytest -q tests/test_core_contracts.py tests/test_config.py
- Reviewed docs/mode_a_audit.md for completeness
- Verified removal of egg-info artifacts

Example harness invocation:
```bash
PYTHONPATH=. pytest -q tests/test_core_contracts.py tests/test_config.py
```











Original prompt

> **SYSTEM PROMPT: CA1/LAM MEMORY CORE ENGINEERING PR PILOT (SAFE EXECUTION ORDER, 2025)**
>
> Ти — **Principal Neuro-Systems Engineer, Research Software Architect та CI/Test Determinism Auditor**.
> Проєкт: **Hippocampal-CA1-LAM**.
> Формат роботи: **виключно через Pull Request**.
>
> ---
>
> ## 0. НЕПОРУШНІ ПРАВИЛА
>
> * Один PR = одна чітка інженерна ціль.
> * Заборонено змінювати наукову/алгоритмічну поведінку без контрактних тестів.
> * Заборонено scope creep, переписування "всього", неявні побічні ефекти.
> * Усі зміни мають бути детерміновані, відтворювані, оборотні (rollback).
> * Безпека: жодних секретів у коді, жодних небезпечних команд, мінімальні дозволи CI.
>
> ---
>
> ## 1. РЕЖИМИ РОБОТИ
>
> ### MODE A — READ-ONLY AUDIT
>
> 1. Проаналізуй структуру репозиторію та виділи **Memory Core Boundary (CA1/LAM)**.
> 2. Зафіксуй публічні та внутрішні інтерфейси ядра (I/O, стани, сайд-ефекти).
> 3. Сформуй **інваріанти системи** (детермінізм, обмеженість стану, finite-safety, shape-safety).
> 4. Побудуй **Failure Map** (недетермінізм, приховані залежності, неконтрольований ріст стану, silent bugs).
> 5. Склади **Roadmap з 3–5 малих PR** з оцінкою ризиків і метрик.
>
> ### MODE B — WRITE
>
> * Реалізуй **один PR** з roadmap.
> * Мінімальні дифи. Лише заплановані зміни.
> * Тести, метрики та CI — обов'язкові.
>
> ---
>
> ## 2. ПРІОРИТЕТ №1 — КОНТРАКТИ ТА ДЕТЕРМІНІЗМ
>
> **Ціль:** зробити ядро CA1/LAM вимірюваним і перевіряємим.
>
> Обов'язково:
>
> * Явні структури стану пам'яті (без глобалів).
> * Контракти для encode / recall / update.
> * Runtime-guards: shape, bounds, NaN/Inf.
> * Детермінований test harness із фіксованим seed.
> * Базові метрики стабільності та дрейфу.
> * CI-gate: тести + coverage для core.
>
> ---
>
> ## 3. ПРІОРИТЕТ №2 — ІНЖЕНЕРНА ГІГІЄНА
>
> * Чітке розділення: core / experiments / utils.
> * Заборона імпортів з experiments у core.
> * Конфіги замість хардкоду (seed, bounds, timestep).
>
> ---
>
> ## 4. ПРІОРИТЕТ №3 — ТЕСТИ ТА CI
>
> * Усунь флейки, часові та порядкові залежності.
> * Зменш час виконання тестів без втрати покриття.
> * CI має бути швидким, стабільним, відтворюваним.
>
> ---
>
> ## 5. ПРІОРИТЕТ №4 — ДОКУМЕНТАЦІЯ
>
> * README відображає **реальну поведінку**, не наміри.
> * Інструкції запуску перевірені.
> * Приклад мінімального детермінованого використання.
>
> ---
>
> ## 6. ФОРМАТ ВИХОДУ ДЛЯ КОЖНОГО PR
>
> 1. PR Title
> 2. Scope
> 3. Files changed
> 4. Test plan
> 5. Metrics
> 6. Risks
> 7. Rollback
>
> ---
>
> ## 7. СТОП-КРИТЕРІЇ
>
> * Немає детермінізму — зупинка.
> * Немає тесту на зміну — PR заборонено.
> * Порушення контрактів — лише через адаптер або окремий PR.
>
> ---
>
> ## 8. СТАРТ
>
> Запусти MODE A та підготуй PR-**Core Contracts + Deterministic Harness**.




---

💡 You can make Copilot smarter by setting up custom instructions, customizing its development environment and configuring Model Context Protocol (MCP) servers. Learn more [Copilot coding agent tips](https://gh.io/copilot-coding-agent-tips) in the docs.
"""


def update_pr_body():
    """Update PR #19 body using GitHub API."""
    # Get GitHub token from environment
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        print("Please set it with: export GITHUB_TOKEN='your_token'", file=sys.stderr)
        sys.exit(1)

    # GitHub API endpoint
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}"

    # Headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Payload
    data = {"body": NEW_PR_BODY}

    print(f"Updating PR #{PR_NUMBER} in {OWNER}/{REPO}...")

    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()

        print("✓ Successfully updated PR body!")
        print(f"PR URL: https://github.com/{OWNER}/{REPO}/pull/{PR_NUMBER}")
        return 0

    except requests.exceptions.RequestException as e:
        print(f"Error updating PR: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(update_pr_body())
