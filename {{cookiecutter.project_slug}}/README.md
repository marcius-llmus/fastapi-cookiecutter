# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Layout

```
backend/    FastAPI app (src/, tests/, pyproject.toml, Dockerfile, migrations/)
frontend/   placeholder for future frontend
```

## Quickstart

```bash
make install
cp backend/.env.example backend/.env
{% if cookiecutter.use_alembic %}make migrate
{% endif %}make run
```

API at http://localhost:8000, docs at http://localhost:8000/docs.

## Make targets

| Target | What it does |
|---|---|
| `make install` | `uv sync` inside backend/ |
| `make run` | Start uvicorn dev server |
| `make test` | Run pytest |
| `make lint` | Ruff check + format check + mypy |
| `make format` | Ruff format + auto-fix |
| `make up` / `make down` | docker compose up/down |
| `make logs` | Follow backend logs |
{%- if cookiecutter.use_alembic %}
| `make migrate` | Apply migrations through compose |
| `make generate-migration name=<msg>` | Autogenerate migration |
| `make alembic-check` | Detect un-migrated model changes |
{%- endif %}
