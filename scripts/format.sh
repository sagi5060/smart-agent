#!/bin/bash

# Auto-fix linting issues for smart-agent project

echo "Running ruff linter with auto-fix..."
poetry run ruff check . --fix

echo ""
echo "Running black formatter..."
poetry run black .

echo ""
echo "Running isort import sorter..."
poetry run isort .

echo ""
echo "Linting fixes complete!"
