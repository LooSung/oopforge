---
name: lint-enforcement
description: How to enforce layer/boundary Hard Rules in CI with standard tools (import-linter, ArchUnit). Add machine enforcement so guidance alone does not collapse.
tags: [lint, ci, layered, hexagonal, java, python]
stability: stable
---

# Lint Enforcement

## When to use

When you want to enforce layer/boundary rules **via the build, not docs**. Self-checks and reviews can be missed, so block the core Hard Rules automatically with tools.

Stack it in two layers:

1. **Fast stdlib gate** — `scripts/ci/archlint.py` (0 dependencies, blocks the PR). Instantly checks layer-folder existence, the router->repository ban, and CQRS rules.
2. **Standard tools** — `import-linter` for Python, `ArchUnit` for Java. Analyze the actual import graph to prove the same rules once more.

Do not invent a new tool; copy the example configs below as the **canonical template**.

## Python — import-linter

Template: `examples/calculator-python-layered/.importlinter`

Put `.importlinter` at the project root and add `import-linter>=2.1` to dev dependencies.

```ini
[importlinter]
root_package = app

[importlinter:contract:layers]
name = Layers (router > service > repository > domain)
type = layers
layers =
    app.calculator.router
    app.calculator.service
    app.calculator.repository
    app.calculator.domain

[importlinter:contract:no-router-repository]
name = Router must not import repository directly
type = forbidden
source_modules =
    app.calculator.router
forbidden_modules =
    app.calculator.repository
allow_indirect_imports = true
```

- The `layers` contract fails if a lower layer imports a higher one (e.g., domain->service is banned).
- The `forbidden` contract fails if the router imports the repository **directly**. `allow_indirect_imports = true` allows the normal indirect path (router->service->repository) and catches only direct violations.

Run:

```bash
pip install -e ".[dev]"
lint-imports
```

## Java — ArchUnit

Template: `examples/calculator-java-layered/src/test/java/.../calculator/ArchitectureTest.java`

Adding only the test dependency naturally includes it in `./gradlew test` — no separate CI step needed.

```kotlin
testImplementation("com.tngtech.archunit:archunit-junit5:1.3.0")
```

```java
layeredArchitecture().consideringOnlyDependenciesInLayers()
    .layer("Controller").definedBy(BASE + ".controller..")
    .layer("Service").definedBy(BASE + ".service..")
    .layer("Repository").definedBy(BASE + ".repository..")
    .layer("Domain").definedBy(BASE + ".domain..")
    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service")
    .whereLayer("Domain").mayOnlyBeAccessedByLayers("Controller", "Service", "Repository")
    .check(classes);
```

- Making `Repository` accessible only by `Service` blocks direct controller->repository calls.
- Check 0 domain framework dependencies as a separate rule (`noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAnyPackage("org.springframework..", "jakarta..")`).

## CI wiring

- `archlint.py`: blocks PRs on the layered/CQRS examples in `.github/workflows/arch-lint.yml`.
- `import-linter`: add as a `lint-imports` step in the same workflow (run after installing the example).
- `ArchUnit`: included in `./gradlew test`, so the examples workflow enforces it as-is.

## Prohibited

- Do not leave a rule as a README sentence only and drop build enforcement.
- Do not remove `allow_indirect_imports` from the import-linter `forbidden` contract and break normal indirect paths.
- Do not write ArchUnit layer packages (`definedBy`) differently from the actual folders, letting the rule pass vacuously.
