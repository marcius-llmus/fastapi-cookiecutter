.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory
SHELL := /bin/bash

BACKEND := backend
COMPOSE ?= docker compose

.PHONY: help install lint format test run up down logs {% if cookiecutter.use_alembic %}migrate generate-migration alembic-check{% endif %}

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install backend dependencies
	cd $(BACKEND) && uv sync

lint: ## Run lint and type checks
	cd $(BACKEND) && uv run ruff format --check .
	cd $(BACKEND) && uv run ruff check .
	cd $(BACKEND) && uv run mypy src

format: ## Auto-fix formatting
	cd $(BACKEND) && uv run ruff format .
	cd $(BACKEND) && uv run ruff check --fix .

test: ## Run the backend test suite
	cd $(BACKEND) && ENVIRONMENT=test uv run pytest

run: ## Start the backend dev server
	cd $(BACKEND) && uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

up: ## Start the local Docker stack
	$(COMPOSE) up -d --build

down: ## Stop the local Docker stack
	$(COMPOSE) down

logs: ## Follow backend logs
	$(COMPOSE) logs -f backend
{% if cookiecutter.use_alembic %}
{%- if cookiecutter.database == "postgres" %}
ALEMBIC := $(COMPOSE) run --rm --no-deps backend uv run alembic

migrate: ## Apply Alembic migrations through the compose backend
	$(COMPOSE) up -d --wait db
	$(COMPOSE) build backend
	$(ALEMBIC) upgrade head

alembic-check: ## Verify Alembic has no pending model/schema drift
	$(COMPOSE) up -d --wait db
	$(COMPOSE) build backend
	$(ALEMBIC) check

generate-migration: ## Create a new Alembic migration (usage: make generate-migration name="description")
	@test -n "$(name)" || (echo 'usage: make generate-migration name="description"' && exit 1)
	$(COMPOSE) up -d --wait db
	$(COMPOSE) build backend
	$(ALEMBIC) revision --autogenerate -m "$(name)"
{%- else %}
migrate: ## Apply Alembic migrations
	cd $(BACKEND) && uv run alembic upgrade head

alembic-check: ## Verify Alembic has no pending model/schema drift
	cd $(BACKEND) && uv run alembic check

generate-migration: ## Create a new Alembic migration (usage: make generate-migration name="description")
	@test -n "$(name)" || (echo 'usage: make generate-migration name="description"' && exit 1)
	cd $(BACKEND) && uv run alembic revision --autogenerate -m "$(name)"
{%- endif %}
{% endif %}
