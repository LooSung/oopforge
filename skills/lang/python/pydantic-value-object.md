---
name: python-pydantic-value-object
description: Python에서 Pydantic으로 값 객체를 정의할 때. 불변, 자동 검증, 깔끔.
tags: [python, pydantic, value-object]
stability: stable
---

# Python — Pydantic Value Object

## 언제 쓰나
Python에서 값 객체를 만들 때. Pydantic v2 기준.
표준 라이브러리만 쓸 거면 `@dataclass(frozen=True)` 도 가능.

## 체크리스트
- [ ] `model_config = ConfigDict(frozen=True)` 로 불변 강제
- [ ] 필드 타입 명시 (typing)
- [ ] 검증은 `field_validator` 또는 `model_validator`
- [ ] 변경이 필요하면 `model_copy(update={...})` 로 새 인스턴스
- [ ] `__eq__`, `__hash__` 는 Pydantic이 자동 처리 (frozen=True 시 hashable)
- [ ] FastAPI request DTO와 도메인 값 객체는 **분리**

## 템플릿 (Pydantic v2)

```python
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator

class Money(BaseModel):
    model_config = ConfigDict(frozen=True)

    amount: Decimal
    currency: str

    @field_validator("amount")
    @classmethod
    def _non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("amount must be >= 0")
        return v

    @field_validator("currency")
    @classmethod
    def _iso(cls, v: str) -> str:
        if len(v) != 3 or not v.isupper():
            raise ValueError("currency must be ISO 4217 (e.g. USD)")
        return v

    def add(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def multiply(self, factor: Decimal) -> "Money":
        return Money(amount=self.amount * factor, currency=self.currency)


class OrderId(BaseModel):
    model_config = ConfigDict(frozen=True)
    value: str

    @field_validator("value")
    @classmethod
    def _uuid_format(cls, v: str) -> str:
        from uuid import UUID
        UUID(v)  # raises if invalid
        return v
```

## dataclass 변형 (의존성 최소)

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("amount must be >= 0")
```

## 금지
- **`frozen=True` 빠뜨림** — 변경 가능한 값 객체는 의미 없음
- **`Optional` 남발** — 값 객체는 가능하면 non-null
- **검증 없는 생성자** — `Money(amount=-1, currency="zz")` 가 통과되면 안 됨
- **API DTO와 도메인 값 객체 공유** — 영속화/API 변경이 도메인에 누수됨
- **`Any` 타입 사용** — Pydantic 쓰는 의미 없음

## 변형
- **`__slots__`** : 메모리 최적화 (자주 생성되는 값 객체)
- **`StrEnum`** : 작은 enum 값 객체 대용
- **`NewType`** : 더 가벼운 단일 값 래퍼 (검증 안 해도 될 때)

## 참고
- Pydantic v1과 v2는 API가 다름. 이 스킬은 v2 기준.
- FastAPI 입력 DTO는 별도 `*Request` 모델로, 도메인 값 객체로 매핑.
