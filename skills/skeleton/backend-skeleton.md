---
name: backend-skeleton
description: 선택된 백엔드 스택으로 표준 패키지 구조와 빈 타입을 만드는 스켈레톤 규칙.
tags: [backend, skeleton, java, python]
stability: stable
---

# Backend Skeleton

## 언제 쓰나

Skeleton 단계에서 **이미 선택된 스택**으로 패키지 구조를 만들 때 사용한다.
스택이 아직 없으면 먼저 `skills/lang/backend-stack.md`로 하나를 고른다.
언어별 세부 레이아웃을 새로 발명하지 말고 아래 표준 구조를 따른다.

## 공통 규칙

- [ ] domain은 가능한 한 framework import 0을 유지한다.
- [ ] inbound adapter는 request/response 매핑만 맡는다.
- [ ] application service는 orchestration과 transaction boundary만 맡는다.
- [ ] outbound adapter는 repository, external API, messaging 구현만 맡는다.
- [ ] API DTO, ORM entity, domain object를 같은 클래스로 공유하지 않는다.
- [ ] 테스트 폴더는 production 구조를 미러링한다.

## Java Spring

### Layered

```text
src/main/java/com/example/order/
├── controller/
├── service/
├── repository/
├── domain/
├── config/
└── infrastructure/
```

### Hexagonal

```text
src/main/java/com/example/order/
├── domain/
├── application/
│   ├── provided/
│   ├── required/
│   └── service/
├── adapter/
│   ├── web/
│   ├── persistence/
│   └── integration/
└── config/
```

Java API는 `springdoc-openapi`로 `/swagger-ui` 또는 `/v3/api-docs`를 노출한다.
JPA가 필요하면 domain model과 JPA entity를 분리하고 adapter에서 mapper로 변환한다.

## Python FastAPI

### Layered

```text
app/order/
├── router.py
├── service.py
├── repository.py
├── models.py
├── schemas.py
└── exceptions.py
```

### Clean

```text
app/
├── domain/
├── application/
├── infrastructure/
├── presentation/
├── config/
└── shared/
```

FastAPI는 OpenAPI를 기본 생성한다. `docs_url`, `openapi_url`, tags, response model, error schema를 명시한다.
SQLAlchemy 모델은 domain object와 분리하는 것을 기본으로 한다.

## 금지

- 메서드 본문을 작성하지 않는다. `UnsupportedOperationException` 또는 `NotImplementedError`로 둔다.
- layered를 선택했다는 이유로 service에 모든 비즈니스 규칙을 몰아넣지 않는다.
- hexagonal/clean을 선택했다는 이유로 빈 adapter나 불필요한 interface를 만들지 않는다.
- controller/router가 repository를 직접 호출하지 않는다.
- domain이 web, persistence, framework 설정을 import하지 않는다.
