import requests
from fastapi import Query
from typing_extensions import Dict, Annotated, Literal

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

def fetch_static_venue_data(venue_slug: str) -> dict:
    """Fetches static data about a venue."""
    url = f"{BASE_URL}/{venue_slug}/static"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_dynamic_venue_data(venue_slug: str) -> dict:
    """Fetches dynamic data about a venue."""
    url = f"{BASE_URL}/{venue_slug}/dynamic"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

AllowedVenues = Literal[
    "home-assignment-venue-helsinki",
    "home-assignment-venue-stockholm",
    "home-assignment-venue-berlin",
    "home-assignment-venue-tokyo"
]

def fetch_full_venue_data(
    venue_slug: Annotated[
        AllowedVenues, 
        Query()
    ]
) -> Dict[str, Dict]:
    """Fetches both static and dynamic data about the queried venue."""
    static_data = fetch_static_venue_data(venue_slug)
    dynamic_data = fetch_dynamic_venue_data(venue_slug)

    return {
        "static": static_data,
        "dynamic": dynamic_data
    }
