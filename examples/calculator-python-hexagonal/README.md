# Calculator Python Hexagonal Example

**FastAPI hexagonal / clean** reference for OOPforge — same `calculate` use case as [`calculator-python-layered`](../calculator-python-layered/), but with ports & adapters instead of plain layers.

Domain has **zero** framework imports; the use case depends on a repository **port** (Protocol), and the in-memory adapter implements it.

## Layout

```text
app/
├── domain/calculation/        model.py (Calculation, Operator, events) · value.py (CalculationId) · repository.py (port)
├── application/services/calculation/   calculate_service.py (use case)
├── infrastructure/repositories/calculation/  in_memory_calculation_repository.py (adapter)
└── presentation/api/calculation/       router.py · request.py
```

Layered vs hexagonal — same calculator, two dependency styles. For the read/write split layered on top of this, see [`calculator-python-hexagonal-cqrs`](../calculator-python-hexagonal-cqrs/).

## Run tests

```bash
cd examples/calculator-python-hexagonal
pip install -e ".[dev]"
pytest
```

## Run locally

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs

```bash
curl -X POST http://127.0.0.1:8000/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operand_a": 10, "operator": "subtract", "operand_b": 4}'
```

## OOPforge

```text
/oopforge:craft calculate use case in python-fastapi-clean
```
