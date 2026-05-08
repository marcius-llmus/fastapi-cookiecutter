# fastapi-cookiecutter

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template that scaffolds a FastAPI backend matching the strict layered architecture from the `fastapi-backend-architecture` skill:

```
route -> service -> repository -> db
```

## Generated layout

```
src/
├── core/                       # fixed primitives (config, schemas, db, celery)
├── domain/                     # pure models, no imports
├── shared/                     # protocols + DTOs (auth optional)
├── infrastructure/             # protocol implementations
├── apps/<first_app>/           # vertical slice with the route/service/repo trio
├── container/                  # the only composition root (build_*)
└── main.py                     # FastAPI app + lifespan + middleware
tests/
├── conftest.py                 # pytest_plugins aggregates module fixtures
├── unit/<app>/{fixtures,test_*}.py
└── integration/<app>/{fixtures,test_*}.py
```

## Generate

```bash
cookiecutter gh:<you>/fastapi-cookiecutter
# or from a local checkout:
cookiecutter /path/to/fastapi-cookiecutter
```

## Variables

| Variable | Default | Notes |
|---|---|---|
| `project_name` | `FastAPI Backend` | Human-readable name |
| `project_slug` | derived | Top-level python package name |
| `first_app_name` | `wallets` | Plural module name for the sample app |
| `first_app_singular` | `wallet` | Singular module name |
| `first_app_class` | `Wallet` | PascalCase class name |
| `database` | `sqlite` / `postgres` | Driver: `aiosqlite` or `asyncpg` |
| `include_auth` | `false` | Scaffold `apps/auth` + `shared/auth` |
| `use_alembic` | `true` | Scaffold `alembic/` and `alembic.ini` |
| `use_celery` | `true` | Scaffold `core/celery/`, sample `tasks.py`, flow |
| `use_docker` | `true` | Scaffold `Dockerfile` and `docker-compose.yml` |
| `license` | `MIT` / others | Choice |

## After generation

```bash
cd <project_slug>
uv sync
cp .env.example .env
make migrate                  # if use_alembic
make run
```

The generated `README.md` documents per-project commands.

## How conditionals work

This template uses Jinja conditional filenames (no `hooks/` directory) so it
works on systems where post-gen hook scripts cannot be executed. Each
conditional file lives at a path like:

```
{% if cookiecutter.use_docker %}Dockerfile{% endif %}
{% if cookiecutter.use_alembic %}alembic{% endif %}/{% if cookiecutter.use_alembic %}env.py{% endif %}
```

When the flag is `False`, the path renders to empty and cookiecutter skips it.
Both the directory name and each child filename must be wrapped to avoid
re-parenting children into the parent directory.

## Verify locally

```bash
cookiecutter --no-input -o /tmp/out . project_name="Demo"
```

Pass overrides like `use_celery=False` on the CLI to test variants.

