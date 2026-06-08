---
name: oop-cqrs
description: 읽기(Query)와 쓰기(Command)를 분리하되 스토어는 공유하는 미디엄 수준 CQRS를 layered/헥사고날에 적용한다. 진입 기준과 금지 포함.
tags: [cqrs, oop, ddd, layered, hexagonal]
stability: experimental
---

# OOP — CQRS (medium)

## 언제 쓰나

읽기와 쓰기의 모양이 충분히 달라서 한 모델로 둘 다 감당하기 어려울 때.
**기본 깊이는 미디엄**: Command/Query 경로·DTO를 분리하되 **스토어(DB)는 공유**한다.
event-sourcing이나 읽기/쓰기 DB 분리는 이 스킬의 범위가 아니다(장기 항목).

## 진입 기준 (셋 중 하나도 안 맞으면 도입하지 말 것)

- [ ] 읽기 모델과 쓰기 모델의 모양이 크게 다르다 (조회는 조인·집계, 쓰기는 단일 애그리거트).
- [ ] 복잡 조회·리포팅이 애그리거트 로직을 오염시키고 있다.
- [ ] 읽기 성능 요구(캐시·프로젝션)가 분리를 정당화한다.

기준 미달이면 일반 layered/헥사고날을 유지한다. **필요 없는 CQRS는 안티패턴이다.**

## 핵심 규칙

- **Command**: 애그리거트를 로드 → 행동 메서드 호출 → 저장. 불변식은 도메인이 지킨다.
- **Query**: 애그리거트를 로드하지 **않는다.** 읽기 전용 모델(ReadModel/DTO)로 직접 조회한다.
- 쿼리 측은 **부수효과 없음**. 커맨드 측은 **read-shaped 데이터 반환 금지** — ID 또는 void.

## Layered 매핑

```text
order/
├── controller/
│   ├── OrderCommandController.java   # POST/PUT/DELETE
│   └── OrderQueryController.java     # GET
├── service/
│   ├── OrderCommandService.java      # 애그리거트 orchestration
│   └── OrderQueryService.java        # ReadModel 조회만
├── repository/
│   ├── OrderRepository.java          # 애그리거트 저장/로드 (command)
│   └── OrderQueryRepository.java     # ReadModel/projection 조회 (query)
├── domain/                           # Order 애그리거트 (command 전용)
└── readmodel/                        # OrderSummary 등 읽기 전용 DTO
```

- 쓰기: `OrderCommandController → OrderCommandService → Order(domain) → OrderRepository`
- 읽기: `OrderQueryController → OrderQueryService → OrderQueryRepository → OrderSummary`

## Hexagonal 매핑

- Command use case는 provided port (`PlaceOrder`)로 노출, 도메인을 거친다.
- Query는 **별도 provided port** (`OrderQueries`)로 노출하고, 도메인 객체가 아니라 read model을 반환한다.
- Query의 required port는 애그리거트 Repository가 아니라 읽기 전용 조회 port다.

```text
application/
├── provided/
│   ├── PlaceOrder.java          # command use case
│   └── OrderQueries.java        # query use case (read model 반환)
├── required/
│   ├── OrderRepository.java     # command: 애그리거트 영속
│   └── OrderReadModelQuery.java # query: projection 조회
└── service/
    ├── PlaceOrderService.java
    └── OrderQueryService.java
```

## OOP Contract 추가 항목

CQRS 작업이면 Craft의 OOP Contract에 한 줄씩 더한다:

```markdown
Read/Write split: <command 경로 | query 경로>
Read Model: <조회 전용 DTO 이름, 어디서 만들어지나>
Store: shared  # 미디엄은 항상 공유
```

## 금지

- **읽기/쓰기 DB 분리·이벤트소싱을 미디엄에 끌어들이지 않는다** — 별도 결정·별도 작업.
- **Query에서 애그리거트 로드 금지** — read model로 직접 조회.
- **Command가 query DTO 반환 금지** — ID 또는 void.
- **진입 기준 미달인데 CQRS 적용 금지** — 과설계.
- **Command/Query가 같은 서비스 클래스에 섞이지 않게 한다** — 분리가 목적.

## 관련

- `skills/lang/backend-stack.md` — 스택 선택 (CQRS는 변형)
- `skills/skeleton/backend-skeleton.md` — 레이어 폴더 표준
- `skills/oop/use-case-boundary.md` — use case / port 경계
- `AGENTS.md` Hard Rules — CQRS 규칙
