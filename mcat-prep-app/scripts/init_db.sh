#!/bin/bash
# Initialize database with migrations and seed data

set -e

echo "🔧 Initializing MCAT Prep database..."

# Run migrations
echo "📦 Running database migrations..."
docker-compose exec backend alembic upgrade head

# Seed database
echo "🌱 Seeding database with initial data..."
docker-compose exec backend python scripts/seed_database.py

echo "✅ Database initialization complete!"
