---
name: workflow-discovery
description: 새 도메인/기능 시작 시 가장 먼저 수행하는 단계. 코드 없이 도메인 언어와 경계만 정의한다.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Discovery

## 언제 쓰나
새 도메인을 모델링하거나, 큰 기능을 시작할 때. **첫 번째** 단계.
Design 이전에 반드시 수행. 건너뛰면 잘못된 추상화로 직행한다.

## 체크리스트
- [ ] 도메인 용어집(ubiquitous language) 정의
- [ ] 바운디드 컨텍스트 식별 (여러 개일 수 있음)
- [ ] 컨텍스트별 핵심 애그리거트 후보 나열
- [ ] 외부 시스템/액터 식별
- [ ] 비기능 요구사항 (성능, 일관성 모델) 한 줄씩
- [ ] 모르는 것을 명시적으로 적기 (Open Questions)

## 산출물

`docs/discovery.md` 에 다음 형식으로 저장:

```markdown
# <Domain> — Discovery

## Glossary
- **Order**: 고객이 제출한 구매 의사. 결제 전까지 변경 가능.
- **OrderLine**: Order 안의 단일 품목 + 수량.
- ...

## Bounded Contexts
1. **Ordering** — Order, OrderLine, Customer
2. **Payment** — Payment, Refund
3. **Fulfillment** — Shipment, Inventory

## Aggregate Candidates
- Ordering: `Order` (root), `OrderLine` (entity in aggregate)
- Payment: `Payment` (root)

## Actors / External
- Customer (web), AdminUser (back office)
- Payment Gateway (외부), Inventory Service (내부)

## Non-Functional
- 결제는 동기, 발송은 eventual consistency
- Order 생성은 99p 200ms 이내

## Open Questions
- 부분 환불 정책?
- 재고 부족 시 대기열 운영 여부?
```

## 금지
- **코드 작성 금지** — 시그니처도 X. 단어와 문장만.
- **프레임워크 언급 금지** — Spring/FastAPI/JPA는 아직 등장 X.
- **CRUD 사고 금지** — "Order를 update한다" 대신 "주문을 확정한다", "주문을 취소한다".
- **Open Questions 비우기** — 모르는 게 없을 리 없다. 명시하라.

## 다음 단계
사용자 승인 후 → `workflow-design`
