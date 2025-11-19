# Base stage
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

# Install poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy only pyproject.toml (we'll generate lock file fresh)
COPY pyproject.toml ./

# Configure poetry and generate lock file, then install dependencies
RUN poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Install poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy only pyproject.toml (we'll generate lock file fresh)
COPY pyproject.toml ./

# Configure poetry and generate lock file, then install production dependencies only
RUN poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install --no-interaction --no-ansi --no-dev

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
