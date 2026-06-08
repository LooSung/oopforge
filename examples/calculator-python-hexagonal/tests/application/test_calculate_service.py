from app.application.services.calculation.calculate_service import (
    CalculateCommand,
    CalculateService,
)
from app.domain.calculation.model import Operator
from app.infrastructure.repositories.calculation.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)


def test_handle_returns_result() -> None:
    service = CalculateService(InMemoryCalculationRepository())
    result = service.handle(CalculateCommand(operand_a=6, operator=Operator.MULTIPLY, operand_b=7))
    assert result.result == 42
    assert result.calculation_id


def test_calculate_via_api(client) -> None:
    response = client.post(
        "/calculations",
        json={"operand_a": 10, "operator": "subtract", "operand_b": 4},
    )
    assert response.status_code == 201
    assert response.json()["result"] == 6
