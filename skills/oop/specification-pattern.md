---
name: oop-specification-pattern
description: 비즈니스 규칙을 객체로 캡슐화. if-else 산발을 막고 조합 가능한 규칙으로.
tags: [oop, ddd, business-rule]
stability: stable
---

# OOP — Specification Pattern

## 언제 쓰나
- 같은 비즈니스 규칙이 여러 곳에서 if-else 로 중복될 때
- 규칙들을 AND/OR 로 조합해야 할 때
- 규칙이 변경 자주 일어나고 테스트가 필요할 때
- 조회 기준과 검증 기준이 같을 때 (Repository 쿼리 + 도메인 검증)

## 체크리스트
- [ ] 한 Specification = 한 규칙 (Single Responsibility)
- [ ] `isSatisfiedBy(candidate): bool` 메서드 하나만 노출
- [ ] AND/OR/NOT 조합 메서드 제공
- [ ] 규칙은 **도메인 언어**로 이름짓기 (`CustomerIsVip`, `OrderIsCancellable`)
- [ ] 부수효과 없음 (순수 함수처럼)
- [ ] 단위 테스트 쉬워야

## 템플릿 (의사 코드)

```text
interface Specification<T>:
    isSatisfiedBy(candidate: T) -> bool

    and(other: Specification<T>) -> Specification<T>:
        return AndSpec(this, other)

    or(other: Specification<T>) -> Specification<T>:
        return OrSpec(this, other)

    not() -> Specification<T>:
        return NotSpec(this)

// 도메인 규칙
class CustomerIsVip implements Specification<Customer>:
    isSatisfiedBy(customer: Customer) -> bool:
        return customer.totalSpent.greaterThan(Money(10000, USD))

class OrderIsRecent implements Specification<Order>:
    threshold: Duration

    isSatisfiedBy(order: Order) -> bool:
        return order.placedAt.isAfter(now() - threshold)

class OrderQualifiesForDiscount implements Specification<Order>:
    isSatisfiedBy(order: Order) -> bool:
        return CustomerIsVip().isSatisfiedBy(order.customer())
           and OrderIsRecent(Duration.ofDays(30)).isSatisfiedBy(order)
           and not OrderHasReturns().isSatisfiedBy(order)

// 사용 — Application Service
class ApplyDiscount:
    execute(orderId):
        order = orderRepository.findById(orderId)
        if OrderQualifiesForDiscount().isSatisfiedBy(order):
            order.applyDiscount()
        orderRepository.save(order)
```

## Repository 쿼리와 결합

같은 Specification을 쿼리에도 쓸 수 있다 (DB 표현 가능한 경우):

```text
class OrderRepository:
    findMatching(spec: Specification<Order>) -> List<Order>

// 사용
recent = OrderIsRecent(Duration.ofDays(7))
vip = OrderByVipCustomer()
results = orderRepository.findMatching(recent.and(vip))
```

JPA Specification, MyBatis 의 dynamic SQL, SQLAlchemy 의 filter() 등으로 매핑.

## 변형
- **Hard-coded composition**: 매번 새 Spec 클래스 만들지 않고 함수형으로 조합 (Java 8+ Predicate, Python 람다)
- **Validation Spec**: 통과/실패뿐 아니라 **실패 이유**도 반환 (`Result<Valid, Reason>`)
- **Async Spec**: 외부 시스템 조회가 필요한 규칙 (Customer credit check 등)

## 금지
- **거대한 단일 Spec** — 한 클래스 안에 if-else 잔뜩. SRP 위반.
- **상태를 가진 Spec** — 호출할 때마다 결과가 달라지면 안 됨 (테스트 불가능)
- **side effect** — `isSatisfiedBy` 안에서 DB 변경, 외부 호출 X
- **억지 적용** — 단순한 한 줄 검증은 그냥 메서드로 (`order.canCancel()`). Spec은 조합/재사용 가치 있을 때만.

## 자바 함수형 대안 (Java 8+)

```java
Predicate<Order> isRecent = order -> order.placedAt().isAfter(Instant.now().minus(7, DAYS));
Predicate<Order> isVip = order -> order.customer().totalSpent().compareTo(THRESHOLD) > 0;
Predicate<Order> qualifies = isRecent.and(isVip);
```

도메인 객체에 의미를 부여하고 싶으면 클래스로, 즉석 조합이면 Predicate로.

## 참고
- Eric Evans 가 DDD 책에서 정식화한 패턴
- 비즈니스 룰의 "테스트 가능성" 이 가장 큰 가치
