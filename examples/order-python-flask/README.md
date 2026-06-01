# Order Python Flask Example

**Flask 3-tier (Blueprint → Service → Repository)** reference for OOPforge — same `place-order` flow as [`order-python`](../order-python/) (FastAPI hexagonal).

Uses in-memory persistence (no database). OpenAPI via **flask-smorest** (`/api/v1/docs`, `/api/v1/openapi.json`).

## What to look at

| Layer | Path | Role |
|---|---|---|
| Blueprint | `app/order/blueprint.py` | HTTP + schema mapping |
| Service | `app/order/service.py` | Use case orchestration |
| Repository | `app/order/repository.py` | In-memory store |
| Domain | `app/order/domain.py` | Order aggregate logic |

## Run

```bash
cd examples/order-python-flask
pip install -e ".[dev]"
pytest
flask --app wsgi run --debug
```

```bash
curl -X POST http://localhost:5000/api/v1/orders \
  -H 'Content-Type: application/json' \
  -d '{"customer_id":"cust-1","lines":[{"product_id":"p-1","quantity":2,"unit_price":1000}]}'
```

Note: request JSON uses **snake_case** (`customer_id`, `product_id`) per Marshmallow schemas.

Swagger UI: http://localhost:5000/api/v1/docs

## OOPforge skeleton

```text
/oopforge:skeleton python-flask-layered
```

Layout skill: `skills/lang/python/flask-layered-layout.md`
