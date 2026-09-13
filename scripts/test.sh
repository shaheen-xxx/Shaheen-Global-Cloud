#!/bin/bash
# Test script for running all tests

set -e

echo "Running Shaheen Global Cloud tests..."
echo ""

# Backend tests
echo "====== Backend Tests ======"
cd backend
echo "Running pytest..."
pytest -v --tb=short 2>&1 || {
    echo "✗ Backend tests failed"
    exit 1
}
echo "✓ Backend tests passed"
cd ..
echo ""

# Frontend build
echo "====== Frontend Build ======"
cd frontend
echo "Installing dependencies..."
npm install --prefer-offline --no-audit 2>&1 || {
    echo "✗ Failed to install frontend dependencies"
    exit 1
}
echo "Building frontend..."
npm run build 2>&1 || {
    echo "✗ Frontend build failed"
    exit 1
}
echo "✓ Frontend build succeeded"
cd ..
echo ""

echo "====== All Tests Passed ======"
echo "✓ Backend tests: PASSED"
echo "✓ Frontend build: PASSED"
echo ""
echo "You can now run 'docker-compose up' to start the development environment."
