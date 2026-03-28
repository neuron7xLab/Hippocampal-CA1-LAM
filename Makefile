# Makefile for Hippocampal-CA1-LAM
# Professional automation for all common tasks
#
# Usage: make <target>
# Example: make install, make test, make clean

.PHONY: help install install-dev test test-quick test-unit test-golden \
        format lint clean clean-all docs deploy benchmark run-example

# Default target
help:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🧠 Hippocampal-CA1-LAM - Makefile Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Installation:"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install dev dependencies + tools"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests (golden + unit)"
	@echo "  make test-quick       - Run only golden tests"
	@echo "  make test-unit        - Run only unit tests"
	@echo "  make test-golden      - Run golden tests with verbose output"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format           - Auto-format code (black + isort)"
	@echo "  make lint             - Lint code (flake8 + mypy)"
	@echo "  make check            - format + lint + test"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            - Remove build artifacts"
	@echo "  make clean-all        - Remove all generated files + venv"
	@echo "  make docs             - Generate documentation"
	@echo "  make benchmark        - Run performance benchmarks"
	@echo "  make run-example      - Run basic demo"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy           - Deploy to GitHub"
	@echo "  make release          - Create release archive"
	@echo ""

# Installation targets
install:
	@echo "📦 Installing production dependencies..."
	pip install -r requirements.txt
	@echo "✅ Installation complete"

install-dev:
	@echo "📦 Installing development environment..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Dev environment ready"

# Testing targets
test:
	@echo "🧪 Running all tests..."
	@bash scripts/run_all_tests.sh

test-quick:
	@echo "🧪 Running golden tests..."
	@python test_golden_standalone.py

test-unit:
	@echo "🧪 Running unit tests..."
	@pytest tests/ -v

test-golden:
	@echo "🧪 Running golden tests (verbose)..."
	@python test_golden_standalone.py -v

# Code quality targets
format:
	@echo "✨ Formatting code..."
	@black . --line-length 100 --exclude '/(\.git|\.venv|venv|build|dist)/'
	@isort . --profile black
	@echo "✅ Code formatted"

lint:
	@echo "🔍 Linting code..."
	@flake8 . --max-line-length=100 --exclude=venv,venv-dev,build,dist,.git
	@mypy . --ignore-missing-imports --exclude '/(venv|build|dist)/'
	@echo "✅ Linting complete"

check: format lint test
	@echo "✅ All checks passed"

# Cleaning targets
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '*.pyc' -delete
	@find . -type f -name '*.pyo' -delete
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@echo "✅ Clean complete"

clean-all: clean
	@echo "🧹 Removing virtual environments..."
	@rm -rf venv/ venv-dev/
	@echo "✅ All clean"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@if [ -d "docs/" ]; then \
		echo "✅ Documentation already in docs/"; \
	else \
		echo "⚠ No docs/ directory found"; \
	fi

# Utilities
benchmark:
	@echo "⚡ Running benchmarks..."
	@python scripts/benchmark.py

run-example:
	@echo "🎯 Running basic example..."
	@python examples/demo_basic_usage.py

# Deployment
deploy:
	@echo "📤 Deploying to GitHub..."
	@bash deploy_to_github.sh

release:
	@echo "📦 Creating release archive..."
	@tar -czf Hippocampal-CA1-LAM-v2.0.tar.gz \
		--exclude='venv' \
		--exclude='venv-dev' \
		--exclude='.git' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		.
	@echo "✅ Archive created: Hippocampal-CA1-LAM-v2.0.tar.gz"

# Development shortcuts
dev: install-dev
	@echo "✅ Development environment ready"
	@echo "   Run: make test"

quick: test-quick
	@echo "✅ Quick validation complete"
