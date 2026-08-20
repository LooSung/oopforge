---
name: lint-enforcement
description: How to enforce layer/boundary project rules in CI with standard tools (import-linter, ArchUnit). Add machine enforcement so guidance alone does not collapse.
tags: [lint, ci, layered, hexagonal, java, python]
stability: stable
---

# Lint Enforcement

## When to use

When layer or boundary rules must be enforced **by the build, not only docs**.
Self-checks and reviews can be missed, so use executable dependency rules.

Stack it in two layers:

1. **Fast stdlib gate** — `scripts/ci/archlint.py` checks layered folder
   layout, direct router-to-repository imports, and CQRS rules.
2. **Standard tools** — import-linter for Python and ArchUnit for Java inspect
   the actual dependency graph.

Do not invent a new tool. Copy the matching example below as the **canonical
template**, then change only its package names.

## Canonical templates

| Stack | Canonical file | Enforced boundaries |
|---|---|---|
| Python layered | `examples/calculator-python-layered/.importlinter` | layer direction; no direct router-to-repository import |
| Python hexagonal | `examples/calculator-python-hexagonal/.importlinter` | domain independence; application independence; no presentation-to-infrastructure import |
| Java layered | `examples/calculator-java-layered/src/test/java/com/oopforge/example/layered/calculator/ArchitectureTest.java` | layer direction; service-only repository access; framework-free domain |
| Java hexagonal | `examples/calculator-java-hexagonal/src/test/java/com/oopforge/example/calculator/ArchitectureTest.java` | framework-free domain; application-to-adapter ban |

## Python — import-linter

Put `.importlinter` at the project root and add `import-linter>=2.1` to dev
dependencies.

### Layered shape

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

- `layers` rejects lower-to-higher imports.
- `allow_indirect_imports = true` permits router -> service -> repository while
  rejecting a direct router -> repository import.

### Hexagonal shape

```ini
[importlinter]
root_package = app

[importlinter:contract:domain-independence]
name = Domain must not depend on outer packages
type = forbidden
source_modules =
    app.domain
forbidden_modules =
    app.application
    app.core
    app.infrastructure
    app.presentation
allow_indirect_imports = true

[importlinter:contract:application-independence]
name = Application must not depend on adapters or composition
type = forbidden
source_modules =
    app.application
forbidden_modules =
    app.core
    app.infrastructure
    app.presentation
allow_indirect_imports = true

[importlinter:contract:no-presentation-repository]
name = Presentation must not import infrastructure directly
type = forbidden
source_modules =
    app.presentation
forbidden_modules =
    app.infrastructure
allow_indirect_imports = true
```

- Domain and application code cannot depend on outer implementation packages.
- Presentation reaches infrastructure through application wiring, not direct
  imports.

Run `pip install -e ".[dev]" && lint-imports`.

## Java — ArchUnit

Add the test dependency; architecture rules then run inside `./gradlew test`.

```kotlin
testImplementation("com.tngtech.archunit:archunit-junit5:1.3.0")
```

### Layered shape

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

- Repository access through Service blocks direct controller access.
- Add a separate `noClasses()` rule for domain dependencies on
  `org.springframework..`, `jakarta..`, and other project frameworks.

### Hexagonal shape

```java
noClasses()
    .that().resideInAPackage(BASE + ".domain..")
    .should().dependOnClassesThat().resideInAnyPackage(
        "org.springframework..", "jakarta..")
    .check(classes);

noClasses()
    .that().resideInAPackage(BASE + ".application..")
    .should().dependOnClassesThat().resideInAPackage(BASE + ".adapter..")
    .check(classes);
```

## CI and blocking policy

- In OOPforge itself, `lint`, `arch-lint`, and `examples` are repository
  blocking gates. `arch-lint` runs import-linter for both plain Python layered
  and hexagonal examples; `examples` runs ArchUnit through Gradle tests.
- The adopter template
  `templates/github/oopforge-domain-review.yml` is **non-blocking by default**.
  It posts findings and artifacts with a neutral verdict.
- Adopter blocking is **opt-in**: run the copied import-linter contract or
  ArchUnit test in CI and mark that concrete lint/test job as required in
  branch protection. Requiring the feedback-only review job does not make its
  findings fail.

## Prohibited

- Do not describe an adopter's default domain review as blocking.
- Do not remove `allow_indirect_imports` and break valid indirect paths.
- Do not let ArchUnit package patterns differ from real folders and pass
  vacuously.
