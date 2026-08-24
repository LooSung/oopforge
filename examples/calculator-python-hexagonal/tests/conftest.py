from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import reset_runtime_state
from app.main import app


@pytest.fixture(autouse=True)
def clean_runtime_state() -> None:
    reset_runtime_state()


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
