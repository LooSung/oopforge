from collections.abc import Callable
from dataclasses import dataclass
from threading import RLock

from app.presentation.api.calculation.request import CalculationResponse
from app.presentation.api.idempotency import (
    IdempotencyConflict,
    IdempotencyResult,
    RequestFingerprint,
)


@dataclass(frozen=True)
class _StoredResponse:
    fingerprint: RequestFingerprint
    response: CalculationResponse


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._entries: dict[str, _StoredResponse] = {}
        self._lock = RLock()

    def execute(
        self,
        key: str,
        fingerprint: RequestFingerprint,
        operation: Callable[[], CalculationResponse],
    ) -> IdempotencyResult:
        with self._lock:
            stored = self._entries.get(key)
            if stored is not None:
                return self._replay(stored, fingerprint)
            response = operation()
            self._entries[key] = _StoredResponse(fingerprint, response.model_copy(deep=True))
            return IdempotencyResult(response, replayed=False)

    @staticmethod
    def _replay(
        stored: _StoredResponse,
        fingerprint: RequestFingerprint,
    ) -> IdempotencyResult:
        if stored.fingerprint != fingerprint:
            raise IdempotencyConflict
        return IdempotencyResult(stored.response.model_copy(deep=True), replayed=True)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
