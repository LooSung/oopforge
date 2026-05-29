---
name: workflow-design
description: Discovery 다음 단계. 유스케이스 시그니처와 애그리거트 구조를 그린다. 구현은 아직 X.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Design

## 언제 쓰나
Discovery가 끝났을 때. Skeleton 이전.
**시그니처만** 그리고 구현은 절대 하지 않는 단계.

## 체크리스트
- [ ] 각 바운디드 컨텍스트별 유스케이스 나열 (동사형 이름)
- [ ] 각 유스케이스의 입력/출력 시그니처 정의
- [ ] 애그리거트별 불변식(invariants) 명시
- [ ] 도메인 이벤트 후보 정의
- [ ] 리포지토리 포트 시그니처 정의
- [ ] 외부 의존성을 포트(인터페이스)로 추상화

## 산출물

`docs/design.md` 에 저장:

```markdown
# <Domain> — Design

## Use Cases (Ordering)
- `placeOrder(customerId, lines): OrderId`
- `cancelOrder(orderId, reason): void`
- `confirmPayment(orderId, paymentId): void`

## Aggregates

### Order (root)
- Identity: `OrderId`
- State: `status`, `lines`, `customerId`
- Invariants:
  - lines는 비어있을 수 없음
  - SHIPPED 상태에서 cancel 불가
  - 총 금액 = sum(line amounts)
- Methods (시그니처만):
  - `place(...)`, `cancel(reason)`, `confirm()`

## Domain Events
- `OrderPlaced(orderId, customerId, total)`
- `OrderCancelled(orderId, reason)`
- `OrderConfirmed(orderId)`

## Ports (인터페이스만)
- `OrderRepository.findById(id): Order?`
- `OrderRepository.save(order): void`
- `PaymentGateway.charge(orderId, amount): PaymentResult`
```

## 금지
- **구현 코드 금지** — 메서드 본문 작성 X. 시그니처만.
- **프레임워크 의존 금지** — `@Service`, `@Entity` 등장 X.
- **DTO 설계 금지** — 이건 Skeleton/Implement 단계.
- **무한 추상화 금지** — 인터페이스 1단계까지. Adapter 패턴 X.

## 다음 단계
사용자 승인 후 → `workflow-skeleton`
