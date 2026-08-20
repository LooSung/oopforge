from collections.abc import Callable
from typing import Protocol

from app.application.outbox import (
    CalculationPerformedV1,
    OutboxMessage,
    RelayOutboxPort,
)


class OutboxConsumer(Protocol):
    def consume(self, message: OutboxMessage) -> None: ...


class IdempotentConsumer:
    def __init__(self, effect: Callable[[CalculationPerformedV1], None]) -> None:
        self._effect = effect
        self._processed_message_ids: set[str] = set()

    def consume(self, message: OutboxMessage) -> None:
        if message.id in self._processed_message_ids:
            return
        self._effect(message.payload)
        self._processed_message_ids.add(message.id)


class OutboxRelay:
    def __init__(self, outbox: RelayOutboxPort, consumer: OutboxConsumer) -> None:
        self._outbox = outbox
        self._consumer = consumer

    def relay(self) -> int:
        published = 0
        for message in self._outbox.unpublished():
            self._consumer.consume(message)
            self._outbox.mark_published(message.id)
            published += 1
        return published
