---
name: backend-layout
description: Java Spring과 Python FastAPI 백엔드의 layered 또는 hexagonal/clean 패키지 구조를 선택한다.
tags: [backend, layout, java, python, api]
stability: stable
---

# Backend Layout

## 언제 쓰나

Skeleton 단계에서 백엔드 패키지 구조를 만들 때 사용한다.
언어별 세부 레이아웃을 새로 발명하지 말고 아래 선택 기준과 표준 구조를 따른다.

## 선택 기준

| 상황 | 선택 |
|---|---|
| 작은 서비스, MVP, 도메인 1~2개 | layered |
| 도메인 규칙이 복잡함 | hexagonal/clean |
| 외부 adapter가 많음 | hexagonal/clean |
| 팀이 아직 아키텍처 학습 중 | layered로 시작, 경계 규칙은 유지 |

## 공통 규칙

- [ ] domain은 가능한 한 framework import 0을 유지한다.
- [ ] inbound adapter는 request/response 매핑만 맡는다.
- [ ] application service는 orchestration과 transaction boundary만 맡는다.
- [ ] outbound adapter는 repository, external API, messaging 구현만 맡는다.
- [ ] API DTO, ORM entity, domain object를 같은 클래스로 공유하지 않는다.
- [ ] OpenAPI/Swagger는 개발 환경에서 바로 확인 가능해야 한다.
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

- layered를 선택했다는 이유로 service에 모든 비즈니스 규칙을 몰아넣지 않는다.
- hexagonal/clean을 선택했다는 이유로 빈 adapter나 불필요한 interface를 만들지 않는다.
- controller/router가 repository를 직접 호출하지 않는다.
- domain이 web, persistence, framework 설정을 import하지 않는다.
