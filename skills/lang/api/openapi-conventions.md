---
name: api-openapi-conventions
description: 백엔드 API 스켈레톤에 OpenAPI/Swagger를 기본 탑재하기 위한 언어 무관 컨벤션.
tags: [api, openapi, swagger, contract]
stability: stable
---

# API — OpenAPI Conventions

## 언제 쓰나
새 백엔드 서비스 스켈레톤을 만들 때. Java Spring / Python FastAPI / Python Flask 어떤 스택이든
OpenAPI 문서가 비어 있는 채로 출발하지 않게 강제한다.

## 체크리스트
- [ ] 빌드/런타임에 OpenAPI 스펙이 자동 생성됨 (`/v3/api-docs`, `/openapi.json`)
- [ ] Swagger UI 또는 ReDoc이 dev 환경에서 노출됨 (prod는 비공개 또는 인증 뒤)
- [ ] 모든 엔드포인트에 `tag` 부여 (bounded context 단위 권장)
- [ ] 모든 응답에 status code별 스키마 명시 (200/400/404/500)
- [ ] 에러 응답은 공용 스키마 (`ErrorResponse`) 단일화
- [ ] API 버전 prefix (`/api/v1`)
- [ ] request/response 모델 ≠ 도메인 객체 (별도 DTO)

## 표준 응답 스키마

```yaml
ErrorResponse:
  type: object
  required: [code, message]
  properties:
    code: { type: string, example: "ORDER_NOT_FOUND" }
    message: { type: string }
    details: { type: object, nullable: true }
    traceId: { type: string, nullable: true }
```

## 스택별 최소 설정

### Java Spring (`springdoc-openapi`)

```kotlin
// build.gradle.kts
implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.6.0")
```

```yaml
# application.yml
springdoc:
  api-docs.path: /v3/api-docs
  swagger-ui.path: /swagger-ui
  swagger-ui.tags-sorter: alpha
```

```java
// adapter/web/OrderController.java
@Tag(name = "Order", description = "Order placement and lifecycle")
@RestController
@RequestMapping("/api/v1/orders")
class OrderController {
    @Operation(summary = "Place a new order")
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "Created"),
        @ApiResponse(responseCode = "400", description = "Invalid input",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PostMapping
    public OrderResponse place(@RequestBody PlaceOrderRequest req) { ... }
}
```

### Python FastAPI (기본 내장)

FastAPI는 OpenAPI를 자동 생성한다. 컨벤션만 강제하면 된다.

```python
# app/main.py
app = FastAPI(
    title="Order Service",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
)
```

```python
# app/presentation/api/order/order_router.py
router = APIRouter(prefix="/api/v1/orders", tags=["Order"])

@router.post(
    "",
    response_model=OrderResponse,
    status_code=201,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Place a new order",
)
def place_order(req: PlaceOrderRequest, ...): ...
```

### Python Flask (`flask-smorest` 권장)

```python
# requirements
flask-smorest>=0.45
```

```python
# app/__init__.py
from flask_smorest import Api
api = Api(app, spec_kwargs={"title": "Order Service", "version": "1.0.0"})
```

```python
# app/presentation/order_blueprint.py
from flask_smorest import Blueprint
bp = Blueprint("order", __name__, url_prefix="/api/v1/orders", description="Order ops")

@bp.route("", methods=["POST"])
@bp.arguments(PlaceOrderSchema)
@bp.response(201, OrderResponseSchema)
@bp.alt_response(400, schema=ErrorResponseSchema)
def place_order(payload): ...
```

## 금지
- **Controller/Router에 도메인 객체를 그대로 응답** — 항상 DTO 매핑.
- **에러 응답 스키마 제각각** — 항상 `ErrorResponse` 단일.
- **`/swagger-ui`를 prod에 무방비 노출** — 인증 또는 비활성화.
- **버전 prefix 없는 엔드포인트** — `/orders` 단독 금지. `/api/v1/orders`.
- **OpenAPI 어노테이션을 도메인 레이어에 작성** — adapter/presentation에서만.

## 변형
- **gRPC + REST 병행**: `.proto`를 1차 소스로, REST는 grpc-gateway로 생성.
- **API-first 워크플로**: OpenAPI YAML을 먼저 작성 → 코드 생성 (openapi-generator). 팀이 클라이언트 별도면 강력.
