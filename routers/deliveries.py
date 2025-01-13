from typing_extensions import Annotated
from fastapi import APIRouter, Query
from models import Delivery, TotalDeliveryPrice
from api import get_venue_dynamic_info, get_venue_static_info
from delivery_service import get_distance_range, calculate_delivery_fee, calculate_distance, calculate_surcharge, calculate_total_price

router = APIRouter()

@router.get("/api/v1/delivery-order-price", response_model=TotalDeliveryPrice)
def get_delivery_order_price(
    venue_slug: Annotated[
        str,
        Query()
    ],
    cart_value: Annotated[
        int,
        Query()
    ],
    user_lat: Annotated[
        float,
        Query()
    ],
    user_lon: Annotated[
        float,
        Query()
    ],
):
    venue_static_data = get_venue_static_info(venue_slug)
    venue_dynamic_data = get_venue_dynamic_info(venue_slug)

    venue_location = venue_static_data["venue_raw"]["location"]["coordinates"]
    base_price = venue_dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
    distance_ranges = venue_dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
    order_minimum_no_surcharge = venue_dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]

    surcharge = calculate_surcharge(order_minimum_no_surcharge, cart_value)
    distance = calculate_distance(user_lat, user_lon , venue_location[1], venue_location[0])
    delivery_fee = calculate_delivery_fee(base_price, distance, get_distance_range(distance, distance_ranges))
    total_price = calculate_total_price(delivery_fee, cart_value, surcharge)

    return TotalDeliveryPrice(
        total_price=total_price,
        small_order_surcharge=surcharge,
        cart_value=cart_value,
        delivery=Delivery(
            fee=delivery_fee,
            distance=distance
        )
    )
