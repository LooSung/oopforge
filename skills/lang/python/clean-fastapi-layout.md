---
name: python-clean-fastapi-layout
description: FastAPI 프로젝트의 클린/헥사고날 패키지 구조와 의존 규칙.
tags: [python, fastapi, hexagonal, layout]
stability: stable
---

# Python — Clean FastAPI Layout

## 언제 쓰나
FastAPI 기반 새 서비스/모듈을 시작할 때. 모든 OOPforge Python 프로젝트의 기본 레이아웃.

## 체크리스트
- [ ] 4개 레이어: domain, application, infrastructure, interfaces
- [ ] domain 레이어는 FastAPI/SQLAlchemy import 0
- [ ] 의존성 주입은 FastAPI `Depends` 또는 직접 생성자 주입
- [ ] API 요청/응답 모델 ≠ 도메인 값 객체
- [ ] `pyproject.toml` 로 패키지 관리
- [ ] 모듈별 분리 (`src/order/`, `src/payment/`)

## 표준 레이아웃

```
src/order/
├── __init__.py
├── main.py                              ← FastAPI app 생성
│
├── domain/                              ← 프레임워크 import 금지
│   ├── __init__.py
│   ├── model.py                         ← Order, OrderLine 등
│   ├── value.py                         ← Money, OrderId, ...
│   ├── event.py                         ← OrderPlaced 등
│   └── port.py                          ← OrderRepository, PaymentGateway 인터페이스 (Protocol)
│
├── application/                         ← 유스케이스
│   ├── __init__.py
│   ├── command.py                       ← Command 객체
│   └── usecase/
│       ├── place_order.py
│       └── cancel_order.py
│
├── infrastructure/                      ← outbound 어댑터
│   ├── __init__.py
│   ├── persistence/
│   │   ├── models.py                    ← SQLAlchemy ORM
│   │   ├── repository.py                ← OrderRepository 구현
│   │   └── mapper.py
│   ├── external/
│   │   └── payment_gateway.py
│   └── config.py
│
└── interfaces/                          ← inbound (REST)
    ├── __init__.py
    └── rest/
        ├── router.py                    ← APIRouter
        ├── request.py                   ← Pydantic request models
        └── response.py                  ← Pydantic response models
```

## 포트 인터페이스 (Protocol)

```python
# domain/port.py
from typing import Protocol, Optional
from .model import Order
from .value import OrderId

class OrderRepository(Protocol):
    def find_by_id(self, id: OrderId) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...

class PaymentGateway(Protocol):
    def charge(self, order_id: OrderId, amount: "Money") -> "PaymentResult": ...
```

## 의존성 주입 (FastAPI)

```python
# interfaces/rest/router.py
from fastapi import APIRouter, Depends
from ...application.usecase.place_order import PlaceOrder
from ...infrastructure.persistence.repository import SqlOrderRepository

router = APIRouter()

def get_place_order() -> PlaceOrder:
    return PlaceOrder(
        order_repository=SqlOrderRepository(...),
        payment_gateway=...,
    )

@router.post("/orders")
def place_order(
    req: PlaceOrderRequest,
    use_case: PlaceOrder = Depends(get_place_order),
):
    order_id = use_case.execute(req.to_command())
    return {"order_id": order_id.value}
```

## 의존 규칙

```
interfaces ──────┐
                 ▼
application ──→ domain ←── infrastructure
                 ▲
                 │
       (domain은 어떤 레이어도 import하지 않음)
```

검증: import-linter 또는 간단한 grep 스크립트로 강제.

## 금지
- **domain 모듈에서 `from fastapi import`, `from sqlalchemy import`** — 절대.
- **API request 모델을 도메인 객체로 직접 사용** — 항상 매핑.
- **`global` 변수로 repository 보유** — DI 컨테이너 또는 FastAPI Depends 사용.
- **유스케이스 안에서 `requests.get(...)` 직접 호출** — 항상 port 경유.
- **순환 import** — 모듈 분리 신호.

## 변형
- **CQRS**: `application/query/` 별도 분리
- **비동기**: `async def` 유스케이스, async port
- **모노리스 → 마이크로서비스**: `src/order/`, `src/payment/` 를 각각 별 서비스로 분리해도 구조 동일

## 도구 추천
- 패키징: `uv` 또는 `poetry`
- 린트: `ruff`
- 타입: `mypy --strict`
- 의존 규칙 강제: `import-linter`
