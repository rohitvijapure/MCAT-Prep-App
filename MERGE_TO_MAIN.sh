#!/bin/bash
# Script to merge MCAT Prep Application to main branch
# Run this with admin/maintainer privileges

set -e

echo "🔀 Merging MCAT Prep Application code to main branch"
echo ""

# Navigate to repo
cd /home/user/Python

# Fetch latest
echo "📥 Fetching latest changes..."
git fetch origin

# Checkout main
echo "🔄 Checking out main branch..."
git checkout main

# Merge the feature branch
echo "🔀 Merging feature branch into main..."
git merge origin/claude/mcat-prep-app-013vDDhvGbjD1NDVS3y3m7AG -m "Merge: Docker build fixes for production deployment

- Auto-generate poetry.lock during Docker build
- Add REBUILD.sh script for forcing clean rebuilds
- Ensures all Docker layers are rebuilt without cache

This completes the MCAT Prep Application for Nov 19, 2025 launch."

# Push to remote main (requires appropriate permissions)
echo "⬆️  Pushing to remote main..."
git push origin main

echo ""
echo "✅ Successfully merged to main!"
echo ""
echo "📊 Merge summary:"
git log origin/main..main --oneline
echo ""
echo "🚀 Application is ready for Nov 19, 2025 launch!"
