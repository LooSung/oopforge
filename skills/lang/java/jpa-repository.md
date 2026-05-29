---
name: java-jpa-repository
description: JPA로 도메인 Repository port를 구현할 때. 도메인 모델과 JPA Entity를 분리하는 방법.
tags: [java, spring, jpa, repository]
stability: stable
---

# Java — JPA Repository Implementation

## 언제 쓰나
도메인 `OrderRepository` 인터페이스를 JPA로 구현할 때.
**도메인 모델을 그대로 `@Entity`로 쓰지 않는다.**

## 체크리스트
- [ ] 도메인 클래스(`Order`)와 JPA 클래스(`OrderJpaEntity`) 분리
- [ ] Mapper 클래스가 두 모델 간 변환 담당
- [ ] Spring Data 인터페이스(`OrderJpaRepository`)는 infrastructure 내부에서만 사용
- [ ] 도메인 port 구현체(`OrderRepositoryImpl`)가 외부 진입점
- [ ] 트랜잭션은 application service에서 관리, repository는 단순 read/write
- [ ] N+1 회피를 위한 fetch 전략 명시

## 템플릿

```java
// domain/port/OrderRepository.java
package com.example.order.domain.port;

public interface OrderRepository {
    Optional<Order> findById(OrderId id);
    void save(Order order);
}

// infrastructure/persistence/OrderJpaEntity.java
package com.example.order.infrastructure.persistence;

@Entity
@Table(name = "orders")
class OrderJpaEntity {
    @Id private String id;
    private String customerId;
    @Enumerated(EnumType.STRING) private String status;
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLineJpaEntity> lines = new ArrayList<>();

    protected OrderJpaEntity() {}  // JPA 강제, package-private
    // getter only - setter 없음, 도메인 변환만 허용
}

// infrastructure/persistence/OrderJpaRepository.java
package com.example.order.infrastructure.persistence;

interface OrderJpaRepository extends JpaRepository<OrderJpaEntity, String> {
    // Spring Data 내부 전용
}

// infrastructure/persistence/OrderRepositoryImpl.java
package com.example.order.infrastructure.persistence;

@Repository
class OrderRepositoryImpl implements OrderRepository {
    private final OrderJpaRepository jpa;
    private final OrderMapper mapper;

    public Optional<Order> findById(OrderId id) {
        return jpa.findById(id.value()).map(mapper::toDomain);
    }

    public void save(Order order) {
        jpa.save(mapper.toEntity(order));
    }
}

// infrastructure/persistence/OrderMapper.java
@Component
class OrderMapper {
    Order toDomain(OrderJpaEntity e) { ... }
    OrderJpaEntity toEntity(Order o) { ... }
}
```

## 금지
- **`Order` 클래스에 `@Entity`** — 도메인 오염
- **도메인 객체에서 `@OneToMany` 직접 사용** — 영속화 관심사가 도메인에 누수
- **`OrderJpaRepository` 를 application 레이어에서 직접 주입** — 항상 `OrderRepository` 포트로
- **JPA 트랜잭션 어노테이션을 도메인/application 외부에** — 트랜잭션 경계 흩어짐
- **`save()` 안에서 cascading + 외부 호출 함께** — 단일 책임 위반

## 변형
- **Read-only 모델**: 복잡한 조회는 별도 `OrderQueryService` + DTO projection
- **MyBatis/JOOQ**: 같은 패턴, 매퍼 위치만 다름
- **Soft delete**: JPA `@Where` 또는 매퍼에서 필터링
