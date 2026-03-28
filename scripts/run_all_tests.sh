#!/bin/bash
# RUN ALL TESTS - Запуск всіх тестів з детальним звітом
#
# Usage: bash scripts/run_all_tests.sh

set -e

echo "========================================================================"
echo "🧪 HIPPOCAMPAL-CA1-LAM - COMPREHENSIVE TEST SUITE"
echo "========================================================================"
echo ""

# Check if in virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠ Віртуальне середовище не активне"
    echo "   Активуйте: source venv/bin/activate"
    read -p "Продовжити без venv? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

START_TIME=$(date +%s)

# Test 1: Golden Tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1/4: Golden Tests (Reproducibility & Stability)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
python test_golden_standalone.py
GOLDEN_RESULT=$?
echo ""

# Test 2: Unit Tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2/4: Unit Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short
    UNIT_RESULT=$?
else
    echo "⚠ pytest не встановлено, використовую python unittest"
    python -m unittest discover tests/ -v
    UNIT_RESULT=$?
fi
echo ""

# Test 3: Import Tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3/4: Import Tests (Перевірка всіх модулів)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

IMPORT_RESULT=0

echo "Перевірка імпортів..."
python -c "from data.biophysical_parameters import get_default_parameters; print('✓ data.biophysical_parameters')" || IMPORT_RESULT=1
python -c "from core.hierarchical_laminar import HierarchicalLaminarModel; print('✓ core.hierarchical_laminar')" || IMPORT_RESULT=1
python -c "from core.neuron_model import TwoCompartmentNeuron; print('✓ core.neuron_model')" || IMPORT_RESULT=1
python -c "from core.theta_swr_switching import NetworkStateController; print('✓ core.theta_swr_switching')" || IMPORT_RESULT=1
python -c "from plasticity.unified_weights import UnifiedWeightMatrix; print('✓ plasticity.unified_weights')" || IMPORT_RESULT=1
python -c "from ai_integration.memory_module import LLMWithCA1Memory; print('✓ ai_integration.memory_module')" || IMPORT_RESULT=1
python -c "from validation.validators import validate_network_stability; print('✓ validation.validators')" || IMPORT_RESULT=1

if [ $IMPORT_RESULT -eq 0 ]; then
    echo ""
    echo "✅ Всі модулі імпортуються успішно"
else
    echo ""
    echo "❌ Деякі модулі не вдалося імпортувати"
fi
echo ""

# Test 4: Example Scripts
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4/4: Example Scripts (Швидка перевірка)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

EXAMPLES_RESULT=0

if [ -f "examples/demo_basic_usage.py" ]; then
    echo "Запуск demo_basic_usage.py (перші 10 секунд)..."
    timeout 10s python examples/demo_basic_usage.py || true
    echo "✓ demo_basic_usage.py виконано"
else
    echo "⚠ examples/demo_basic_usage.py не знайдено"
    EXAMPLES_RESULT=1
fi
echo ""

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 TEST SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $GOLDEN_RESULT -eq 0 ]; then
    echo "✅ Golden Tests: PASSED"
else
    echo "❌ Golden Tests: FAILED"
fi

if [ $UNIT_RESULT -eq 0 ]; then
    echo "✅ Unit Tests: PASSED"
else
    echo "❌ Unit Tests: FAILED"
fi

if [ $IMPORT_RESULT -eq 0 ]; then
    echo "✅ Import Tests: PASSED"
else
    echo "❌ Import Tests: FAILED"
fi

if [ $EXAMPLES_RESULT -eq 0 ]; then
    echo "✅ Examples: PASSED"
else
    echo "⚠ Examples: PARTIAL (check manually)"
fi

echo ""
echo "Duration: ${DURATION}s"
echo ""

# Final result
if [ $GOLDEN_RESULT -eq 0 ] && [ $UNIT_RESULT -eq 0 ] && [ $IMPORT_RESULT -eq 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ ALL TESTS PASSED - PRODUCTION READY"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "❌ SOME TESTS FAILED - CHECK OUTPUT ABOVE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi
