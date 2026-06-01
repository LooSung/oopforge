---
description: OOPforge Skeleton 단계 — 패키지 구조와 인터페이스 파일 생성
---

**OOPforge Skeleton** 단계를 수행하라.

대상 언어/스택: **$ARGUMENTS**

지원 스택:

| 스택 | 아키텍처 | 언제 |
|---|---|---|
| `java-spring-layered` | 3계층 (Controller/Service/Repository) | 작은 서비스, MVP |
| `java-spring-hexagonal` | 헥사고날 (domain/application/adapter) | 도메인 복잡, 어댑터 다수 |
| `python-fastapi-layered` | 3계층 (Router/Service/Repository) | 작은 서비스, MVP |
| `python-fastapi-clean` | 클린 (domain/application/infrastructure/presentation) | 도메인 복잡 |
| `python-flask-layered` | 3계층 (Blueprint/Service/Repository) | Flask 기반 작은 서비스 |

`java-spring`, `python-fastapi`만 주어지면 사용자에게 "layered인지 hexagonal/clean인지" 묻고 진행한다.

## 스킬 경로

OOPforge 팩 루트는 다음 순서로 찾는다.

1. `$OOPFORGE_HOME`
2. `~/.oopforge`
3. 현재 프로젝트에 설치된 OOPforge pack root

아래 `{pack}`은 그 루트를 의미한다.

## 사전 조건

- `docs/design.md`가 존재해야 한다.
- 없으면 Design 먼저 하도록 안내한다.

## 절차

1. `{pack}/skills/workflow/skeleton.md`를 먼저 읽는다.
2. 언어별 레이아웃 스킬을 반드시 참조한다.
   - `java-spring-layered`: `{pack}/skills/lang/java/spring-layered-layout.md`
   - `java-spring-hexagonal`: `{pack}/skills/lang/java/spring-hexagonal-layout.md`
   - `python-fastapi-layered`: `{pack}/skills/lang/python/fastapi-layered-layout.md`
   - `python-fastapi-clean`: `{pack}/skills/lang/python/clean-fastapi-layout.md`
   - `python-flask-layered`: `{pack}/skills/lang/python/flask-layered-layout.md`
3. API 백엔드라면 `{pack}/skills/lang/api/openapi-conventions.md`도 함께 적용하여 Swagger/OpenAPI를 기본 탑재한다.
4. 패키지 구조를 생성한다.
5. 빈 클래스/인터페이스 파일을 생성한다.
6. 메서드는 시그니처만 작성하고 본문은 `throw new UnsupportedOperationException()` 또는 `raise NotImplementedError`로 둔다.
7. 빌드/실행을 확인한다.
8. 사용자에게 다음을 묻는다.

> Skeleton 검토하고 Implement 시작할 유스케이스를 골라주세요.

## 금지

- 메서드 본문 작성, 단 NotImplementedError류는 허용
- if/for 등 로직 작성
- 비즈니스 룰 작성
- 레이어 의존 규칙 위반
