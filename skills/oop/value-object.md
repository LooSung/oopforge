---
name: oop-value-object
description: 값 객체를 정의할 때. 식별자가 없고 속성으로 동등성이 결정되는 불변 객체.
tags: [oop, ddd, value-object]
stability: stable
---

# OOP — Value Object

## 언제 쓰나
- 식별자 없이 값으로 정의되는 개념 (Money, Email, Address, OrderId)
- 두 인스턴스의 모든 속성이 같으면 같은 것으로 간주
- 변경 불가능해야 의미가 있는 도메인 개념

## 체크리스트
- [ ] 모든 필드 final/immutable
- [ ] 생성 시 유효성 검증 (생성자/팩토리 메서드)
- [ ] equals/hashCode는 모든 의미있는 필드 사용
- [ ] 변경이 필요하면 새 인스턴스 반환 (`withAmount(...)`)
- [ ] setter 없음
- [ ] toString 의미있게 (디버깅용)
- [ ] 원시값 래핑 (Primitive Obsession 회피)

## 템플릿 (의사 코드)

```text
class Money:
    amount: Decimal
    currency: Currency

    constructor(amount, currency):
        if amount < 0: raise InvalidAmount
        if currency is null: raise InvalidCurrency
        this.amount = amount
        this.currency = currency

    add(other: Money) -> Money:
        if other.currency != currency: raise CurrencyMismatch
        return Money(amount + other.amount, currency)

    multiply(factor: Decimal) -> Money:
        return Money(amount * factor, currency)

    equals(other) -> bool:
        return amount == other.amount and currency == other.currency

class OrderId:                          # ID도 값 객체로
    value: UUID
    constructor(value):
        if value is null: raise Invalid
```

## 변형
- **단일 값 래퍼** (`OrderId`, `Email`) — 가장 흔함
- **복합 값 객체** (`Address`, `DateRange`) — 여러 필드
- **계산 가능한 값** (`Money`) — 연산 메서드 포함

## 금지
- **mutable 필드** — 값 객체의 정의 위배
- **setter** — 절대 금지
- **유효성 검증 없는 생성자** — `Email("not-an-email")` 통과되면 안 됨
- **식별자 추가** — 식별자가 필요하면 그건 엔티티
- **너무 많은 필드** — 7개 넘으면 분할 고민
- **JPA `@Entity` 어노테이션** — `@Embeddable` 사용

## 참고
- "Tiny Types" 패턴: `String email` 대신 `Email email`
- 도메인 표현력을 가장 빠르게 높이는 도구
