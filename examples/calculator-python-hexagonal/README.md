# Calculator Python Hexagonal Example

**FastAPI hexagonal / clean** reference for OOPforge — same `calculate` use case as [`calculator-python-layered`](../calculator-python-layered/), but with ports & adapters instead of plain layers.

Domain has **zero** framework imports; the use case depends on a repository **port** (Protocol), and the in-memory adapter implements it.

## Layout

```text
app/
├── domain/calculation/        model.py (Calculation, Operator, events) · value.py (CalculationId) · repository.py (port)
├── application/               domain_events.py · outbox.py · transactions.py · services/calculation/
├── infrastructure/            in_memory_transaction.py · in_memory_outbox.py · event_relay.py
│   └── repositories/calculation/  in_memory_calculation_repository.py
└── presentation/api/calculation/       router.py · request.py
```

Layered vs hexagonal — same calculator, two dependency styles. For the read/write split layered on top of this, see [`calculator-python-hexagonal-cqrs`](../calculator-python-hexagonal-cqrs/).

The calculate transaction saves the Aggregate, drains its event once, and
dispatches a handler that appends immutable `CalculationPerformedV1` to the
outbox. The relay runs after commit and its consumer deduplicates by message ID.

The HTTP adapter validates finite operands and request shape, emits safe errors,
replays matching `Idempotency-Key` requests, rejects key conflicts, echoes
`X-Correlation-Id`, and records a secret-free audit entry. Its idempotency,
audit, repository, and outbox stores are process-local reference adapters; use
durable shared adapters for a real multi-instance deployment.

## Run tests

```bash
cd examples/calculator-python-hexagonal
pip install -e ".[dev]"
python -m mypy
pytest
lint-imports
```

`lint-imports` enforces domain and application independence and rejects direct
presentation-to-infrastructure imports. The architecture-lint workflow runs
this check as a blocking repository gate.

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
