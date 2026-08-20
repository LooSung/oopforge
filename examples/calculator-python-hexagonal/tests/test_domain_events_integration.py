import pytest

from app.application.domain_events import (
    CalculationPerformedHandler,
    DomainEventDispatcher,
)
from app.application.outbox import CalculationPerformedV1
from app.application.services.calculation.calculate_service import (
    CalculateCommand,
    CalculateService,
)
from app.domain.calculation.model import CalculationPerformed, Operator
from app.infrastructure.event_relay import IdempotentConsumer, OutboxRelay
from app.infrastructure.in_memory_outbox import InMemoryOutbox
from app.infrastructure.in_memory_transaction import InMemoryTransactionRunner
from app.infrastructure.repositories.calculation.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)


def build_service() -> tuple[CalculateService, InMemoryOutbox]:
    repository = InMemoryCalculationRepository()
    outbox = InMemoryOutbox()
    handler = CalculationPerformedHandler(outbox)
    dispatcher = DomainEventDispatcher({CalculationPerformed: (handler,)})
    transaction = InMemoryTransactionRunner(repository, outbox)
    return CalculateService(repository, transaction, dispatcher), outbox


def test_versioned_payload_and_duplicate_delivery_have_one_effect() -> None:
    service, outbox = build_service()
    result = service.handle(CalculateCommand(8, Operator.DIVIDE, 2))
    message = outbox.unpublished()[0]

    assert message.event_type == "CalculationPerformedV1"
    assert message.aggregate_id == result.calculation_id
    assert message.payload.schema_version == 1
    assert message.payload.calculation_id == result.calculation_id
    assert message.payload.result == 4

    effects: list[CalculationPerformedV1] = []
    consumer = IdempotentConsumer(effects.append)
    consumer.consume(message)
    assert OutboxRelay(outbox, consumer).relay() == 1
    assert effects == [message.payload]
    assert outbox.unpublished() == ()


def test_relay_leaves_message_unpublished_when_consumer_fails() -> None:
    service, outbox = build_service()
    service.handle(CalculateCommand(1, Operator.ADD, 2))
    message = outbox.unpublished()[0]

    def fail(_: CalculationPerformedV1) -> None:
        raise RuntimeError("consumer failed")

    relay = OutboxRelay(outbox, IdempotentConsumer(fail))
    with pytest.raises(RuntimeError, match="consumer failed"):
        relay.relay()

    assert outbox.unpublished() == (message,)
