---
name: python-fastapi-layered-layout
description: FastAPI 3계층(Router/Service/Repository) 레이아웃. 클린 아키텍처까지 필요 없는 작은 서비스의 기본 출발점.
tags: [python, fastapi, layered, layout]
stability: stable
---

# Python — FastAPI Layered Layout (3-tier)

## 언제 쓰나
- 작은 FastAPI 서비스 (단일 도메인 또는 1~3개)
- 팀이 헥사고날/클린 아키텍처 도입 비용을 감당하기 어려운 초기
- MVP 단계, 도메인이 자라면 `clean-fastapi-layout.md`로 마이그레이션 예정

복잡도가 처음부터 높거나 외부 어댑터가 다수면 `clean-fastapi-layout.md`를 쓴다.

## 기준
`router → service → repository` 3계층 + `models`/`schemas` + `core`(설정/공통). FastAPI 표준 튜토리얼 구조의 OOPforge 버전.

## 체크리스트
- [ ] 큰 영역: `routers`, `services`, `repositories`, `models`, `schemas`, `core`, `infrastructure`
- [ ] `routers` → FastAPI APIRouter, request/response 매핑, DI
- [ ] `services` → 비즈니스 로직, 트랜잭션 경계
- [ ] `repositories` → DB 접근 (SQLAlchemy session)
- [ ] `models` → SQLAlchemy ORM 엔티티 또는 도메인 클래스
- [ ] `schemas` → Pydantic request/response 모델 (≠ ORM 모델)
- [ ] `core` → 설정, 의존성 주입, 예외, 로거
- [ ] `infrastructure` → 외부 API 클라이언트, 캐시, 메시징
- [ ] OpenAPI 자동 노출 (FastAPI 기본, `skills/lang/api/openapi-conventions.md` 컨벤션 적용)
- [ ] `pyproject.toml`로 패키지 관리

## 표준 레이아웃

```text
app/
├── main.py                              ← FastAPI 앱 생성, router include
│
├── order/                               ← Bounded Context (단일 도메인이면 생략 가능)
│   ├── router.py                        ← APIRouter (prefix=/api/v1/orders, tags=[Order])
│   ├── service.py                       ← OrderService
│   ├── repository.py                    ← OrderRepository (SQLAlchemy)
│   ├── models.py                        ← Order ORM 엔티티
│   ├── schemas.py                       ← PlaceOrderRequest / OrderResponse (Pydantic)
│   └── exceptions.py
│
├── core/
│   ├── config.py                        ← Settings (env)
│   ├── database.py                      ← engine, SessionLocal, get_db()
│   ├── dependencies.py                  ← FastAPI Depends 헬퍼
│   ├── exceptions.py                    ← ErrorResponse, exception handlers
│   └── logging.py
│
└── infrastructure/
    ├── clients/
    │   └── payment_client.py
    ├── cache/
    └── messaging/

tests/
├── unit/order/
├── integration/order/
└── e2e/
```

## 의존 규칙

```text
router ──→ service ──→ repository ──→ models
                  │
                  ▼
          infrastructure.clients

core   →  설정·DB세션·DI wiring
```

- `router` → `service` 호출만. **`repository` 직접 호출 금지**.
- `service` → `repository`, `models`, `infrastructure.clients` 호출.
- `repository` → `models`만 다룸.
- `models` (도메인) → 외부 import 최소화. SQLAlchemy 어노테이션은 허용하되 FastAPI/Service 의존 금지.
- 순환 import 금지.

## 최소 템플릿

```python
# app/order/schemas.py
from pydantic import BaseModel

class PlaceOrderRequest(BaseModel):
    customer_id: int
    items: list[dict]

class OrderResponse(BaseModel):
    id: int
    status: str
    total: float
```

```python
# app/order/repository.py
from sqlalchemy.orm import Session
from .models import Order

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get(self, order_id: int) -> Order | None:
        return self.db.get(Order, order_id)
```

```python
# app/order/service.py
from .repository import OrderRepository
from .models import Order
from .schemas import PlaceOrderRequest
from app.infrastructure.clients.payment_client import PaymentClient

class OrderService:
    def __init__(self, repo: OrderRepository, payment: PaymentClient):
        self.repo = repo
        self.payment = payment

    def place(self, req: PlaceOrderRequest) -> Order:
        order = Order.create(req.customer_id, req.items)
        self.payment.authorize(order.total)
        return self.repo.save(order)
```

```python
# app/order/router.py
from fastapi import APIRouter, Depends
from .service import OrderService
from .schemas import PlaceOrderRequest, OrderResponse
from app.core.dependencies import get_order_service

router = APIRouter(prefix="/api/v1/orders", tags=["Order"])

@router.post("", response_model=OrderResponse, status_code=201)
def place_order(req: PlaceOrderRequest, svc: OrderService = Depends(get_order_service)):
    return OrderResponse.model_validate(svc.place(req))
```

## 금지
- **Router에서 Repository 직접 호출** — 항상 Service 경유.
- **ORM 모델을 응답으로 그대로 반환** — Pydantic 스키마로 매핑 (지연 로딩 사고/정보 노출 방지).
- **`schemas`와 `models`를 한 파일에 섞기** — 분리.
- **`global` repository 인스턴스** — DI(`Depends`) 사용.
- **비즈니스 로직을 Router에 작성** — Router는 매핑·검증·HTTP 코드만.
- **Repository에 비즈니스 메서드** (`find_active_with_discount()`) — 쿼리만, 판단은 Service.

## 변형 — 클린 아키텍처로 마이그레이션
도메인이 자라면(어댑터 3개 이상, 도메인 로직이 service에 몰림):
1. `models.py` → `domain/order/model.py`(순수) + `infrastructure/persistence/order_orm.py`(매핑) 분리
2. `repository.py` → 인터페이스(`domain/order/repository.py`, Protocol) + 구현(`infrastructure/repositories/order_repository.py`)
3. `service.py` → `application/services/order/place_order_service.py`
4. `router.py` → `presentation/api/order/order_router.py`
5. 자세히는 `skills/lang/python/clean-fastapi-layout.md`

## 도구
- 패키징: `uv` 또는 `poetry`
- 린트: `ruff`
- 타입: `mypy`
- 테스트: `pytest` + `httpx.AsyncClient`
