#!/bin/bash
# АВТОМАТИЧНИЙ DEPLOY НА GITHUB
# Автоматизує всі кроки для публікації на GitHub
#
# Usage: bash deploy_to_github.sh

set -e

echo "========================================================================"
echo "📤 HIPPOCAMPAL-CA1-LAM - DEPLOY TO GITHUB"
echo "========================================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git не встановлено!"
    echo "   Встановіть Git: https://git-scm.com/downloads"
    exit 1
fi

# Get GitHub username
echo "Введіть ваш GitHub username:"
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Username не може бути пустим"
    exit 1
fi

REPO_NAME="Hippocampal-CA1-LAM"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "Repository: $REPO_URL"
echo ""

# Check if .git exists
if [ -d ".git" ]; then
    echo "⚠ Git repository вже існує"
    read -p "Перезаписати? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .git
        echo "   ✓ Старий .git видалено"
    else
        echo "❌ Скасовано"
        exit 1
    fi
fi

# Initialize git
echo "1. Ініціалізація Git repository..."
git init
git branch -M main
echo "   ✓ Git ініціалізовано"
echo ""

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    echo "2. Створення .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
venv/
.venv/
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
*.npz
*.h5
.DS_Store
EOF
    echo "   ✓ .gitignore створено"
else
    echo "2. .gitignore існує ✓"
fi
echo ""

# Add all files
echo "3. Додавання файлів..."
git add .
echo "   ✓ Файли додано"
echo ""

# Commit
echo "4. Створення commit..."
read -p "Введіть commit message (Enter для default): " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Initial release v2.0.0 - Production ready Hippocampal CA1 LAM framework"
fi
git commit -m "$COMMIT_MSG"
echo "   ✓ Commit створено"
echo ""

# Add remote
echo "5. Додавання remote..."
git remote add origin "$REPO_URL"
echo "   ✓ Remote додано: $REPO_URL"
echo ""

# Push
echo "6. Push на GitHub..."
echo ""
echo "⚠ ВАЖЛИВО:"
echo "   1. Створіть repository на GitHub: https://github.com/new"
echo "   2. Назва: $REPO_NAME"
echo "   3. НЕ додавайте README, .gitignore, license (вже є)"
echo ""
read -p "Repository створено на GitHub? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Спочатку створіть repository на GitHub"
    exit 1
fi

echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "========================================================================"
echo "✅ УСПІШНО ОПУБЛІКОВАНО НА GITHUB!"
echo "========================================================================"
echo ""
echo "Repository URL: $REPO_URL"
echo ""
echo "Наступні кроки:"
echo "  1. Перейдіть на: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "  2. Створіть Release (Releases → New Release)"
echo "     • Tag: v2.0.0"
echo "     • Title: Hippocampal-CA1-LAM v2.0 - Production Ready"
echo "     • Attach: tar.gz archive"
echo "  3. Enable GitHub Actions (дозволить автоматичні тести)"
echo ""
echo "GitHub Actions будуть автоматично тестувати код при кожному push!"
