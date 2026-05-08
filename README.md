# fastapi-cookiecutter

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for a layered
FastAPI backend in a monorepo layout (`backend/` + `frontend/` siblings),
aligned with the architecture enforced by the `fastapi-backend-architecture`
skill: `route -> service -> repository -> db`.

## Generated layout

```
<project_slug>/
├── Makefile                        # delegates code targets into backend/, runs compose at root
├── docker-compose.yml              # db (postgres only) + backend; frontend block commented
├── README.md
├── .gitignore
├── .python-version
├── frontend/.gitkeep               # placeholder until a real frontend lands
└── backend/
    ├── Dockerfile
    ├── .dockerignore
    ├── .env.example
    ├── pyproject.toml              # hatchling, ruff (line=120), mypy, py3.14
    ├── main.py                     # re-exports `app` and `create_app`
    ├── alembic.ini                 # if use_alembic
    ├── migrations/                 # if use_alembic
    ├── src/
    │   ├── main.py                 # FastAPI lifespan + middleware + create_app()
    │   ├── apps/
    │   │   ├── health/             # working /api/v1/health
    │   │   └── example_app/        # empty stub showing the per-app layout
    │   ├── container/              # composition root (lifecycle.py, core/db.py, core/dependencies.py)
    │   ├── core/                   # fixed primitives (config, db, schemas)
    │   ├── shared/schemas/         # cross-app DTOs (Page[TItem], IdResponse)
    │   ├── domain/                 # pure models, imports nothing
    │   └── infrastructure/         # protocol implementations
    └── tests/unit/health/test_routes.py   # smoke test on /api/v1/health
```

## Generate

```bash
cookiecutter gh:marcius-llmus/fastapi-cookiecutter
# or from a local checkout:
cookiecutter /path/to/fastapi-cookiecutter
```

## Variables

| Variable | Default | Notes |
|---|---|---|
| `project_name` | `FastAPI Backend` | Human-readable name |
| `project_slug` | derived | Top-level directory + python package name |
| `project_description` | `Layered FastAPI backend.` | Used in pyproject + main.py title |
| `database` | `sqlite` / `postgres` | Selects `aiosqlite` or `asyncpg`, plus a `db` service in compose for postgres |
| `use_alembic` | `true` | Scaffolds `backend/alembic.ini` + `backend/migrations/` |
| `license` | `MIT` / `Apache-2.0` / `BSD-3-Clause` / `Proprietary` | Sets `[project].license` |

Docker is always shipped (`Dockerfile` + `docker-compose.yml`); there is no
flag to opt out.

## After generation

```bash
cd <project_slug>
make install                # cd backend && uv sync
make migrate                # alembic upgrade head (local for sqlite, via compose for postgres)
make run                    # uvicorn src.main:app --reload
```

API at http://localhost:8000, docs at http://localhost:8000/docs.

`backend/.env.example` is provided as a hint — `DevelopmentSettings` already
ships sensible defaults, so creating `backend/.env` is optional.

## How conditionals work

This template uses Jinja conditional filenames (no `hooks/` directory) so it
works on systems where post-gen hook scripts cannot be executed. Conditional
files live at paths like:

```
backend/{% if cookiecutter.use_alembic %}alembic.ini{% endif %}
backend/{% if cookiecutter.use_alembic %}migrations{% endif %}/{% if cookiecutter.use_alembic %}env.py{% endif %}
```

When the flag is `False`, the path renders to empty and cookiecutter skips it.
Both the directory name and each child filename must be wrapped to avoid
re-parenting children into the parent directory.

## Verify locally

```bash
cookiecutter --no-input -o /tmp/out . database=sqlite
cd /tmp/out/fastapi_backend
make install && make lint && make test
```

Swap `database=postgres` to verify the postgres variant. Both pass `lint`
(ruff + mypy) and `test` (1 smoke test against `/api/v1/health`) out of the
box.
