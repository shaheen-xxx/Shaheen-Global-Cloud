#!/bin/bash
# Setup script for local development

set -e

echo "Setting up Shaheen Global Cloud..."

# Check prerequisites
echo "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed."; exit 1; }

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env created. Please update credentials if needed."
fi

# Create necessary directories
mkdir -p /tmp/dagger-work
mkdir -p /tmp/dagger-cache

echo "✓ Directory structure ready"

# Build and start services
echo "Building Docker images..."
docker-compose build

echo "✓ Setup complete!"
echo ""
echo "To start the development environment, run:"
echo "  docker-compose up"
echo ""
echo "Services will be available at:"
echo "  Frontend: http://localhost:5173"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
