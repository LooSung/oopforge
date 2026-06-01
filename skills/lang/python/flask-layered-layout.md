---
name: python-flask-layered-layout
description: Flask 3계층(Blueprint/Service/Repository) 레이아웃. application factory + flask-smorest로 OpenAPI 자동 노출.
tags: [python, flask, layered, layout]
stability: stable
---

# Python — Flask Layered Layout (3-tier)

## 언제 쓰나
- 사내 표준이 Flask인 팀의 신규 백엔드
- 작은~중간 규모 REST 서비스
- FastAPI로 마이그레이션 부담이 큰 환경

도메인이 복잡해지면 동일 레이아웃을 유지한 채 도메인 레이어를 분리하거나, FastAPI clean으로 전환.

## 기준
`Blueprint(controller) → Service → Repository` 3계층 + application factory + `flask-smorest`로 OpenAPI 기본 탑재.

## 체크리스트
- [ ] Application factory 패턴 (`create_app()`)
- [ ] `flask-smorest`로 Swagger UI 자동 노출 (`/api/v1/docs`)
- [ ] 큰 영역: `blueprints`, `services`, `repositories`, `models`, `schemas`, `core`, `infrastructure`
- [ ] `blueprints` → `flask_smorest.Blueprint`, request/response 매핑
- [ ] `services` → 비즈니스 로직, 트랜잭션 경계
- [ ] `repositories` → SQLAlchemy 접근
- [ ] `models` → SQLAlchemy ORM 또는 도메인 클래스
- [ ] `schemas` → Marshmallow 스키마 (request/response, ≠ ORM 모델)
- [ ] `core` → 설정, DB, DI, 예외 핸들러
- [ ] `infrastructure` → 외부 API 클라이언트, 캐시 등
- [ ] `pyproject.toml`로 패키지 관리

## 표준 레이아웃

```text
app/
├── __init__.py                          ← create_app(), extensions 초기화
├── extensions.py                        ← db = SQLAlchemy(), api = Api()
│
├── order/                               ← Bounded Context
│   ├── blueprint.py                     ← Blueprint(prefix=/api/v1/orders)
│   ├── service.py
│   ├── repository.py
│   ├── models.py                        ← Order(db.Model)
│   ├── schemas.py                       ← PlaceOrderSchema, OrderResponseSchema
│   └── exceptions.py
│
├── core/
│   ├── config.py                        ← Config 클래스 (env)
│   ├── database.py
│   ├── dependencies.py                  ← 서비스 팩토리
│   ├── exceptions.py                    ← ErrorResponseSchema, 핸들러
│   └── logging.py
│
└── infrastructure/
    ├── clients/
    │   └── payment_client.py
    ├── cache/
    └── messaging/

tests/
├── unit/order/
├── integration/order/
└── e2e/

pyproject.toml
wsgi.py                                  ← create_app()
```

## 의존 규칙

```text
blueprint ──→ service ──→ repository ──→ models
                    │
                    ▼
            infrastructure.clients

core      →  설정·DB·예외·DI
```

- `blueprint` → `service` 호출만. `repository` 직접 호출 금지.
- `service` → `repository`, `models`, `infrastructure.clients` 호출.
- `models` → 외부 의존 최소. SQLAlchemy 매핑 허용, Flask import 금지.

## 최소 템플릿

```python
# app/__init__.py
from flask import Flask
from flask_smorest import Api
from .extensions import db
from .core.config import Config

def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["API_TITLE"] = "Order Service"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/api/v1"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    db.init_app(app)
    api = Api(app)

    from .order.blueprint import bp as order_bp
    api.register_blueprint(order_bp)
    return app
```

```python
# app/order/schemas.py
from marshmallow import Schema, fields

class PlaceOrderSchema(Schema):
    customer_id = fields.Int(required=True)
    items = fields.List(fields.Dict(), required=True)

class OrderResponseSchema(Schema):
    id = fields.Int()
    status = fields.Str()
    total = fields.Float()
```

```python
# app/order/blueprint.py
from flask.views import MethodView
from flask_smorest import Blueprint
from .schemas import PlaceOrderSchema, OrderResponseSchema
from .service import OrderService
from app.core.dependencies import get_order_service

bp = Blueprint("order", __name__, url_prefix="/api/v1/orders", description="Order ops")

@bp.route("")
class OrderCollection(MethodView):
    @bp.arguments(PlaceOrderSchema)
    @bp.response(201, OrderResponseSchema)
    def post(self, payload):
        svc: OrderService = get_order_service()
        return svc.place(payload)
```

```python
# app/order/service.py
from .repository import OrderRepository
from .models import Order

class OrderService:
    def __init__(self, repo: OrderRepository, payment):
        self.repo = repo
        self.payment = payment

    def place(self, payload: dict) -> Order:
        order = Order.create(payload["customer_id"], payload["items"])
        self.payment.authorize(order.total)
        return self.repo.save(order)
```

## 금지
- **Blueprint에서 Repository 직접 호출** — 항상 Service 경유.
- **ORM 모델을 응답으로 그대로 반환** — Marshmallow 스키마로 매핑.
- **`schemas`와 `models` 한 파일에 섞기** — 분리.
- **`g.repository` 같은 글로벌 상태로 의존성 전달** — 명시적 DI.
- **비즈니스 로직을 Blueprint에 작성** — Blueprint는 매핑·검증·HTTP 코드만.
- **`create_app` 없이 모듈 최상위에 `app = Flask(__name__)`** — 테스트와 설정 분리가 깨짐.

## 도구
- 패키징: `uv` 또는 `poetry`
- OpenAPI: `flask-smorest`
- ORM: `flask-sqlalchemy`
- 마이그레이션: `flask-migrate` (Alembic)
- 린트: `ruff`
- 타입: `mypy`
- 테스트: `pytest` + `pytest-flask`
