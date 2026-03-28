#!/bin/bash
# QUICK START - Миттєвий запуск Hippocampal-CA1-LAM
# Одна команда для повної установки та перевірки
#
# Usage: bash quick_start.sh

set -e  # Exit on error

echo "========================================================================"
echo "🚀 HIPPOCAMPAL-CA1-LAM - QUICK START"
echo "========================================================================"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo "✓ Detected OS: $OS"
echo ""

# Check Python
echo "1. Перевірка Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не знайдено!"
    echo "   Встановіть Python 3.8+ з https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "   ✓ Python $PYTHON_VERSION знайдено"
echo ""

# Create virtual environment
echo "2. Створення віртуального середовища..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✓ venv створено"
else
    echo "   ✓ venv вже існує"
fi
echo ""

# Activate virtual environment
echo "3. Активація віртуального середовища..."
if [[ "$OS" == "windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "   ✓ venv активовано"
echo ""

# Upgrade pip
echo "4. Оновлення pip..."
python -m pip install --upgrade pip -q
echo "   ✓ pip оновлено"
echo ""

# Install dependencies
echo "5. Встановлення залежностей..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    echo "   ✓ Основні залежності встановлено"
else
    echo "   ⚠ requirements.txt не знайдено"
fi
echo ""

# Install dev dependencies (optional)
read -p "Встановити dev залежності? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt -q
        echo "   ✓ Dev залежності встановлено"
    fi
fi
echo ""

# Run golden tests
echo "6. Запуск golden tests (перевірка установки)..."
python test_golden_standalone.py

echo ""
echo "========================================================================"
echo "✅ ГОТОВО! Hippocampal-CA1-LAM встановлено та перевірено"
echo "========================================================================"
echo ""
echo "Наступні кроки:"
echo "  • Приклади: python examples/demo_basic_usage.py"
echo "  • Всі тести: bash scripts/run_all_tests.sh"
echo "  • Документація: docs/"
echo ""
echo "Віртуальне середовище активне. Для вимкнення: deactivate"
