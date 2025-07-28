# Multi-stage Dockerfile for Electrical Quotation Automation

# Stage 1: Base image with dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development image
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    ipython \
    ipdb \
    pytest-watch

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p logs uploads temp

# Expose port
EXPOSE 8000

# Development command
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage 3: Production image
FROM base as production

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy only necessary files
COPY --chown=appuser:appuser ./agents ./agents
COPY --chown=appuser:appuser ./shared ./shared
COPY --chown=appuser:appuser ./services ./services
COPY --chown=appuser:appuser ./api ./api
COPY --chown=appuser:appuser ./alembic.ini ./alembic.ini

# Create necessary directories
RUN mkdir -p logs uploads temp && \
    chown -R appuser:appuser logs uploads temp

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Production command with proper worker configuration
CMD ["gunicorn", "api.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

# Stage 4: Testing image
FROM base as testing

# Install testing dependencies
RUN pip install --no-cache-dir \
    pytest-xdist \
    pytest-timeout \
    pytest-env

# Copy the entire project
COPY . .

# Run tests
CMD ["pytest", "tests/", "-v", "--tb=short"]
