from collections.abc import Callable
from typing import TypeVar

from app.infrastructure.in_memory_outbox import InMemoryOutbox
from app.infrastructure.repositories.calculation.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)


T = TypeVar("T")


class InMemoryTransactionRunner:
    def __init__(
        self,
        repository: InMemoryCalculationRepository,
        outbox: InMemoryOutbox,
    ) -> None:
        self._repository = repository
        self._outbox = outbox

    def run(self, operation: Callable[[], T]) -> T:
        repository_snapshot = self._repository.snapshot()
        outbox_snapshot = self._outbox.snapshot()
        try:
            return operation()
        except BaseException:
            self._repository.restore(repository_snapshot)
            self._outbox.restore(outbox_snapshot)
            raise
