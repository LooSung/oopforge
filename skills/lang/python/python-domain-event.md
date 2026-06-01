---
name: python-domain-event
description: Python에서 도메인 이벤트를 정의·수집·발행하는 표준 패턴.
tags: [python, ddd, event]
stability: stable
---

# Python — Domain Event

## 언제 쓰나
Aggregate에서 발생한 사실(`OrderPlaced`, `PaymentAuthorized`)을 다른 컨텍스트나 비동기 핸들러로 전달할 때.
`skills/oop/domain-event.md`의 언어 무관 규칙을 먼저 읽고 이 스킬로 구체화한다.

## 기준
- 이벤트는 **불변(frozen)**, **과거형 이름**, **순수 데이터**
- Aggregate가 내부 리스트에 기록 → Application Service가 회수 → 디스패처가 발행
- 트랜잭션 커밋 후 발행이 기본 (Outbox 또는 SQLAlchemy `after_commit`)

## 체크리스트
- [ ] 이벤트 클래스는 `@dataclass(frozen=True)` 또는 Pydantic `frozen=True`
- [ ] 이름은 과거형 (`OrderPlaced`, `PaymentRefunded`)
- [ ] 필드는 원시 타입 + Value Object만, Aggregate 참조는 ID로
- [ ] `occurred_at: datetime` 포함
- [ ] Aggregate는 `_events` 리스트에 append, `pull_events()`로 회수
- [ ] Application Service가 Repository 저장 후 `pull_events()` → 디스패처로 전달
- [ ] 핸들러는 멱등(idempotent) — 같은 이벤트가 두 번 와도 안전

## 이벤트 정의

```python
# domain/order/event.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from .value import OrderId, CustomerId

@dataclass(frozen=True)
class OrderPlaced:
    order_id: OrderId
    customer_id: CustomerId
    total: int
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class OrderCancelled:
    order_id: OrderId
    reason: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

## 디스패처 (간단 인메모리)

```python
# shared/event_bus.py
from collections import defaultdict
from typing import Callable, Type, Any

class EventBus:
    def __init__(self):
        self._handlers: dict[Type, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type, handler: Callable[[Any], None]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: Any) -> None:
        for handler in self._handlers[type(event)]:
            handler(event)

bus = EventBus()
```

## Application Service에서 회수·발행

```python
# application/services/order/place_order_service.py
from app.shared.event_bus import bus
from app.domain.order.repository import OrderRepository

class PlaceOrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, cmd) -> "OrderId":
        order = Order.create(cmd.id, cmd.customer_id, cmd.lines)
        self.repo.save(order)
        for event in order.pull_events():
            bus.publish(event)        # 트랜잭션 커밋 후가 이상적
        return order.id
```

## 트랜잭션 커밋 후 발행 (Outbox 권장)

```python
# infrastructure/messaging/outbox.py
# 1) save(order) 와 같은 트랜잭션에서 events를 outbox 테이블에 INSERT
# 2) 별도 워커가 outbox를 읽어 메시지 큐로 발행 + 발행된 행 표시
# 3) 핸들러는 멱등 처리 (event_id 기반)
```

가장 단순한 형태: SQLAlchemy `event.listens_for(session, "after_commit")` 훅에서 발행. 단일 인스턴스/단일 DB일 때 충분.

## 핸들러 예

```python
# application/handlers/notification_handler.py
def send_order_confirmation(event: OrderPlaced) -> None:
    # 이미 보낸 적 있으면 무시 (멱등)
    if notifications.exists(event_id=hash((event.order_id, event.occurred_at))):
        return
    email.send(to=customer_email(event.customer_id), template="order_placed", data=event)

bus.subscribe(OrderPlaced, send_order_confirmation)
```

## 금지
- **이벤트에 Aggregate 객체 참조 저장** — 항상 ID + 원시 데이터.
- **현재형 이름** (`PlaceOrder`) — 명령(Command)과 혼동됨. 과거형 (`OrderPlaced`).
- **mutable 이벤트** — `frozen=True`. 발행 후 변형되면 디버깅 지옥.
- **트랜잭션 커밋 전 발행** — 롤백 시 유령 이벤트. 커밋 후 또는 outbox.
- **동기 핸들러에서 외부 API 호출 후 전체 트랜잭션 롤백** — 핸들러 실패가 원래 유스케이스를 깨면 안 됨.
- **이벤트 페이로드에 인증/암호화된 비밀** — 로그·큐로 새어 나감.

## 변형
- **다중 인스턴스**: 인메모리 `EventBus` 대신 Kafka/Redis Streams/SQS.
- **동기 vs 비동기**: 같은 트랜잭션 내 부수 효과는 명령(Command)로, 다른 컨텍스트 알림은 이벤트.
- **Pydantic 사용 시**: `class OrderPlaced(BaseModel): model_config = {"frozen": True}`
