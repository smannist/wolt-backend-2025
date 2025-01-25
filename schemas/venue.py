from pydantic import BaseModel
from typing import List, Dict


class VenueLocation(BaseModel):
    lon: float
    lat: float


class VenuePricing(BaseModel):
    base_price: int
    distance_ranges: List[Dict]
    order_minimum_no_surcharge: int
