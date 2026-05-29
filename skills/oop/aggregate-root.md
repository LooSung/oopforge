---
name: oop-aggregate-root
description: DDD 애그리거트 루트를 설계할 때. 일관성 경계가 필요한 엔티티 클러스터의 진입점.
tags: [oop, ddd, aggregate]
stability: stable
---

# OOP — Aggregate Root

## 언제 쓰나
여러 엔티티/값객체가 함께 변하며 **하나의 일관성 경계**로 다뤄져야 할 때.
외부에서는 루트를 통해서만 내부에 접근한다.

## 체크리스트
- [ ] 식별자(ID)는 값 객체로 별도 정의 (`OrderId`, not `Long`)
- [ ] 생성자는 private/protected, 정적 팩토리 메서드 사용 (`Order.place(...)`)
- [ ] 상태 변경은 메서드를 통해서만 (public setter 금지)
- [ ] 내부 컬렉션은 방어적 복사 또는 불변 뷰로 노출
- [ ] equals/hashCode는 식별자만 사용
- [ ] 불변식(invariant)은 메서드 안에서 검증
- [ ] 도메인 이벤트 발행 고려
- [ ] 다른 애그리거트는 ID로만 참조 (객체 참조 X)

## 템플릿 (의사 코드)

```text
class Order:                          # Aggregate Root
    id: OrderId                       # Value Object
    status: OrderStatus
    lines: List<OrderLine>            # 내부 엔티티/값객체
    customerId: CustomerId            # 다른 애그리거트는 ID로만

    private constructor(...)

    static place(id, customerId, lines) -> Order:
        if lines.isEmpty(): raise InvalidOrder
        order = Order(id, customerId, lines, status=PENDING)
        order.record(OrderPlaced(...))
        return order

    cancel(reason: String):
        if status == SHIPPED: raise IllegalState
        status = CANCELLED
        record(OrderCancelled(id, reason))

    addLine(line):
        if status != PENDING: raise IllegalState
        lines = lines + [line]        # 방어적

    lines() -> List<OrderLine>:
        return immutableCopy(lines)
```

## 변형
- **단일 엔티티 애그리거트**: 루트 외 다른 엔티티가 없어도 됨. 단순한 게 가장 좋다.
- **이벤트 소싱**: 메서드가 상태 변경 대신 이벤트만 발행.
- **버전 필드**: 낙관적 락이 필요하면 `version` 필드 추가.

## 금지
- **public setter** — 캡슐화 깨짐의 시작
- **빈 생성자** — JPA가 강제하면 `protected`로 제한
- **컬렉션 직접 노출** — `return this.lines` 금지. 복사 또는 unmodifiable.
- **다른 애그리거트 객체 참조** — `Customer customer` 대신 `CustomerId customerId`
- **CRUD 메서드명** — `update()` 금지, 의도를 표현하는 동사 (`cancel`, `confirm`, `place`)
- **트랜잭션 안에서 여러 애그리거트 동시 변경** — 일관성 경계 위반

## 참고
- 한 트랜잭션 = 한 애그리거트 변경 (원칙)
- 애그리거트 간 동기화는 도메인 이벤트로
