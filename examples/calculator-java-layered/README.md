# Calculator Java Layered Example

Minimal **Spring Boot 3-tier (layered)** reference for OOPforge — the `calculate` use case across `controller / service / repository / domain`, no database (in-memory).

The simplest Java member of the calculator family. For ports & adapters, see [`calculator-java-hexagonal`](../calculator-java-hexagonal/).

Each layer is its **own package/folder** (v0.7 Hard Rule), and the controller goes through the service — never straight to the repository.

## Layout

```text
com/oopforge/example/layered/calculator/
├── controller/   CalculatorController · dto/ (CalculateRequest, CalculationResponse)
├── service/      CalculatorService
├── repository/   CalculationRepository · InMemoryCalculationRepository
└── domain/       Calculation (aggregate) · Operator · events  (0 framework imports)
```

## Run

```bash
cd examples/calculator-java-layered
./gradlew test
./gradlew bootRun
```

- Swagger UI: http://localhost:8080/swagger-ui · OpenAPI: http://localhost:8080/v3/api-docs

```bash
curl -X POST http://localhost:8080/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 6, "operator": "MULTIPLY", "operandB": 7}'
```

## OOPforge

```text
/oopforge:craft calculate use case in java-spring-layered
```

See [examples/README.md](../README.md) for the full calculator family.
