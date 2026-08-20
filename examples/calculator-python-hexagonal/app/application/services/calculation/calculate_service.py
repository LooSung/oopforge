from dataclasses import dataclass

from app.application.domain_events import DomainEventDispatcher
from app.application.transactions import TransactionRunner
from app.domain.calculation.model import Calculation, Operator
from app.domain.calculation.repository import CalculationRepository
from app.domain.calculation.value import CalculationId


@dataclass(frozen=True)
class CalculateCommand:
    operand_a: float
    operator: Operator
    operand_b: float


@dataclass(frozen=True)
class CalculationResult:
    calculation_id: str
    operand_a: float
    operator: str
    operand_b: float
    result: float


class CalculateService:
    def __init__(
        self,
        calculation_repository: CalculationRepository,
        transaction_runner: TransactionRunner,
        event_dispatcher: DomainEventDispatcher,
    ) -> None:
        self._calculation_repository = calculation_repository
        self._transaction_runner = transaction_runner
        self._event_dispatcher = event_dispatcher

    def handle(self, command: CalculateCommand) -> CalculationResult:
        return self._transaction_runner.run(lambda: self._perform(command))

    def _perform(self, command: CalculateCommand) -> CalculationResult:
        calculation = Calculation.perform(
            CalculationId.generate(),
            command.operand_a,
            command.operator,
            command.operand_b,
        )
        self._calculation_repository.save(calculation)
        self._event_dispatcher.dispatch(calculation.pop_events())
        return self._to_result(calculation)

    @staticmethod
    def _to_result(calculation: Calculation) -> CalculationResult:
        return CalculationResult(
            calculation_id=str(calculation.id.value),
            operand_a=calculation.operand_a,
            operator=calculation.operator.value,
            operand_b=calculation.operand_b,
            result=calculation.result,
        )
