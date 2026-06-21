"""Standalone oracle smoke test (no pytest required).

Mirrors the project's golden-test convention. Verifies the instrument runs
end-to-end deterministically and emits well-formed verdicts. Run:

    python test_oracle_standalone.py     # expected: 3/3 PASSED
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from oracle.benchmark import CONDITIONS, run_condition  # noqa: E402
from oracle.oracle import adjudicate, run_battery  # noqa: E402
from oracle.predictions import registry_hash  # noqa: E402


def test_determinism() -> None:
    assert run_condition(1, CONDITIONS["BASE"]) == run_condition(1, CONDITIONS["BASE"])


def test_registry_pinned() -> None:
    assert registry_hash() == "20be317d26223261b1ffe8434fe229a82b0a7a120e7dd7091f0e82db55a3f269"


def test_battery_and_verdicts() -> None:
    verdicts = adjudicate(run_battery(list(range(6))))
    assert verdicts
    for v in verdicts:
        assert v.verdict in ("PASS", "REFUTED", "NULL")


def main() -> int:
    tests = [test_determinism, test_registry_pinned, test_battery_and_verdicts]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASSED: {t.__name__}")
            passed += 1
        except AssertionError as exc:
            print(f"FAILED: {t.__name__}: {exc}")
    print(f"\n{passed}/{len(tests)} PASSED")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    raise SystemExit(main())
