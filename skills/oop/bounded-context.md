---
name: oop-bounded-context
description: 도메인 모델의 적용 범위 경계. 같은 단어가 다른 의미를 가질 때, 또는 모델이 너무 커질 때 분할.
tags: [oop, ddd, strategic-design]
stability: stable
---

# OOP — Bounded Context

## 언제 쓰나
- "Customer" 가 Ordering에선 구매자, Billing에선 결제자, Marketing에선 잠재 고객처럼 **같은 단어가 컨텍스트마다 다른 의미** 일 때
- 한 모델이 너무 커져서 일관성 유지가 어려울 때
- 팀이 분리되어 독립적으로 변경하고 싶을 때

## 체크리스트
- [ ] 각 컨텍스트는 **독립적인 용어집**을 가진다
- [ ] 컨텍스트 간 모델 공유 금지 (같은 클래스 import X)
- [ ] 컨텍스트 경계 = 패키지 경계 (또는 모듈/서비스 경계)
- [ ] 다른 컨텍스트의 객체를 가져올 땐 **번역(translation)** 한다
- [ ] 컨텍스트 간 관계를 명시 (Partnership, Customer-Supplier, Conformist, ACL 등)
- [ ] Context Map 문서로 시각화

## 패키지 표현 (모놀리스)

```
src/main/java/com/example/
├── ordering/                  ← Bounded Context 1
│   ├── domain/
│   │   ├── Customer.java      ← Ordering 의 Customer (구매자)
│   │   └── Order.java
│   └── ...
├── billing/                   ← Bounded Context 2
│   ├── domain/
│   │   ├── Customer.java      ← Billing 의 Customer (결제자)
│   │   └── Invoice.java
│   └── ...
└── shared/                    ← 정말 공유해야 할 것만 (Money 같은 진짜 범용)
    └── kernel/
```

`ordering.Customer` ≠ `billing.Customer`. 두 클래스는 다른 클래스다.

## Context Map (관계 종류)

| 관계 | 의미 |
|---|---|
| **Partnership** | 두 컨텍스트가 함께 성공/실패. 긴밀히 협의. |
| **Customer-Supplier** | 한쪽이 다른 쪽에 의존. 공급자가 우선순위 조율. |
| **Conformist** | 다운스트림이 업스트림 모델을 그대로 받아들임. |
| **Anti-Corruption Layer** | 다른 컨텍스트로부터 자기 모델을 보호하는 번역 계층. |
| **Shared Kernel** | 작은 공유 코드 (`Money` 같은 정말 범용 값) — 신중히. |
| **Open Host Service** | 공개 프로토콜로 다수에 노출 (REST API). |
| **Published Language** | 표준화된 메시지/이벤트 포맷. |

## 컨텍스트 간 통신 패턴

```text
// Ordering 컨텍스트가 Customer 정보 필요
// X: billing.Customer 직접 import
// O: Ordering 자체 Customer 정의 + ACL 로 번역

// ordering/infrastructure/billing/
class BillingCustomerAdapter:                    // ACL
    billingClient: BillingHttpClient

    fetchCustomer(id: CustomerId) -> Customer:   // Ordering 의 Customer
        dto = billingClient.getCustomer(id.value)
        return Customer(
            id = CustomerId(dto.uuid),
            name = dto.fullName,
            // billing 의 결제 정보는 Ordering에 무의미 → 버림
        )
```

## 금지
- **공유 모델 욕심** — "어차피 같은 Customer니까 클래스 하나로" → 결국 거대 모델로 폭발
- **God Context** — 한 컨텍스트가 모든 걸 알아야 함. 분할 실패의 신호.
- **Anemic Context Map** — 컨텍스트들만 그리고 관계 표시 안 함. 관계가 본질.
- **CRUD Context** — 컨텍스트 경계를 엔티티 기준으로 자르기. 비즈니스 능력 기준으로 잘라야.
- **무분별한 Shared Kernel** — 공유는 결합. 최소화.

## 산출물

`docs/context-map.md` 에 저장:

```markdown
# Context Map

## Contexts
- **Ordering** — 주문 접수, 라이프사이클
- **Billing** — 결제, 환불, 청구서
- **Fulfillment** — 출하, 배송

## Relationships
- Ordering ──(events)──> Billing (Customer-Supplier, 비동기)
- Ordering ──(events)──> Fulfillment
- Billing <──(ACL)── Ordering (결제 상태 조회)
```

## 참고
- 컨텍스트 분리는 비싸지만, 안 하면 더 비싸진다
- 의심스러우면 한 컨텍스트로 시작하고, 패키지 분리로 경계 연습 → 진짜 분리해도 될 때 모듈/서비스로 승격
