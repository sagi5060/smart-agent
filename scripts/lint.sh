#!/bin/bash

# Linting script for smart-agent project

echo "Running ruff linter..."
poetry run ruff check .

echo ""
echo "Running black formatter check..."
poetry run black --check .

echo ""
echo "Running isort import sorter check..."
poetry run isort --check-only .

echo ""
echo "Running mypy type checker..."
poetry run mypy src/smart_agent --ignore-missing-imports
