---
name: oop-use-case-boundary
description: Application service와 Repository port의 책임 경계를 정해 얇은 유스케이스를 유지한다.
tags: [oop, ddd, application, port]
stability: stable
---

# OOP — Use Case Boundary

## 언제 쓰나

유스케이스를 구현하거나 외부 의존성을 연결할 때 사용한다.
Craft의 OOP Contract에서 Use Case, Required Ports, Transaction Boundary를 채울 때 먼저 읽는다.

## Application Service

- [ ] 한 유스케이스를 한 클래스 또는 한 메서드로 표현한다.
- [ ] 메서드 이름은 비즈니스 동사로 둔다. 예: `placeOrder`, `cancelOrder`, `approvePayment`.
- [ ] 도메인 객체를 로드하거나 생성하고, 도메인 행동 메서드를 호출한다.
- [ ] 트랜잭션 경계를 명시한다.
- [ ] 외부 의존성은 port 인터페이스로 주입한다.
- [ ] 입력은 command/request DTO로 받고, 출력은 ID 또는 result로 반환한다.
- [ ] 도메인 이벤트는 Aggregate에서 회수해 발행한다.

## Repository Port

- [ ] Aggregate 단위로 port를 정의한다.
- [ ] 필요한 메서드만 둔다. CRUD 세트를 기계적으로 만들지 않는다.
- [ ] 도메인 언어로 쿼리 의도를 드러낸다. 예: `findActiveByCustomer`, `findOverdueOrders`.
- [ ] domain 객체와 domain ID를 입출력으로 사용한다.
- [ ] JPA, SQLAlchemy, Pageable, HTTP DTO 같은 framework 타입을 노출하지 않는다.
- [ ] 구현체와 mapper는 infrastructure 또는 adapter에 둔다.

## 흐름

```text
Inbound adapter
  -> Application service
  -> Aggregate behavior
  -> Repository port
  -> Outbound adapter
```

## 금지

- application service에 상태 전이 조건문을 쌓지 않는다.
- `OrderService` 하나에 place/cancel/ship/refund를 모두 넣지 않는다.
- controller/router가 repository를 직접 호출하지 않는다.
- repository가 트랜잭션 시작/종료나 외부 API 호출까지 맡지 않는다.
- port 인터페이스에 persistence 모델이나 API DTO를 노출하지 않는다.
