from app.application.domain_events import (
    CalculationPerformedHandler,
    DomainEventDispatcher,
)
from app.application.services.calculation.calculate_service import CalculateService
from app.domain.calculation.model import CalculationPerformed
from app.infrastructure.in_memory_outbox import InMemoryOutbox
from app.infrastructure.in_memory_transaction import InMemoryTransactionRunner
from app.infrastructure.repositories.calculation.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)

_repository = InMemoryCalculationRepository()
_outbox = InMemoryOutbox()
_event_handler = CalculationPerformedHandler(_outbox)
_event_dispatcher = DomainEventDispatcher(
    {CalculationPerformed: (_event_handler,)}
)
_transaction_runner = InMemoryTransactionRunner(_repository, _outbox)
_service = CalculateService(_repository, _transaction_runner, _event_dispatcher)


def get_calculate_service() -> CalculateService:
    return _service
