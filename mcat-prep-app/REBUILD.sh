#!/bin/bash
# Quick fix script to rebuild Docker containers without cache

set -e

echo "🔧 Rebuilding MCAT Prep Application (No Cache)"
echo "This will take 5-10 minutes but ensures all changes are applied"
echo ""

# Stop and remove existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old images to force rebuild
echo "🗑️  Removing old images..."
docker-compose rm -f backend frontend 2>/dev/null || true

# Build without cache
echo "🔨 Building containers from scratch..."
docker-compose build --no-cache

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run migrations
echo "📊 Running database migrations..."
docker-compose exec backend alembic upgrade head

# Seed database
echo "🌱 Seeding database..."
docker-compose exec backend python scripts/seed_comprehensive.py

echo ""
echo "✅ Rebuild complete!"
echo ""
echo "Access the app at: http://localhost:5173"
echo "Login: demo@mcatprep.com / demo123"
