---
name: oop-domain-event
description: 도메인에서 의미 있는 일이 발생했음을 표현하는 이벤트. 애그리거트 간 동기화의 표준 수단.
tags: [oop, ddd, event]
stability: stable
---

# OOP — Domain Event

## 언제 쓰나
- 한 애그리거트의 상태 변경을 **다른 애그리거트/컨텍스트가 알아야 할 때**
- "주문이 확정되면 재고를 줄인다" 같은 부수 효과를 일관성 있게 처리할 때
- 트랜잭션 안에서 여러 애그리거트를 동시에 바꾸지 않으려 할 때

## 체크리스트
- [ ] 이름은 **과거형 동사** (`OrderPlaced`, `PaymentApproved`)
- [ ] 불변 (생성 후 변경 불가)
- [ ] 발생 시각(`occurredAt`) 포함
- [ ] 식별자 포함 (어느 애그리거트인가)
- [ ] 페이로드는 필요한 최소만
- [ ] 도메인 모델 안에서 발행, 외부 발송은 인프라가 담당
- [ ] 직렬화 가능 (메시지 큐로 보낼 수 있어야)

## 템플릿 (의사 코드)

```text
abstract class DomainEvent:
    occurredAt: Instant
    eventId: UUID

class OrderPlaced(DomainEvent):
    orderId: OrderId
    customerId: CustomerId
    total: Money

// 애그리거트 안에서 발행
class Order:
    private events: List<DomainEvent> = []

    static place(...) -> Order:
        order = Order(...)
        order.record(OrderPlaced(orderId=order.id, ...))
        return order

    record(event: DomainEvent):
        events.add(event)

    popEvents() -> List<DomainEvent>:
        out = copy(events)
        events.clear()
        return out

// Application service가 발행
class PlaceOrder:
    execute(cmd):
        order = Order.place(...)
        orderRepository.save(order)
        eventPublisher.publishAll(order.popEvents())  // 트랜잭션 커밋 후
```

## 변형
- **Transactional Outbox**: 같은 트랜잭션에 이벤트도 DB에 저장 → 별도 프로세스가 발송. 메시지 유실 방지.
- **Eventual Consistency**: 수신측은 비동기로 처리, 일시적 불일치 허용.
- **이벤트 소싱**: 상태가 아니라 이벤트들의 합으로 애그리거트 재구성.

## 금지
- **현재형 이름** — `PlaceOrder` (X), `OrderPlaced` (O). 명령은 Command, 사실은 Event.
- **mutable 필드** — 이미 발생한 사실은 바뀌지 않음.
- **트랜잭션 안에서 외부 발송** — 롤백 시 이벤트만 나가버림. outbox 또는 commit hook.
- **거대한 페이로드** — 전체 애그리거트 통째로 X. ID + 필요 필드만.
- **여러 책임 섞기** — `OrderChanged` 같은 모호한 이벤트 X. `OrderConfirmed`, `OrderCancelled` 처럼 의미 분리.

## 참고
- 한 트랜잭션 = 한 애그리거트 변경 + 이벤트 발행
- 이벤트는 도메인 언어로 (기술 용어 X)
