import requests
from fastapi import Query
from typing_extensions import Dict, Annotated, Literal, Union, List

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

AllowedVenues = Literal[
    "home-assignment-venue-helsinki",
    "home-assignment-venue-stockholm",
    "home-assignment-venue-berlin",
    "home-assignment-venue-tokyo"
]


def fetch_venue_coordinates(venue_slug: Annotated[
    AllowedVenues,
    Query()
]) -> Dict:
    """Fetches static coordinates of the venue"""
    url = f"{BASE_URL}/{venue_slug}/static"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["venue_raw"]["location"]["coordinates"]


def fetch_venue_dynamic_pricing(venue_slug: Annotated[
        AllowedVenues,
        Query()]) -> Dict[str, Union[int, List[Dict]]]:
    """Fetches dynamic venue data and returns the pricing details"""
    url = f"{BASE_URL}/{venue_slug}/dynamic"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "base_price": data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"],
        "distance_ranges": data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"],
        "order_minimum_no_surcharge": data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]}
