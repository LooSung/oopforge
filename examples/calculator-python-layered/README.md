# Calculator Python Layered Example

**FastAPI 3-tier (Router → Service → Repository)** reference for OOPforge.

Same `calculate` use case as [`calculator-java-layered`](../calculator-java-layered/), and the simplest member of the calculator family (no history). For the read/write split, see [`calculator-python-hexagonal-cqrs`](../calculator-python-hexagonal-cqrs/).

Each layer is its **own folder** (v0.7 Hard Rule), and the router never touches the repository directly — wiring lives in `app/core/dependencies.py`.

## Layout

```text
app/calculator/
├── router/        calculator_router.py   (HTTP in/out only)
├── service/       calculator_service.py  (orchestration)
├── repository/    calculation_repository.py (in-memory)
├── domain/        calculation.py         (Calculation aggregate, 0 framework imports)
└── schemas/       api_models.py          (request/response DTOs)
```

## Run tests

```bash
cd examples/calculator-python-layered
pip install -e ".[dev]"
pytest
```

## Run locally

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs

```bash
curl -X POST http://127.0.0.1:8000/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operand_a": 8, "operator": "divide", "operand_b": 2}'
```

## OOPforge

```text
/oopforge:craft calculate use case in python-fastapi-layered
```

Skeleton skill: `skills/skeleton/backend-skeleton.md` · stack via `skills/lang/backend-stack.md`
