---
name: java-spring-layered-layout
description: Spring Boot 3계층(Controller/Service/Repository) 레이아웃. 헥사고날까지 필요 없는 작은 서비스의 기본 출발점.
tags: [java, spring, layered, layout]
stability: stable
---

# Java — Spring Layered Layout (3-tier)

## 언제 쓰나
- 단일 도메인 또는 1~3개 작은 도메인의 신규 서비스
- 팀이 헥사고날 학습 비용을 감당하기 어려운 초기 단계
- 빠르게 MVP를 만들고 도메인이 자라면 헥사고날로 마이그레이션할 계획

도메인 복잡도가 높거나 외부 어댑터가 다수면 처음부터 `spring-hexagonal-layout.md`를 쓴다.

## 기준
Spring 표준 `controller → service → repository` 3계층 + `domain`(엔티티/값 객체) + `config`/`infrastructure`(횡단 관심사).
헥사고날의 port/adapter는 없지만 **레이어 방향**과 **도메인 무결성**은 동일하게 강제한다.

## 체크리스트
- [ ] 루트는 Gradle Spring Boot 프로젝트
- [ ] bounded context 별 패키지 분리 (단일 도메인이면 평탄)
- [ ] 큰 영역: `controller`, `service`, `repository`, `domain`, `config`, `infrastructure`
- [ ] `controller` → REST API 입출력 + DTO
- [ ] `service` → 비즈니스 유스케이스, 트랜잭션 경계
- [ ] `repository` → Spring Data JPA 인터페이스 (또는 직접 JDBC)
- [ ] `domain` → 엔티티, 값 객체, 도메인 예외 (가능한 한 framework-free)
- [ ] `config` → Spring Bean 설정, 시큐리티, OpenAPI
- [ ] `infrastructure` → 외부 API 클라이언트, 메시징, 캐시 등 횡단 어댑터
- [ ] `springdoc-openapi` 의존성 추가 (`skills/lang/api/openapi-conventions.md`)

## 표준 레이아웃

```text
src/main/java/com/example/
├── ExampleApplication.java
│
├── order/                               ← Bounded Context (단일 도메인이면 생략 가능)
│   ├── controller/
│   │   ├── OrderController.java
│   │   ├── dto/
│   │   │   ├── PlaceOrderRequest.java
│   │   │   └── OrderResponse.java
│   │   └── mapper/
│   │       └── OrderDtoMapper.java
│   │
│   ├── service/
│   │   ├── OrderService.java            ← 인터페이스 (선택)
│   │   └── OrderServiceImpl.java
│   │
│   ├── repository/
│   │   └── OrderRepository.java         ← extends JpaRepository<Order, Long>
│   │
│   └── domain/
│       ├── Order.java                   ← @Entity (또는 순수 도메인 + JPA 매핑 분리)
│       ├── OrderStatus.java
│       └── OrderException.java
│
├── config/
│   ├── OpenApiConfig.java
│   ├── SecurityConfig.java
│   └── JpaConfig.java
│
└── infrastructure/
    ├── client/
    │   └── PaymentClient.java           ← 외부 API
    ├── messaging/
    └── cache/
```

테스트는 같은 구조 미러링:

```text
src/test/java/com/example/order/
├── controller/    ← MockMvc / WebMvcTest
├── service/       ← 단위 테스트
├── repository/    ← @DataJpaTest
└── domain/        ← 순수 단위 테스트
```

## 의존 규칙

```text
controller ──→ service ──→ repository
       │            │           │
       │            ▼           ▼
       └─────→  domain (엔티티/값 객체)

infrastructure ←── service (필요할 때만)
config       →  Bean wiring
```

- `controller` → `service` 호출. **`repository` 직접 호출 금지**.
- `service` → `repository`, `domain`, `infrastructure.client` 호출.
- `repository` → `domain` 엔티티만 다룸.
- `domain` → 외부 의존 0 (이상적). 현실적으로 JPA 어노테이션 허용하되 Spring/Service 의존 금지.
- 순환 의존 금지.

## 최소 템플릿

```java
// controller/OrderController.java
@Tag(name = "Order")
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
class OrderController {
    private final OrderService orderService;

    @PostMapping
    public OrderResponse place(@RequestBody @Valid PlaceOrderRequest req) {
        return OrderDtoMapper.toResponse(orderService.place(req.toCommand()));
    }
}

// service/OrderServiceImpl.java
@Service
@Transactional
@RequiredArgsConstructor
class OrderServiceImpl implements OrderService {
    private final OrderRepository orderRepository;
    private final PaymentClient paymentClient;

    public Order place(PlaceOrderCommand cmd) {
        Order order = Order.create(cmd.customerId(), cmd.lines());
        paymentClient.authorize(order.totalAmount());
        return orderRepository.save(order);
    }
}

// repository/OrderRepository.java
interface OrderRepository extends JpaRepository<Order, Long> {
    Optional<Order> findByCustomerId(Long customerId);
}
```

## 금지
- **Controller에서 Repository 직접 호출** — 항상 Service 경유.
- **Service 간 순환 의존** — 도메인 이벤트 또는 별도 모듈로 분리.
- **Entity를 그대로 응답 DTO로 반환** — 항상 매핑 (지연 로딩 사고/정보 노출 방지).
- **`@Setter` 도메인에 추가** — 의도된 메서드(`changeStatus()`)로.
- **비즈니스 로직을 Controller에 작성** — Controller는 매핑·검증·HTTP 코드만.
- **Repository에 비즈니스 메서드 추가** (`findActiveOrdersWithDiscountApplied()`) — 쿼리만, 판단은 Service.

## 변형 — 헥사고날로 마이그레이션
도메인이 자라면(어댑터 3개 이상, 외부 의존 다수, 테스트가 어려워짐):
1. `service/` → `application/service/` 이동, 인터페이스를 `application/provided/`로
2. `repository/` 인터페이스 → `application/required/`, JPA 구현은 `adapter/persistence/`
3. `infrastructure/client/` → `adapter/integration/`
4. 자세히는 `skills/lang/java/spring-hexagonal-layout.md`

## 참고
- 단일 모듈, 단일 도메인이면 최상위 패키지(`controller/`, `service/`, ...) 평탄해도 됨.
- 도메인 2개 이상이면 반드시 bounded context 패키지로 묶기.
