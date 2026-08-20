from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeAlias

from app.presentation.api.calculation.request import CalculationResponse


RequestFingerprint: TypeAlias = tuple[float, str, float]


class IdempotencyConflict(Exception):
    pass


class InvalidIdempotencyKey(Exception):
    pass


@dataclass(frozen=True)
class IdempotencyResult:
    response: CalculationResponse
    replayed: bool


class IdempotencyStore(Protocol):
    def execute(
        self,
        key: str,
        fingerprint: RequestFingerprint,
        operation: Callable[[], CalculationResponse],
    ) -> IdempotencyResult: ...


def normalize_idempotency_key(raw_key: str) -> str:
    key = raw_key.strip()
    if not key or len(key) > 255:
        raise InvalidIdempotencyKey
    return key
