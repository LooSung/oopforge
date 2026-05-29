---
name: oop-repository-port
description: 애그리거트 영속화를 위한 outbound port (인터페이스). 도메인 레이어에 위치, 구현은 infrastructure에.
tags: [oop, ddd, port, repository]
stability: stable
---

# OOP — Repository Port

## 언제 쓰나
애그리거트를 영속화/조회해야 할 때. **도메인 레이어**에 인터페이스로 정의하고,
**infrastructure 레이어**에서 JPA/MyBatis/SQLAlchemy 등으로 구현.

## 체크리스트
- [ ] 애그리거트 단위로만 정의 (엔티티별 X)
- [ ] 도메인 언어 사용 (`findActiveByCustomer`, `findById`)
- [ ] 도메인 객체를 입출력으로 사용 (DTO/Entity 변환 X)
- [ ] CRUD 4원칙 강요하지 않음 (필요한 메서드만)
- [ ] 쿼리 메서드는 도메인 의도를 표현 (`findOverdue`, not `findByDateLessThan`)
- [ ] 조회 메서드는 `Optional` 또는 nullable 반환 (예외 X)
- [ ] 페이징/정렬은 도메인 객체 (`Pagination`, `Sort`) 로

## 템플릿 (의사 코드)

```text
// domain/port/OrderRepository
interface OrderRepository:
    findById(id: OrderId) -> Order?
    findActiveByCustomer(customerId: CustomerId) -> List<Order>
    save(order: Order) -> void
    delete(order: Order) -> void

// 도메인 의도를 표현하는 쿼리
interface OrderRepository:
    findOverdueOrders(asOf: Instant) -> List<Order>
    countPendingByCustomer(id: CustomerId) -> int
```

## 구현 위치

```text
domain/
└── port/
    └── OrderRepository.java          ← 인터페이스만

infrastructure/
└── persistence/
    ├── OrderJpaEntity.java           ← JPA 매핑용
    ├── OrderJpaRepository.java       ← Spring Data 인터페이스
    └── OrderRepositoryImpl.java      ← OrderRepository 구현, 매퍼
```

## 금지
- **도메인 객체에 JPA 어노테이션** — Order(도메인) ≠ OrderJpaEntity(영속화). 분리.
- **CRUD 강제 (`update`, `delete` 무조건 추가)** — 도메인이 요구할 때만
- **`Pageable`, `Specification` 같은 프레임워크 타입 노출** — 도메인 레이어에 누수
- **N+1 쿼리 유발 메서드 무비판 추가** — 성능 우려는 인터페이스에서도 고려
- **트랜잭션 시작/종료 책임 가짐** — 트랜잭션은 application service에서 관리

## 변형
- **CQRS**: 쓰기는 Repository, 읽기는 별도 QueryService (read model)
- **In-memory 구현**: 테스트용으로 항상 하나 두면 단위 테스트 빨라짐

## 참고
- "Repository는 Collection처럼 느껴져야 한다" — Evans
- `save(order)` 호출 후에도 동일 객체로 작업 가능해야 자연스러움
