---
name: lint-enforcement
description: 레이어/경계 Hard Rule을 표준 도구(import-linter, ArchUnit)로 CI에서 강제하는 방법. 가이드만으로 무너지지 않게 기계 강제를 얹는다.
tags: [lint, ci, layered, hexagonal, java, python]
stability: stable
---

# Lint Enforcement

## 언제 쓰나

레이어/경계 규칙을 **문서가 아니라 빌드로 강제**하고 싶을 때. 셀프 체크나 리뷰는 빠뜨릴 수 있으므로, 핵심 Hard Rule은 도구로 자동 차단한다.

두 겹으로 쌓는다:

1. **빠른 stdlib 게이트** — `scripts/ci/archlint.py` (의존성 0, PR 차단). 레이어 폴더 존재·router→repository 금지·CQRS 규칙을 즉시 검사.
2. **표준 도구** — Python은 `import-linter`, Java는 `ArchUnit`. 실제 import 그래프를 분석해 같은 규칙을 한 번 더 증명한다.

새 도구를 발명하지 말고 아래 예제 설정을 **정식 템플릿**으로 복사해 쓴다.

## Python — import-linter

템플릿: `examples/calculator-python-layered/.importlinter`

`.importlinter`를 프로젝트 루트에 두고, dev 의존성에 `import-linter>=2.1`을 추가한다.

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

- `layers` 계약: 하위 레이어가 상위를 import하면 실패(예: domain→service 금지).
- `forbidden` 계약: router가 repository를 **직접** import하면 실패. `allow_indirect_imports = true`는 router→service→repository 같은 정상 간접 경로를 허용하고 직접 위반만 잡는다.

실행:

```bash
pip install -e ".[dev]"
lint-imports
```

## Java — ArchUnit

템플릿: `examples/calculator-java-layered/src/test/java/.../calculator/ArchitectureTest.java`

테스트 의존성만 추가하면 `./gradlew test`에 자연히 포함된다 — 별도 CI 스텝 불필요.

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

- `Repository`를 `Service`만 접근 가능하게 두면 controller→repository 직접 호출이 차단된다.
- domain 프레임워크 의존 0은 별도 규칙으로 검사한다(`noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAnyPackage("org.springframework..", "jakarta..")`).

## CI 연결

- `archlint.py`: `.github/workflows/arch-lint.yml`에서 layered/CQRS 예제에 PR 차단.
- `import-linter`: 같은 워크플로에 `lint-imports` 스텝으로 추가(예제 install 후 실행).
- `ArchUnit`: `./gradlew test`에 포함되므로 examples 워크플로가 그대로 강제.

## 금지

- 규칙을 README 문장으로만 남기고 빌드 강제를 빼지 않는다.
- import-linter `forbidden`에서 `allow_indirect_imports`를 빼서 정상 간접 경로까지 깨뜨리지 않는다.
- ArchUnit 레이어 패키지(`definedBy`)를 실제 폴더와 다르게 적어 규칙이 vacuous하게 통과되게 두지 않는다.
