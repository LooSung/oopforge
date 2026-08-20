from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from app.application.outbox import CalculationPerformedV1, OutboxMessage


class InMemoryOutbox:
    def __init__(self) -> None:
        self._messages: list[OutboxMessage] = []

    def append(self, event: CalculationPerformedV1) -> None:
        self._messages.append(
            OutboxMessage(
                id=str(uuid4()),
                event_type=type(event).__name__,
                aggregate_id=event.calculation_id,
                payload=event,
                occurred_at=event.occurred_at,
            )
        )

    def unpublished(self) -> tuple[OutboxMessage, ...]:
        return tuple(message for message in self._messages if message.published_at is None)

    def mark_published(self, message_id: str) -> None:
        for index, message in enumerate(self._messages):
            if message.id == message_id:
                self._messages[index] = replace(message, published_at=datetime.now(UTC))
                return
        raise KeyError(message_id)

    def snapshot(self) -> tuple[OutboxMessage, ...]:
        return tuple(self._messages)

    def restore(self, snapshot: tuple[OutboxMessage, ...]) -> None:
        self._messages = list(snapshot)
