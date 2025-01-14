from typing_extensions import Annotated, Dict
from fastapi import APIRouter, Query, Depends
from schemas.delivery import TotalDeliveryPrice
from services.api import fetch_full_venue_data
from services.delivery import (
    get_distance_range, 
    calculate_delivery_fee, 
    calculate_distance, 
    calculate_surcharge, 
    calculate_total_price,
)

router = APIRouter()

@router.get("/api/v1/delivery-order-price", response_model=TotalDeliveryPrice)
def get_delivery_order_price(
    cart_value: Annotated[
        int,
        Query(gt=0)
    ],
    user_lat: Annotated[
        float,
        Query(ge=-90, le=90)
    ],
    user_lon: Annotated[
        float,
        Query(ge=-180, le=180)
    ],
    venue_data: Dict[str, Dict] = Depends(fetch_full_venue_data), # inheritely leverages param ?venue_slug=.... 
):
    """Fetches a delivery order price based on the venue, cart value, and user location.

    Query parameters:
      - venue_slug: a valid venue slug.
      - cart_value: total cart value (must be a positive integer).
      - user_lat: user latitude, between -90 and 90.
      - user_lon: user longitude, between -180 and 180.

    Example usage:
    ```
    GET /api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087
    ```

    Returns:
      - JSON containing the final total price, small order surcharge, cart value, and delivery details (fee, distance).
    """
    venue_static_data, venue_dynamic_data = venue_data["static"], venue_data["dynamic"]

    venue_location = venue_static_data["venue_raw"]["location"]["coordinates"]
    base_price = venue_dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
    distance_ranges = venue_dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
    order_minimum_no_surcharge = venue_dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]

    surcharge = calculate_surcharge(order_minimum_no_surcharge, cart_value)
    distance = calculate_distance(user_lon, user_lat , venue_location[0], venue_location[1])
    delivery_fee = calculate_delivery_fee(base_price, distance, get_distance_range(distance, distance_ranges))
    total_price = calculate_total_price(delivery_fee, cart_value, surcharge)

    return {
        "total_price": total_price,
        "small_order_surcharge": surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": distance,
        },
    }
