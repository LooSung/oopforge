# Order Python Layered Example

**FastAPI 3-tier (Router → Service → Repository)** reference for OOPforge — same `place-order` flow as [`order-python`](../order-python/) (FastAPI hexagonal).

Uses in-memory persistence (no database). OpenAPI via **FastAPI built-in** (`/docs`, `/openapi.json`).

## Run tests

```bash
cd examples/order-python-layered
pip install -e ".[dev]"
pytest
```

## Run locally

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## OOPforge

```text
/oopforge:craft place-order in python-fastapi-layered
```

Skeleton skill: `skills/skeleton/backend-skeleton.md` (stack via `skills/lang/backend-stack.md`)
