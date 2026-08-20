from contextvars import ContextVar, Token
from dataclasses import dataclass
from uuid import uuid4


_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


@dataclass
class _RequestObservation:
    outcome: str = "completed"
    calculation_id: str | None = None


_observation: ContextVar[_RequestObservation | None] = ContextVar(
    "request_observation",
    default=None,
)


@dataclass(frozen=True)
class RequestContextTokens:
    correlation_id: Token[str]
    observation: Token[_RequestObservation | None]


def choose_correlation_id(candidate: str | None) -> str:
    if candidate and candidate == candidate.strip() and _is_safe_id(candidate):
        return candidate
    return str(uuid4())


def _is_safe_id(candidate: str) -> bool:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.:")
    return len(candidate) <= 128 and all(character in allowed for character in candidate)


def begin_request(correlation_id: str) -> RequestContextTokens:
    return RequestContextTokens(
        correlation_id=_correlation_id.set(correlation_id),
        observation=_observation.set(_RequestObservation()),
    )


def end_request(tokens: RequestContextTokens) -> None:
    _observation.reset(tokens.observation)
    _correlation_id.reset(tokens.correlation_id)


def mark_outcome(outcome: str, calculation_id: str | None = None) -> None:
    observation = _observation.get()
    if observation is not None:
        observation.outcome = outcome
        observation.calculation_id = calculation_id


def current_correlation_id() -> str:
    return _correlation_id.get()


def current_outcome() -> str:
    observation = _observation.get()
    return observation.outcome if observation is not None else "completed"


def current_calculation_id() -> str | None:
    observation = _observation.get()
    return observation.calculation_id if observation is not None else None
