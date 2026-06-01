---
name: python-clean-fastapi-layout
description: FastAPI 프로젝트의 클린/헥사고날 패키지 구조와 의존 규칙.
tags: [python, fastapi, hexagonal, layout]
stability: stable
---

# Python — Clean FastAPI Layout

## 언제 쓰나
FastAPI 기반 새 서비스/모듈을 시작할 때. OOPforge Python 프로젝트의 기본 레이아웃.

## 기준
대형 FastAPI 백엔드에서 쓰는 `app/application/domain/infrastructure/presentation/shared` 구조를 OOPforge용으로 일반화한다.
회사/제품 전용 배포 티어, 인증명, DB/버킷명은 포함하지 않는다.

## 체크리스트
- [ ] 큰 영역: `application`, `domain`, `infrastructure`, `presentation`, `shared`
- [ ] domain 레이어는 FastAPI/SQLAlchemy import 0
- [ ] API 요청/응답 모델 ≠ 도메인 값 객체
- [ ] 의존성 주입은 FastAPI `Depends` 또는 직접 생성자 주입
- [ ] bounded context 별로 domain/application/infrastructure/presentation 하위 구조를 미러링
- [ ] `pyproject.toml` 로 패키지 관리
- [ ] OpenAPI 문서 자동 노출 — `/api/v1/docs`, `tags`, `response_model`, `responses` 컨벤션 (`skills/lang/api/openapi-conventions.md` 참조)

## 표준 레이아웃

```text
app/
├── main.py                              ← FastAPI app 생성
│
├── application/                         ← use case orchestration
│   ├── dto/
│   │   └── order/
│   └── services/
│       └── order/
│           ├── place_order_service.py
│           └── cancel_order_service.py
│
├── domain/                              ← framework import 0
│   ├── order/
│   │   ├── model.py                     ← Aggregate, Entity
│   │   ├── value.py                     ← Value Objects
│   │   ├── event.py                     ← Domain Events
│   │   ├── repository.py                ← Repository Protocol
│   │   └── indexes/                     ← optional index specs
│   └── shared/
│       └── value.py
│
├── infrastructure/                      ← outbound adapters
│   ├── dependencies/
│   │   └── order/
│   │       └── order_dependencies.py
│   ├── repositories/
│   │   └── order/
│   │       └── order_repository.py
│   ├── persistence/
│   │   ├── relationdb/
│   │   ├── documentdb/
│   │   ├── objectstorage/
│   │   └── messaging/
│   ├── external/
│   │   └── payment_gateway.py
│   └── shared/
│
├── presentation/                        ← inbound adapters
│   └── api/
│       ├── order/
│       │   ├── order_router.py
│       │   ├── request.py
│       │   └── response.py
│       └── shared/
│
├── config/
│   ├── settings.py
│   └── dependencies.py
│
└── shared/
    ├── exception/
    ├── logger/
    └── utils/

tests/
├── unit/
│   └── order/
├── integration/
│   └── order/
└── e2e/
```

## 포트 인터페이스 (Protocol)

```python
# app/domain/order/repository.py
from typing import Optional, Protocol
from .model import Order
from .value import OrderId

class OrderRepository(Protocol):
    def find_by_id(self, id: OrderId) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...
```

## 의존성 주입 (FastAPI)

```python
# app/presentation/api/order/order_router.py
from fastapi import APIRouter, Depends
from app.application.services.order.place_order_service import PlaceOrderService
from app.infrastructure.dependencies.order.order_dependencies import get_place_order_service

router = APIRouter()

@router.post("/orders")
def place_order(
    req: PlaceOrderRequest,
    use_case: PlaceOrderService = Depends(get_place_order_service),
):
    order_id = use_case.execute(req.to_command())
    return {"order_id": order_id.value}
```

## 의존 규칙

```text
presentation ──→ application ──→ domain
                      ▲            ▲
                      │            │
          infrastructure.dependencies
                      │
          infrastructure.repositories/external
```

- `domain` 은 어떤 레이어도 import 하지 않는다.
- `application` 은 domain port/protocol에만 의존한다.
- `presentation` 은 application service를 호출한다.
- `infrastructure.repositories/external` 은 domain port를 구현한다.
- `infrastructure.dependencies` 는 wiring만 담당한다.

## 금지
- **domain 모듈에서 `from fastapi import`, `from sqlalchemy import`** — 절대.
- **API request 모델을 도메인 객체로 직접 사용** — 항상 매핑.
- **`global` 변수로 repository 보유** — DI 또는 Depends 사용.
- **유스케이스 안에서 `requests.get(...)` 직접 호출** — 항상 port 경유.
- **순환 import** — 모듈 분리 신호.
- **회사/제품 전용 tier, bucket, auth 이름을 기본 템플릿에 고정 금지** — 프로젝트 `AGENTS.md`에서만 정의.

## 도구 추천
- 패키징: `uv` 또는 `poetry`
- 린트: `ruff`
- 타입: `mypy`
- 의존 규칙 강제: `import-linter`
