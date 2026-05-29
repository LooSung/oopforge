---
name: oop-factory-method
description: 복잡한 객체 생성을 캡슐화. 생성자 대신 의도를 표현하는 정적 팩토리 메서드 사용.
tags: [oop, ddd, creation]
stability: stable
---

# OOP — Factory Method

## 언제 쓰나
- 객체 생성 자체가 도메인 의미를 갖는 행위일 때 (`Order.place()`, `User.register()`)
- 생성 시 불변식(invariants) 검증이 필요할 때
- 여러 생성 경로가 있을 때 (`Order.placeFromCart()`, `Order.placeFromQuote()`)
- 생성 시 도메인 이벤트를 발행해야 할 때

## 체크리스트
- [ ] **public 생성자 금지** (private 또는 protected)
- [ ] 정적 팩토리 메서드 이름은 **도메인 동사**
- [ ] 메서드 안에서 불변식 검증
- [ ] 필요하면 생성과 동시에 이벤트 발행
- [ ] 반환 타입은 자기 자신 (`Order`)
- [ ] null 대신 예외 (생성 실패는 예외적 상황)

## 템플릿 (의사 코드)

```text
class Order:
    private id: OrderId
    private customerId: CustomerId
    private lines: List<OrderLine>
    private status: OrderStatus
    private events: List<DomainEvent>

    private constructor(id, customerId, lines, status):
        this.id = id
        ...

    // 의도가 다른 여러 팩토리 메서드
    static place(customerId, lines) -> Order:
        if lines.isEmpty(): raise InvalidOrder("at least 1 line")
        if lines.size() > 100: raise InvalidOrder("too many lines")
        id = OrderId.next()
        order = Order(id, customerId, lines, PENDING)
        order.events.add(OrderPlaced(...))
        return order

    static placeFromCart(cart: Cart) -> Order:
        return place(cart.customerId, cart.toOrderLines())

    static reconstitute(id, customerId, lines, status) -> Order:
        // 영속화에서 복원할 때 (이벤트 발행 X)
        return Order(id, customerId, lines, status)
```

## Reconstitute 패턴 (영속화 복원용)

- 일반 팩토리: 도메인 행위 → 이벤트 발행
- `reconstitute`: DB에서 복원 → 이벤트 발행 X
- 두 경로를 분리해야 영속화 복원 시 이벤트 중복 발행 안 됨

## 변형
- **Factory 클래스 분리**: 생성 로직이 복잡하거나 외부 의존성 필요할 때 (`OrderFactory` 별도 클래스)
- **Builder**: 인자가 너무 많을 때 (5개 이상)
- **Abstract Factory**: 변형이 여럿일 때 (`StandardOrderFactory`, `SubscriptionOrderFactory`)

## 금지
- **public 생성자 노출** — 우회 생성 가능해지면 불변식 깨짐
- **`new` 생성 후 setter로 초기화** — 일시적으로 유효하지 않은 상태 존재
- **getter 이름 같은 팩토리** — `getInstance()` 같은 모호한 이름 (싱글톤 의도 외엔 X)
- **너무 일반적인 이름** — `create()`, `build()` (의도 안 보임). `place`, `register`, `issue` 같은 도메인 동사로.
- **팩토리 안에서 영속화** — 팩토리는 생성만, 저장은 repository

## 자바 / 파이썬 표기

**Java:**
```java
public static Order place(CustomerId customerId, List<OrderLine> lines) {
    // ...
}
```

**Python (Pydantic):**
```python
class Order(BaseModel):
    model_config = ConfigDict(frozen=False)  # 도메인 객체는 메서드로 변경

    @classmethod
    def place(cls, customer_id: CustomerId, lines: list[OrderLine]) -> "Order":
        if not lines:
            raise InvalidOrder("at least 1 line")
        ...
```

## 참고
- "객체가 생성되는 순간 항상 유효해야 한다" — 이게 팩토리의 존재 이유
- Effective Java Item 1: "Consider static factory methods instead of constructors"
