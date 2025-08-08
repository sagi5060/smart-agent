#!/bin/bash

# Smart Agent Test Runner Script
# This script provides various ways to run tests with coverage

echo "🧪 Smart Agent Test Suite"
echo "=========================="
echo

# Function to run tests with different options
run_tools_tests() {
    echo "📁 Running Tool Tests..."
    poetry run pytest tests/tools/ -v
}

run_tools_tests_with_coverage() {
    echo "📊 Running Tool Tests with Coverage..."
    poetry run pytest tests/tools/ --cov=src/smart_agent/tools --cov-report=term-missing
}

run_tools_tests_with_html_coverage() {
    echo "🌐 Running Tool Tests with HTML Coverage Report..."
    poetry run pytest tests/tools/ --cov=src/smart_agent/tools --cov-report=html
    echo "📋 HTML Coverage report generated in htmlcov/"
}

run_all_tests() {
    echo "🔍 Running All Tests..."
    poetry run pytest tests/ -v
}

run_all_tests_with_coverage() {
    echo "📈 Running All Tests with Full Coverage..."
    poetry run pytest tests/ --cov=src/smart_agent --cov-report=term-missing --cov-report=html
}

# Parse command line arguments
case "$1" in
    "tools")
        run_tools_tests
        ;;
    "tools-cov")
        run_tools_tests_with_coverage
        ;;
    "tools-html")
        run_tools_tests_with_html_coverage
        ;;
    "all")
        run_all_tests
        ;;
    "all-cov")
        run_all_tests_with_coverage
        ;;
    *)
        echo "Usage: $0 {tools|tools-cov|tools-html|all|all-cov}"
        echo
        echo "Commands:"
        echo "  tools      - Run tool tests only"
        echo "  tools-cov  - Run tool tests with terminal coverage"
        echo "  tools-html - Run tool tests with HTML coverage report"
        echo "  all        - Run all tests"
        echo "  all-cov    - Run all tests with full coverage"
        echo
        echo "Examples:"
        echo "  ./run_tests.sh tools-cov"
        echo "  ./run_tests.sh tools-html"
        exit 1
        ;;
esac
