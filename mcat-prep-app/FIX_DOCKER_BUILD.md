# Docker Build Error Fix

## Problem
Getting "The lock file does not have a metadata entry" error when building Docker containers.

## Root Cause
Docker is using **cached layers** from before the poetry.lock fix was applied. Even though the Dockerfile now has the correct fix, Docker continues using the old cached layer.

## Solution

### Option 1: Use the provided scripts (RECOMMENDED)
```bash
cd /home/user/Python/mcat-prep-app

# Either use START_HERE.sh
./START_HERE.sh

# Or use REBUILD.sh
./REBUILD.sh
```

Both scripts include the `--no-cache` flag to force Docker to rebuild all layers.

### Option 2: Manual rebuild with --no-cache flag
```bash
cd /home/user/Python/mcat-prep-app

# Stop and remove existing containers
docker-compose down

# Build without cache (IMPORTANT!)
docker-compose build --no-cache

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed database
docker-compose exec backend python scripts/seed_comprehensive.py
```

### Option 3: Clear Docker cache completely
```bash
# Nuclear option - clears ALL Docker build cache
docker builder prune -af

# Then build normally
cd /home/user/Python/mcat-prep-app
docker-compose build
docker-compose up -d
```

## Why This Happens

The Dockerfile was updated to auto-generate poetry.lock:
```dockerfile
RUN poetry config virtualenvs.create false && \
    (poetry check --lock 2>/dev/null || poetry lock --no-update) && \
    poetry install --no-interaction --no-ansi
```

However, Docker caches each layer. When you run `docker build` or `docker-compose build` WITHOUT `--no-cache`, Docker reuses the cached layer from BEFORE this fix was added, causing the error.

## Verification

After rebuilding, you should see poetry.lock being generated during the build:
```
Step X/Y : RUN poetry config virtualenvs.create false && ...
 ---> Running in xxxxx
Skipping virtualenv creation, as specified in config file.
Creating virtualenv
Updating dependencies
Resolving dependencies... (X.Xs)
```

Then the build should complete successfully.
