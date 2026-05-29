---
name: java-spring-hexagonal-layout
description: Spring Boot 프로젝트의 헥사고날 아키텍처 패키지 구조와 의존 규칙.
tags: [java, spring, hexagonal, layout]
stability: stable
---

# Java — Spring Hexagonal Layout

## 언제 쓰나
Spring Boot 기반 새 모듈/서비스를 시작할 때. 모든 OOPforge 프로젝트의 기본 레이아웃.

## 체크리스트
- [ ] 4개 레이어: domain, application, infrastructure, interfaces
- [ ] domain 레이어는 Spring/JPA import 0
- [ ] 모듈 별로 패키지 분리 (`com.example.order`, `com.example.payment`)
- [ ] ArchUnit 등으로 레이어 의존성 강제 (선택)
- [ ] `interfaces` (inbound) vs `infrastructure` (outbound) 구분
- [ ] 메인 설정 클래스는 루트 패키지에

## 표준 레이아웃

```
src/main/java/com/example/order/
├── OrderApplication.java                ← @SpringBootApplication
│
├── domain/                              ← 프레임워크 import 금지
│   ├── model/
│   │   ├── Order.java                   ← Aggregate Root
│   │   ├── OrderLine.java
│   │   ├── OrderId.java                 ← Value Object
│   │   └── OrderStatus.java
│   ├── event/
│   │   ├── OrderPlaced.java
│   │   └── OrderCancelled.java
│   └── port/                            ← outbound ports
│       ├── OrderRepository.java
│       └── PaymentGateway.java
│
├── application/                         ← 유스케이스 오케스트레이션
│   ├── command/
│   │   ├── PlaceOrderCommand.java
│   │   └── CancelOrderCommand.java
│   └── usecase/
│       ├── PlaceOrder.java              ← @Service, @Transactional
│       └── CancelOrder.java
│
├── infrastructure/                      ← outbound 어댑터 (구현)
│   ├── persistence/
│   │   ├── OrderJpaEntity.java          ← @Entity (도메인과 분리)
│   │   ├── OrderJpaRepository.java      ← Spring Data
│   │   ├── OrderRepositoryImpl.java     ← domain port 구현
│   │   └── OrderMapper.java             ← Entity ↔ Domain
│   ├── external/
│   │   └── PaymentGatewayHttpAdapter.java
│   └── config/
│       └── BeanConfiguration.java
│
└── interfaces/                          ← inbound 어댑터
    └── rest/
        ├── OrderController.java
        ├── PlaceOrderRequest.java       ← DTO (입력)
        └── OrderResponse.java           ← DTO (출력)
```

## 의존 규칙 (절대)

```
interfaces ──────┐
                 ▼
application ──→ domain ←── infrastructure
                 ▲
                 │
       (domain은 어떤 레이어도 import하지 않음)
```

- `domain` → import 0 (java.* 와 외부 라이브러리 중 java spec 만 허용)
- `application` → domain만 import
- `infrastructure` → domain (port 구현 위함)
- `interfaces` → application

## ArchUnit 예시 (선택)

```java
@Test
void domainHasNoSpringDependency() {
    noClasses().that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAnyPackage(
            "org.springframework..", "jakarta.persistence.."
        )
        .check(classes);
}
```

## 금지
- **도메인 클래스에 `@Entity`, `@Component`, `@Autowired`** — 절대.
- **`domain` 패키지에 `infrastructure` import** — 의존 방향 위반.
- **Controller에서 Repository 직접 호출** — 항상 use case 경유.
- **Lombok `@Setter` 도메인에 추가** — `@Getter`만, setter는 의도된 도메인 메서드로.
- **순환 의존** — 모듈 간 양방향 의존 시 이벤트로 분리.

## 참고
- 모노리스에서도 모듈 단위로 위 구조 반복 (`com.example.order`, `com.example.payment` 각각)
- Maven 멀티 모듈로 강제하면 더 안전 (`domain` 모듈이 `spring-boot-starter`를 모름)
