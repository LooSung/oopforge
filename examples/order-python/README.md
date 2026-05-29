# Order Python Example

Minimal **FastAPI + hexagonal** reference for OOPforge — mirrors [`order-java`](../order-java/).

## What to look at

| Layer | Path | Role |
|---|---|---|
| Domain | `app/domain/order/model.py` | Aggregate — `Order.place(...)` |
| Domain | `app/domain/order/event.py` | `OrderPlaced` domain event |
| Application | `app/application/services/order/place_order_service.py` | Use case |
| Infrastructure | `app/infrastructure/repositories/order/in_memory_order_repository.py` | Port adapter |
| Presentation | `app/presentation/api/order/order_router.py` | REST → use case |

Domain uses **stdlib only** (`dataclasses`). No FastAPI/Pydantic imports in domain.

## Run

```bash
cd examples/order-python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```

```bash
curl -X POST http://localhost:8000/orders \
  -H 'Content-Type: application/json' \
  -d '{"customer_id":"cust-1","lines":[{"product_id":"p-1","quantity":2,"unit_price":1000}]}'
```

## OOPforge mapping

Same bounded context and use case as the Java example — compare side by side when learning the layout.

See [docs/claude-code.md](../../docs/claude-code.md) and [docs/cursor.md](../../docs/cursor.md).
