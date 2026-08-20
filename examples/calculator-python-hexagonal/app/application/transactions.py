from typing import Callable, Protocol, TypeVar


T = TypeVar("T")


class TransactionRunner(Protocol):
    def run(self, operation: Callable[[], T]) -> T: ...
