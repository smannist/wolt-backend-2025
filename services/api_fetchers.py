from fastapi import Request, Query
from typing_extensions import Annotated, Literal
from schemas.venue import VenueLocation, VenuePricing

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

ALLOWED_VENUES = Literal[
    "home-assignment-venue-helsinki",
    "home-assignment-venue-stockholm",
    "home-assignment-venue-berlin",
    "home-assignment-venue-tokyo"
]


async def fetch_venue_coordinates(
    request: Request,
    venue_slug: Annotated[
        ALLOWED_VENUES,
        Query()
    ]
) -> VenueLocation:
    """Fetches static coordinates of the venue and returns a Pydantic object with the coordinates."""
    url = f"{BASE_URL}/{venue_slug}/static"
    async with request.app.state.aio_session.get(url) as response:
        response.raise_for_status()
        data = await response.json()
        return VenueLocation(
            lon=data["venue_raw"]["location"]["coordinates"][0],
            lat=data["venue_raw"]["location"]["coordinates"][1]
        )


async def fetch_venue_pricing(
    request: Request,
    venue_slug: Annotated[
        ALLOWED_VENUES,
        Query()
    ]
) -> VenuePricing:
    """Fetches dynamic venue data and returns a Pydantic object containing pricing details."""
    url = f"{BASE_URL}/{venue_slug}/dynamic"
    async with request.app.state.aio_session.get(url) as response:
        response.raise_for_status()
        data = await response.json()
        return VenuePricing(
            base_price=data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"],
            distance_ranges=data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"],
            order_minimum_no_surcharge=data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
        )
