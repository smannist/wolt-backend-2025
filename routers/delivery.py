from typing_extensions import Annotated, Dict, Any
from fastapi import APIRouter, Query, Depends
from schemas.delivery import DeliveryOrderSummary
from services.api import fetch_venue_coordinates, fetch_venue_dynamic_pricing
from services.delivery import (
    get_distance_range,
    calculate_delivery_fee,
    calculate_distance,
    calculate_surcharge,
    calculate_total_price,
)

router = APIRouter()


@router.get("/api/v1/delivery-order-price", response_model=DeliveryOrderSummary, responses={
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "total_price": 1190,
                    "small_order_surcharge": 0,
                    "cart_value": 1000,
                    "delivery": {
                        "fee": 190,
                        "distance": 177
                    }
                }
            }
        },
    },
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "We are sorry, this location is currently outside our delivery range."
                },
            },
        },
    },
    422: {
        "description": "Validation error or missing parameters",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "error_count": 1,
                    "errors": [
                        {
                            "field": "query.user_lon",
                            "error_type": "missing",
                            "message": "user_lon is required."
                        },
                    ]
                }
            }
        },
    },
})
async def get_delivery_order_price(
    cart_value: Annotated[
        int,
        Query(ge=0)
    ],
    user_lat: Annotated[
        float,
        Query(ge=-90, le=90)
    ],
    user_lon: Annotated[
        float,
        Query(ge=-180, le=180)
    ],
    venue_location: Dict[Any, Dict] = Depends(fetch_venue_coordinates),
    venue_pricing: Dict[Any, Dict] = Depends(fetch_venue_dynamic_pricing)
):
    """Fetches a delivery order price based on the venue, cart value, and user location.

    Example usage:
    ```
    curl "http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
    ```

    Returns:
      - JSON containing the final total price, small order surcharge, cart value, and delivery details (fee, distance).
    """
    surcharge = calculate_surcharge(
        venue_pricing["order_minimum_no_surcharge"], cart_value)

    distance = calculate_distance(
        user_lon,
        user_lat,
        venue_location[0],
        venue_location[1])

    delivery_fee = calculate_delivery_fee(
        venue_pricing["base_price"], distance, get_distance_range(
            distance, venue_pricing["distance_ranges"]))

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
