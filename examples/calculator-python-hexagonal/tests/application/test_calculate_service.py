from collections.abc import Callable, Iterable

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
from app.domain.calculation.model import (
    Calculation,
    CalculationPerformed,
    DomainEvent,
    Operator,
)
from app.infrastructure.in_memory_outbox import InMemoryOutbox
from app.infrastructure.in_memory_transaction import InMemoryTransactionRunner
from app.infrastructure.repositories.calculation.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)


class RecordingRepository(InMemoryCalculationRepository):
    def __init__(self, calls: list[str]) -> None:
        super().__init__()
        self._calls = calls

    def save(self, calculation: Calculation) -> None:
        self._calls.append("save")
        assert len(calculation._events) == 1
        super().save(calculation)


class RecordingOutbox(InMemoryOutbox):
    def __init__(self, calls: list[str]) -> None:
        super().__init__()
        self._calls = calls

    def append(self, event: CalculationPerformedV1) -> None:
        self._calls.append("outbox")
        super().append(event)


class RecordingDispatcher(DomainEventDispatcher):
    def __init__(
        self,
        calls: list[str],
        handler: CalculationPerformedHandler,
    ) -> None:
        super().__init__({CalculationPerformed: (handler,)})
        self._calls = calls

    def dispatch(self, events: Iterable[DomainEvent]) -> None:
        self._calls.append("dispatch")
        super().dispatch(events)


class RecordingTransactionRunner(InMemoryTransactionRunner):
    def __init__(
        self,
        calls: list[str],
        repository: InMemoryCalculationRepository,
        outbox: InMemoryOutbox,
    ) -> None:
        super().__init__(repository, outbox)
        self._calls = calls

    def run(self, operation: Callable[[], object]) -> object:
        self._calls.append("transaction")
        return super().run(operation)


class FailingHandler:
    def __init__(self) -> None:
        self.event: CalculationPerformed | None = None

    def handle(self, event: DomainEvent) -> None:
        assert isinstance(event, CalculationPerformed)
        self.event = event
        raise RuntimeError("handler failed")


def test_handle_saves_then_drains_and_dispatches_once(monkeypatch) -> None:
    calls: list[str] = []
    repository = RecordingRepository(calls)
    outbox = RecordingOutbox(calls)
    handler = CalculationPerformedHandler(outbox)
    dispatcher = RecordingDispatcher(calls, handler)
    transaction = RecordingTransactionRunner(calls, repository, outbox)
    original_pop_events = Calculation.pop_events

    def tracked_pop_events(calculation: Calculation) -> list[DomainEvent]:
        calls.append("pop")
        return original_pop_events(calculation)

    monkeypatch.setattr(Calculation, "pop_events", tracked_pop_events)
    service = CalculateService(repository, transaction, dispatcher)
    result = service.handle(CalculateCommand(operand_a=6, operator=Operator.MULTIPLY, operand_b=7))

    assert result.result == 42
    assert calls == ["transaction", "save", "pop", "dispatch", "outbox"]
    assert len(outbox.unpublished()) == 1


def test_handler_failure_rolls_back_calculation_and_outbox() -> None:
    repository = InMemoryCalculationRepository()
    outbox = InMemoryOutbox()
    failing_handler = FailingHandler()
    dispatcher = DomainEventDispatcher(
        {
            CalculationPerformed: (
                CalculationPerformedHandler(outbox),
                failing_handler,
            )
        }
    )
    transaction = InMemoryTransactionRunner(repository, outbox)
    service = CalculateService(repository, transaction, dispatcher)

    with pytest.raises(RuntimeError, match="handler failed"):
        service.handle(CalculateCommand(1, Operator.ADD, 2))

    assert failing_handler.event is not None
    assert repository.find_by_id(failing_handler.event.calculation_id) is None
    assert outbox.unpublished() == ()


def test_calculate_via_api(client) -> None:
    response = client.post(
        "/calculations",
        json={"operand_a": 10, "operator": "subtract", "operand_b": 4},
    )
    assert response.status_code == 201
    assert response.json()["result"] == 6
