import requests
from fastapi import Query
from typing_extensions import Dict, Annotated, Literal, Union, List
from schemas.venue import VenueLocation, VenuePricing

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

AllowedVenues = Literal[
    "home-assignment-venue-helsinki",
    "home-assignment-venue-stockholm",
    "home-assignment-venue-berlin",
    "home-assignment-venue-tokyo"
]


async def fetch_venue_coordinates(venue_slug: Annotated[
    AllowedVenues,
    Query()
]) -> Dict:
    """Fetches static coordinates of the venue return pydantic object with the coordinates"""
    url = f"{BASE_URL}/{venue_slug}/static"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return VenueLocation(
        lon=data["venue_raw"]["location"]["coordinates"][0],
        lat=data["venue_raw"]["location"]["coordinates"][1]
    )


async def fetch_venue_dynamic_pricing(venue_slug: Annotated[
        AllowedVenues,
        Query()
]) -> Dict[str, Union[int, List[Dict]]]:
    """Fetches dynamic venue data and returns a pydantic object containing pricing details"""
    url = f"{BASE_URL}/{venue_slug}/dynamic"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return VenuePricing(
        base_price=data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"],
        distance_ranges=data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"],
        order_minimum_no_surcharge=data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"])
