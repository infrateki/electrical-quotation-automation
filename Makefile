# Makefile for Electrical Quotation Automation System

.PHONY: help install dev test lint format clean docker-up docker-down setup

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make dev          - Start development environment"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Clean up generated files"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make setup        - Complete project setup"

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

# Development environment
dev: docker-up
	@echo "Starting development server..."
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	pytest tests/ -v --cov=agents --cov=shared --cov=services --cov=api --cov-report=html

test-watch:
	pytest-watch -- -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

# Linting
lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy .

# Format code
format:
	black .
	isort .

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# Docker commands
docker-up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo "Services are ready!"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v
	docker system prune -f

# Database commands
db-migrate:
	alembic upgrade head

db-rollback:
	alembic downgrade -1

db-reset: docker-down docker-clean docker-up
	@sleep 10
	python scripts/setup_database.py

# Setup commands
setup: install docker-up db-migrate
	@echo "Setting up project..."
	cp .env.example .env
	@echo "Please update .env with your API keys!"
	python scripts/setup_project.py

# Development utilities
shell:
	python -m IPython

docs:
	mkdocs serve

build-docs:
	mkdocs build

# CI/CD commands
ci-test:
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
	docker-compose -f docker-compose.test.yml down

# Agent development
create-agent:
	@read -p "Enter agent name: " agent_name; \
	python scripts/create_agent.py $$agent_name

# Security
security-check:
	bandit -r . -ll -i -x '/tests/'
	safety check
