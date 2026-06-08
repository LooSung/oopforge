# OOPforge Examples

One domain — a **calculator with history** — implemented across architectures and stacks. Same use case, different structure, so you compare layouts without re-learning the domain.

| Example | Stack | Architecture |
|---|---|---|
| [calculator-java-layered](calculator-java-layered/) | Spring Boot | 3-tier (controller / service / repository) |
| [calculator-java-hexagonal](calculator-java-hexagonal/) | Spring Boot | hexagonal (ports & adapters) |
| [calculator-java-hexagonal-cqrs](calculator-java-hexagonal-cqrs/) | Spring Boot | hexagonal **+ CQRS** overlay (command/query ports, history) |
| [calculator-python-layered](calculator-python-layered/) | FastAPI | 3-tier (router / service / repository) |
| [calculator-python-hexagonal](calculator-python-hexagonal/) | FastAPI | hexagonal / clean |
| [calculator-python-hexagonal-cqrs](calculator-python-hexagonal-cqrs/) | FastAPI | hexagonal **+ CQRS** overlay (command/query ports, history) |

## How to read them

1. **Start with `*-layered`** — the simplest: `calculate(a, op, b)` returns the result. Each layer is its own folder.
2. **Compare with `*-hexagonal`** — same calculator, but the use case depends on a repository **port** and the domain has zero framework imports.
3. **Then `*-hexagonal-cqrs`** — add **history** by laying CQRS *on top of* hexagonal: the command returns only an ID via the write port; queries read `HistorySummary` projections via a separate read port.

> Two different axes: `layered` vs `hexagonal` is **structure** (how dependencies are arranged); `CQRS` is a **pattern** (split read/write) you overlay on either. So it's not a third peer architecture — and it's not "3-tier vs 4-tier" either; hexagonal is not a tier count. We ship CQRS on hexagonal because its ports map cleanly to command/query sides.

## Quick verify

```bash
cd examples/calculator-java-layered && ./gradlew test
cd examples/calculator-java-hexagonal && ./gradlew test
cd examples/calculator-java-hexagonal-cqrs && ./gradlew test
cd examples/calculator-python-layered && pip install -e ".[dev]" && pytest
cd examples/calculator-python-hexagonal && pip install -e ".[dev]" && pytest
cd examples/calculator-python-hexagonal-cqrs && pip install -e ".[dev]" && pytest
```

## Enforced in CI

`scripts/ci/archlint.py` runs in `.github/workflows/arch-lint.yml` against the layered/CQRS examples — the v0.7 layer-layout and CQRS Hard Rules block the PR if violated.

## OOPforge workflow

Pick one stack per project. Start with the [library loan walkthrough](../docs/guides/library-loan/README.md) or Craft:

```text
/oopforge:craft calculate use case in python-fastapi-layered
/oopforge:craft calculator with history using python-fastapi-clean + CQRS
```
