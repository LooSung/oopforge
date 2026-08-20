from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class CalculationPerformedV1:
    event_id: str
    calculation_id: str
    result: float
    occurred_at: datetime
    schema_version: int = field(default=1, init=False)


@dataclass(frozen=True)
class OutboxMessage:
    id: str
    event_type: str
    aggregate_id: str
    payload: CalculationPerformedV1
    occurred_at: datetime
    published_at: datetime | None = None


class OutboxPort(Protocol):
    def append(self, event: CalculationPerformedV1) -> None: ...


class RelayOutboxPort(Protocol):
    def unpublished(self) -> tuple[OutboxMessage, ...]: ...

    def mark_published(self, message_id: str) -> None: ...
