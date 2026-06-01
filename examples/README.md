# OOPforge Examples

Runnable **place-order** proof projects. Same use case, different layout stacks.

| Skeleton command | Example folder | Stack | OpenAPI |
|---|---|---|---|
| `java-spring-hexagonal` | [order-java](order-java/) | Spring hexagonal (ports/adapters) | springdoc (add in v0.2+) |
| `java-spring-layered` | [order-java-layered](order-java-layered/) | Spring 3-tier (Controller/Service/Repository) | springdoc `/swagger-ui` |
| `python-fastapi-clean` | [order-python](order-python/) | FastAPI hexagonal/clean | FastAPI `/docs` |
| `python-flask-layered` | [order-python-flask](order-python-flask/) | Flask 3-tier (Blueprint/Service/Repository) | flask-smorest `/api/v1/docs` |

> `python-fastapi-layered` uses the same 3-tier idea as Flask; a dedicated FastAPI layered example may follow in a later release.

## Quick verify

```bash
cd examples/order-java-layered && ./gradlew test
cd examples/order-python-flask && pip install -e ".[dev]" && PYTHONPATH=. pytest
cd examples/order-java && ./gradlew test
cd examples/order-python && pip install -e ".[dev]" && pytest
```

## OOPforge workflow

Pick one stack per project. Start with [library loan walkthrough](../docs/guides/library-loan/README.md) or slash commands:

```text
/oopforge:route place-order in java-spring-layered
/oopforge:skeleton java-spring-layered
/oopforge:implement place-order
/oopforge:test place-order
```
