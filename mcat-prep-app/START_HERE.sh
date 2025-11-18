#!/bin/bash
# MCAT Prep Application - Complete Setup and Launch Script
# Run this script to set up and launch the application for the first time

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        MCAT Prep Application - Complete Setup             ║"
echo "║        Launch Date: November 19, 2025                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Step 1: Environment setup
echo "📝 Step 1: Setting up environment variables..."
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo "✅ Created .env.local from .env.example"
else
    echo "✅ .env.local already exists"
fi
echo ""

# Step 2: Build and start containers
echo "🐳 Step 2: Building and starting Docker containers..."
echo "This may take 5-10 minutes on first run..."
echo "Building without cache to ensure latest changes..."
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo ""
echo "🔍 Checking service status..."
docker-compose ps
echo ""

# Step 3: Run database migrations
echo "📊 Step 3: Running database migrations..."
docker-compose exec backend alembic upgrade head
echo "✅ Database migrations complete"
echo ""

# Step 4: Seed database with comprehensive content
echo "🌱 Step 4: Seeding database with comprehensive MCAT content..."
echo "Creating 60+ verified MCAT questions..."
docker-compose exec backend python scripts/seed_comprehensive.py
echo "✅ Database seeded successfully"
echo ""

# Display success message
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              🎉 Setup Complete! 🎉                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📱 Access the application:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend API: http://localhost:8000/docs"
echo ""
echo "👤 Demo Login Credentials:"
echo "   Email:    demo@mcatprep.com"
echo "   Password: demo123"
echo ""
echo "   OR"
echo ""
echo "   Email:    student@mcatprep.com"
echo "   Password: student123"
echo ""
echo "🎯 Features Available:"
echo "   ✓ 60+ verified MCAT practice questions"
echo "   ✓ Full quiz interface with timer"
echo "   ✓ Instant feedback and detailed explanations"
echo "   ✓ Analytics dashboard with charts"
echo "   ✓ Concept mastery tracking"
echo "   ✓ Progress visualization"
echo "   ✓ Review queue for missed questions"
echo ""
echo "📚 Content Coverage:"
echo "   - CPBS: Chemical & Physical Foundations"
echo "   - BBLS: Biological & Biochemical Foundations"
echo "   - PSBB: Psychological & Social Foundations"
echo "   - Topics: Amino Acids, Thermodynamics, Cell Biology, Genetics, and more"
echo ""
echo "🛠️  Useful Commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop app:      docker-compose down"
echo "   Restart:       docker-compose restart"
echo "   Reset DB:      docker-compose down -v && ./START_HERE.sh"
echo ""
echo "🚀 Ready to launch! Open http://localhost:5173 in your browser."
echo ""
