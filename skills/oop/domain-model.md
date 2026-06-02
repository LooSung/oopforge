---
name: oop-domain-model
description: Aggregate, Value Object, Domain Event를 한 경계 안에서 설계하는 핵심 도메인 모델 규칙.
tags: [oop, ddd, domain-model]
stability: stable
---

# OOP — Domain Model

## 언제 쓰나

도메인 객체의 책임, 상태 변경, 불변식, 이벤트를 정할 때 사용한다.
Forge의 OOP Contract에서 Aggregate Root, Domain Invariants, State Transition을 채울 때 먼저 읽는다.

## Aggregate Root

- [ ] 한 트랜잭션에서 일관성을 지킬 경계를 하나 정한다.
- [ ] 외부 접근은 Aggregate Root를 통해서만 허용한다.
- [ ] 생성은 의도를 드러내는 factory method로 한다. 예: `Order.place(...)`, `User.register(...)`.
- [ ] 생성과 상태 변경 시 불변식을 검증한다.
- [ ] public setter를 만들지 않는다.
- [ ] 내부 컬렉션은 복사본이나 불변 view로 노출한다.
- [ ] 다른 Aggregate는 객체가 아니라 ID로 참조한다.

## Value Object

- [ ] 식별자가 없고 값으로 동등성이 결정되는 개념만 Value Object로 만든다.
- [ ] 생성 시 유효성을 검증한다.
- [ ] 변경이 필요하면 기존 객체를 바꾸지 말고 새 인스턴스를 반환한다.
- [ ] 원시값 남발을 줄인다. 예: `String email` 대신 `Email`.
- [ ] API DTO나 ORM entity를 도메인 Value Object로 공유하지 않는다.

## Domain Event

- [ ] 도메인에서 이미 발생한 의미 있는 사실만 Event로 만든다.
- [ ] 이름은 과거형으로 짓는다. 예: `OrderPlaced`, `PaymentApproved`.
- [ ] Aggregate ID와 발생 시각을 포함한다.
- [ ] 페이로드는 필요한 최소 정보만 담는다.
- [ ] Aggregate 내부에 기록하고 application service가 저장 후 회수해 발행한다.
- [ ] 외부 메시지 발송은 domain이 아니라 adapter 또는 infrastructure가 맡는다.

## 판단 기준

| 질문 | 선택 |
|---|---|
| 상태 변경 규칙이 있는가? | Aggregate 행동 메서드 |
| 식별자 없이 값 자체가 의미인가? | Value Object |
| 다른 경계가 알아야 하는 사실인가? | Domain Event |
| 단순 생성자가 불변식을 우회하는가? | Factory method |

## 금지

- 비즈니스 규칙을 controller, router, application service private method에 숨기지 않는다.
- 도메인 객체에 Spring, JPA, FastAPI, SQLAlchemy, HTTP 타입을 넣지 않는다.
- `create`, `update`, `delete` 같은 CRUD 이름으로 도메인 행동을 흐리지 않는다.
- 여러 Aggregate를 한 트랜잭션에서 함께 수정하지 않는다.
