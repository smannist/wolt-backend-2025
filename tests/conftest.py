import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi import Request
from main import app as test_app
from services.api_fetchers import fetch_venue_coordinates, fetch_venue_pricing
from schemas.venue import VenueLocation, VenuePricing
from tests.delivery_constants import HELSINKI_VENUE_LAT, HELSINKI_VENUE_LON, DISTANCE_RANGES, BASE_PRICE, ORDER_MINIMUM_NO_SURCHARGE


@pytest.fixture
def app():
    """Fixture app instance for mocking"""
    return test_app


@pytest.fixture(scope="function")
def event_loop():
    """Fixture to provide an event loop for tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_client():
    """Fixture to provide a test client for the FastAPI app."""
    with TestClient(test_app) as client:
        yield client


@pytest.fixture
def anyio_backend():
    """Make AnyIO tests only with asyncio"""
    return "asyncio"


@pytest.fixture
def mock_delivery_route_dependencies(app):
    async def mock_fetch_venue_coordinates(
            request: Request,
            venue_slug: str) -> VenueLocation:
        return VenueLocation(
            lon=HELSINKI_VENUE_LON,
            lat=HELSINKI_VENUE_LAT
        )
    async def mock_fetch_venue_pricing(
            request: Request,
            venue_slug: str) -> VenuePricing:
        return VenuePricing(
            base_price=BASE_PRICE,
            order_minimum_no_surcharge=ORDER_MINIMUM_NO_SURCHARGE,
            distance_ranges=DISTANCE_RANGES
        )
    app.dependency_overrides[fetch_venue_coordinates] = mock_fetch_venue_coordinates
    app.dependency_overrides[fetch_venue_pricing] = mock_fetch_venue_pricing
    yield
    app.dependency_overrides.clear()
