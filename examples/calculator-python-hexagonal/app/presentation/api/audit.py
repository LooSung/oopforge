from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AuditEntry:
    action: str
    outcome: str
    correlation_id: str
    calculation_id: str | None = None


class AuditPort(Protocol):
    def record(self, entry: AuditEntry) -> None: ...
