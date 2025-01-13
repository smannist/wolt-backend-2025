import requests
from typing_extensions import Dict

BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

def get_venue_static_info(venue_slug: str) -> Dict[str, str | int]:
    """Fetches static information about a venue."""
    url = f"{BASE_URL}/{venue_slug}/static"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_venue_dynamic_info(venue_slug: str) -> Dict[str, str | int]:
    """Fetches dynamic information about a venue."""
    url = f"{BASE_URL}/{venue_slug}/dynamic"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
