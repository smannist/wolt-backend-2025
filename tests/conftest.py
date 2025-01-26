import pytest
import asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="function")
def test_client():
    """Fixture to provide a test client for the FastAPI app."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def mock_aio_session(monkeypatch):
    """Fixture to mock the aiohttp client session."""
    mock_session = AsyncMock()
    monkeypatch.setattr("aiohttp.ClientSession")
    app.state.aio_session = mock_session
    yield mock_session


@pytest.fixture(scope="function")
def event_loop():
    """Fixture to provide an event loop for tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def anyio_backend():
    """Make AnyIO tests only with asyncio"""
    return "asyncio"
