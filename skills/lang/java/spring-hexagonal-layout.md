---
name: java-spring-hexagonal-layout
description: Splearn 스타일의 Spring Boot 헥사고날 아키텍처 패키지 구조와 의존 규칙.
tags: [java, spring, hexagonal, layout]
stability: stable
---

# Java — Spring Hexagonal Layout

## 언제 쓰나
Spring Boot 기반 새 모듈/서비스를 시작할 때. OOPforge Java 프로젝트의 기본 레이아웃.

## 기준
토비의 Clean Spring / Splearn 스타일을 OOPforge Java 기본 구조로 삼는다.
핵심은 `application/provided` 와 `application/required` 를 분리해 inbound/outbound port를 명확히 하는 것이다.

## 체크리스트
- [ ] 루트는 Gradle Spring Boot 프로젝트 (`build.gradle.kts`, `settings.gradle.kts`)
- [ ] bounded context 별 패키지 분리 (`com.example.order`, `com.example.payment`)
- [ ] 큰 영역: `domain`, `application`, `adapter`, `config`
- [ ] `application/provided`: inbound port (use case API)
- [ ] `application/required`: outbound port (repository/gateway)
- [ ] `application/service`: use case implementation
- [ ] `adapter/web`: inbound web adapter
- [ ] `adapter/persistence`, `adapter/integration`: outbound adapter
- [ ] domain 레이어는 Spring/JPA import 0
- [ ] 메인 설정 클래스는 루트 패키지에
- [ ] ArchUnit 등으로 레이어 의존성 강제 (선택)

## 표준 레이아웃

```text
src/main/java/com/example/
├── ExampleApplication.java              ← @SpringBootApplication
│
├── order/                               ← Bounded Context
│   ├── domain/                          ← framework import 0
│   │   ├── Order.java                   ← Aggregate Root
│   │   ├── OrderLine.java
│   │   ├── OrderId.java                 ← Value Object
│   │   ├── OrderStatus.java
│   │   └── OrderPlaced.java             ← Domain Event
│   │
│   ├── application/
│   │   ├── provided/                    ← inbound port
│   │   │   ├── PlaceOrder.java
│   │   │   └── CancelOrder.java
│   │   ├── required/                    ← outbound port
│   │   │   ├── OrderRepository.java
│   │   │   └── PaymentGateway.java
│   │   └── service/                     ← use case implementation
│   │       ├── PlaceOrderService.java
│   │       └── CancelOrderService.java
│   │
│   ├── adapter/
│   │   ├── web/
│   │   │   ├── OrderController.java
│   │   │   ├── PlaceOrderRequest.java
│   │   │   └── OrderResponse.java
│   │   ├── persistence/
│   │   │   ├── OrderJpaEntity.java
│   │   │   ├── OrderJpaRepository.java
│   │   │   ├── OrderRepositoryAdapter.java
│   │   │   └── OrderMapper.java
│   │   └── integration/
│   │       └── PaymentGatewayAdapter.java
│   │
│   └── config/
│       └── OrderConfig.java
│
└── shared/
    ├── domain/
    │   └── Money.java
    └── config/
```

테스트는 같은 bounded context를 미러링한다.

```text
src/test/java/com/example/order/
├── domain/
├── application/
└── adapter/
```

## 의존 규칙

```text
adapter ────────→ application ───────→ domain
                       │
                       ▼
              application.required  ← adapter persistence/integration 구현
```

- `domain` → import 0 (java.* 와 외부 라이브러리 중 java spec 만 허용)
- `application.provided` → 외부에 노출할 use case interface
- `application.required` → repository/gateway 등 outbound port
- `application.service` → provided 구현, required 사용
- `adapter.web` → provided 호출
- `adapter.persistence/integration` → required 구현
- `config` → Bean wiring

## 금지
- **도메인 클래스에 `@Entity`, `@Component`, `@Autowired`** — 절대.
- **`domain` 패키지에 `adapter` import** — 의존 방향 위반.
- **Controller에서 Repository 직접 호출** — 항상 use case 경유.
- **Lombok `@Setter` 도메인에 추가** — setter는 의도된 도메인 메서드로.
- **순환 의존** — 모듈 간 양방향 의존 시 이벤트로 분리.

## 참고
- 모노리스에서도 bounded context 단위로 위 구조 반복.
- 멀티 모듈로 강제하면 더 안전하다 (`domain` 모듈이 Spring Boot를 모름).
