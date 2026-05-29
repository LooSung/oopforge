---
name: oop-application-service
description: 유스케이스 한 개를 오케스트레이션하는 애플리케이션 서비스. 도메인 로직은 도메인에, 조정만 여기서.
tags: [oop, ddd, application]
stability: stable
---

# OOP — Application Service (Use Case)

## 언제 쓰나
**한 유스케이스 = 한 클래스 (또는 한 메서드)**.
도메인 로직을 호출하고, 트랜잭션 경계를 관리하고, 포트와 어댑터를 연결한다.

## 체크리스트
- [ ] 한 클래스는 한 유스케이스 (Single Responsibility)
- [ ] 메서드 이름은 유스케이스 동사 (`execute`, `place`, `cancel`)
- [ ] 도메인 로직을 여기에 두지 않음 (도메인 모델로 위임)
- [ ] 트랜잭션 경계 명시
- [ ] 외부 의존성은 포트(인터페이스)로 주입
- [ ] 입력은 Command 객체, 출력은 Result 객체 (또는 ID)
- [ ] 도메인 이벤트 발행 처리

## 템플릿 (의사 코드)

```text
class PlaceOrder:                          # Use case
    orderRepository: OrderRepository       # outbound port
    paymentGateway: PaymentGateway         # outbound port
    eventPublisher: EventPublisher

    constructor(orderRepository, paymentGateway, eventPublisher):
        ...

    @Transactional
    execute(command: PlaceOrderCommand) -> OrderId:
        // 1. 도메인 객체 생성 (도메인 로직)
        order = Order.place(
            id = OrderId.next(),
            customerId = command.customerId,
            lines = command.lines
        )

        // 2. 외부 호출 (필요시)
        paymentResult = paymentGateway.charge(order.id, order.total)
        if not paymentResult.success:
            raise PaymentFailed

        // 3. 영속화
        orderRepository.save(order)

        // 4. 이벤트 발행
        eventPublisher.publishAll(order.popEvents())

        return order.id
```

## Command / Result 객체

```text
class PlaceOrderCommand:                   # 불변
    customerId: CustomerId
    lines: List<OrderLineCommand>

class OrderLineCommand:
    productId: ProductId
    quantity: int
```

## 금지
- **도메인 로직 작성 금지** — `if order.status == ...` 같은 비즈니스 규칙은 도메인 모델 안으로
- **여러 유스케이스를 한 클래스에** — `OrderService` 안에 place/cancel/ship 다 넣지 말 것
- **트랜잭션 안에서 여러 애그리거트 변경** — 다른 애그리거트는 이벤트로 동기화
- **infrastructure 직접 사용** — `JpaOrderRepository` 직접 import 금지. `OrderRepository` 포트만.
- **return void 남발** — 가능하면 ID나 결과 객체 반환 (테스트 편함)

## 변형
- **CQRS 분리**: Command 핸들러와 Query 핸들러 분리
- **Functional**: 클래스 대신 함수 하나로 표현 (작은 유스케이스)
