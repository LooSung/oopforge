from collections.abc import Iterable, Mapping, Sequence
from typing import Protocol

from app.application.outbox import CalculationPerformedV1, OutboxPort
from app.domain.calculation.model import CalculationPerformed, DomainEvent


class DomainEventHandler(Protocol):
    def handle(self, event: DomainEvent) -> None: ...


class DomainEventDispatcher:
    def __init__(
        self,
        handlers: Mapping[type[DomainEvent], Sequence[DomainEventHandler]],
    ) -> None:
        self._handlers = {
            event_type: tuple(event_handlers)
            for event_type, event_handlers in handlers.items()
        }

    def dispatch(self, events: Iterable[DomainEvent]) -> None:
        for event in events:
            for handler in self._handlers.get(type(event), ()):
                handler.handle(event)


class CalculationPerformedHandler:
    def __init__(self, outbox: OutboxPort) -> None:
        self._outbox = outbox

    def handle(self, event: DomainEvent) -> None:
        if not isinstance(event, CalculationPerformed):
            raise TypeError(f"unsupported event: {type(event).__name__}")
        self._outbox.append(
            CalculationPerformedV1(
                event_id=event.event_id,
                calculation_id=str(event.calculation_id.value),
                result=event.result,
                occurred_at=event.occurred_at,
            )
        )
