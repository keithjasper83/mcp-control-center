.PHONY: help install dev test lint format clean run docker-build docker-up seed

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -e .

dev: ## Install development dependencies
	pip install -e '.[dev]'
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=backend/app --cov-report=html --cov-report=term

lint: ## Run linters
	ruff check backend/
	mypy backend/app
	bandit -r backend/app

format: ## Format code
	black backend/
	isort backend/
	ruff check --fix backend/

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -f .coverage
	rm -f mcpcc.db

run: ## Run the application
	uvicorn backend.app.main:app --reload

init: ## Initialize database
	python -m backend.app.cli init

seed: ## Seed database with demo data
	python -m backend.app.cli seed

docker-build: ## Build Docker image
	cd ops && docker-compose build

docker-up: ## Start Docker containers
	cd ops && docker-compose up

docker-down: ## Stop Docker containers
	cd ops && docker-compose down

docker-logs: ## View Docker logs
	cd ops && docker-compose logs -f
