# OOPforge Examples

Runnable **place-order** proof projects. Same use case, different layout stacks.

| Skeleton command | Example folder | Stack | OpenAPI |
|---|---|---|---|
| `java-spring-hexagonal` | [order-java](order-java/) | Spring hexagonal (ports/adapters) | springdoc (add in v0.2+) |
| `java-spring-layered` | [order-java-layered](order-java-layered/) | Spring 3-tier (Controller/Service/Repository) | springdoc `/swagger-ui` |
| `python-fastapi-clean` | [order-python](order-python/) | FastAPI hexagonal/clean | FastAPI `/docs` |
| `python-fastapi-layered` | [order-python-layered](order-python-layered/) | FastAPI 3-tier (Router/Service/Repository) | FastAPI `/docs` |

## Quick verify

```bash
cd examples/order-java-layered && ./gradlew test
cd examples/order-python-layered && pip install -e ".[dev]" && pytest
cd examples/order-java && ./gradlew test
cd examples/order-python && pip install -e ".[dev]" && pytest
```

## OOPforge workflow

Pick one stack per project. Start with [library loan walkthrough](../docs/guides/library-loan/README.md) or Craft:

```text
/oopforge:craft place-order in java-spring-layered
```
