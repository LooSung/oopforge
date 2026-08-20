from app.application.domain_events import (
    CalculationPerformedHandler,
    DomainEventDispatcher,
)
from app.application.services.calculation.calculate_service import CalculateService
from app.domain.calculation.model import CalculationPerformed
from app.infrastructure.in_memory_audit import InMemoryAuditLog
from app.infrastructure.in_memory_idempotency import InMemoryIdempotencyStore
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
_idempotency_store = InMemoryIdempotencyStore()
_audit_log = InMemoryAuditLog()


def get_calculate_service() -> CalculateService:
    return _service


def get_idempotency_store() -> InMemoryIdempotencyStore:
    return _idempotency_store


def get_audit_log() -> InMemoryAuditLog:
    return _audit_log


def get_outbox() -> InMemoryOutbox:
    return _outbox


def reset_runtime_state() -> None:
    _repository.restore({})
    _outbox.restore(())
    _idempotency_store.clear()
    _audit_log.clear()
