# Calculator Python Hexagonal + CQRS Example

CQRS is **not a third architecture** next to layered/hexagonal — it's a read/write split you lay **on top of** one. This example shows it on [`calculator-python-hexagonal`](../calculator-python-hexagonal/), where it fits most naturally: the write and read sides each get their **own port**.

- **Command** (`POST /api/v1/calculations`) → `CalculateCommandService` via the write port `CalculationRepository`, returns `calculation_id` only.
- **Query** (`GET /api/v1/calculations/history`, `GET /api/v1/calculations/{id}`) → `HistoryQueryService` via the read port `HistoryQueryRepository`, returns `HistorySummary` read models (never loads the aggregate).

Both adapters share one in-memory `CalculationStore`; the write adapter projects each calculation into the history read model.

## Layout

```text
app/
├── domain/calculation/          model.py · value.py · repository.py  ← write port
├── application/
│   ├── command/                 calculate_command_service.py
│   └── query/                   history_query_service.py · history_query_repository.py (read port) · history_summary.py (read model)
├── infrastructure/repositories/ store.py · in_memory_calculation_repository.py (write adapter) · in_memory_history_query_repository.py (read adapter)
└── presentation/api/            command_router.py · query_router.py · schemas.py
```

> Progression: [`*-layered`](../calculator-python-layered/) (simplest) → [`*-hexagonal`](../calculator-python-hexagonal/) (ports & adapters) → **this** (hexagonal + CQRS).

## Run tests

```bash
cd examples/calculator-python-hexagonal-cqrs
pip install -e ".[dev]"
pytest
```

## Run locally

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs

## CI

`scripts/ci/archlint.py cqrs` runs on this example in `.github/workflows/arch-lint.yml` — query side stays read-only, command side returns no read-shaped data.

## OOPforge

```text
/oopforge:craft calculator with history using python-fastapi-clean + CQRS
```

See [`skills/oop/cqrs.md`](../../skills/oop/cqrs.md).
